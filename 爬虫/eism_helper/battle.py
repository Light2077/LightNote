"""
http://primera.e-sim.org/region.html?id=266

- 当地必是防守方
- 若是起义战，当地也是进攻方
- 若非起义战，要寻找当地的领近地区，且进攻国家同

页面跳转逻辑

- 战场页面 读取进攻方国家和防守方国家
- 地区页面
- 飞行页面
- 战场页面

"""
import time

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

from base import BaseManager
import requests
import config

BATTLE_TYPE = ("起义战", "进攻战")


class Battle(BaseManager):
    def __init__(self, driver, id_):
        super().__init__(driver, id_=id_, name="battle")
        # 防守方和进攻方名字
        self.defender = self.driver.find_element_by_class_name("alliesList.leftList.fightFont").text
        self.attacker = self.driver.find_element_by_class_name("alliesList.rightList.fightFont").text

        # 地区地址和url
        self.area = self.driver.find_element_by_xpath("//div[@id='fightName']/span/a").text
        self.area_url = self.driver.find_element_by_xpath("//div[@id='fightName']/span/a").get_attribute(
            "href")

        self.end_ = False
        self.type = self.check_type()
        # 更新战斗信息
        # self.update_battle()

    # 必须要在战斗页面才能访问battle的属性
    # 当前战斗轮次的id，战斗结束就不能访问了
    @property
    def battle_round_id(self):
        return self.driver.find_element_by_id("battleRoundId").get_attribute("value")

    # 防御方得分
    @property
    def defender_score(self):
        return len(self.driver.find_elements_by_xpath("//*[contains(@src, 'blue_ball')]"))

    # 进攻方得分
    @property
    def attacker_score(self):
        return len(self.driver.find_elements_by_xpath("//*[contains(@src, 'red_ball')]"))

    # 战斗类型
    def check_type(self):
        tags = self.driver.find_elements_by_xpath("//div[@id='fightName']/span/*[2]")
        if tags:
            tag = tags[0]
            if tag.text[:3] == "起义战":
                return "起义战"
            else:
                return "未知战"
        return "进攻战"

    # 自己的输出
    @property
    def my_damage(self):
        return int(self.driver.find_element_by_id("topPlayerHit").text.replace(",", ""))

    # 检查战斗是否已结束
    @property
    def is_ended(self):
        if self.end_:
            return True
        self.page()
        if self.defender_score == 8 or self.attacker_score == 8:
            self.end_ = True
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[-1])
            return True
        return False

    def update_battle(self):
        """
        更新战斗数据
        :return:
        """
        if self.is_ended:
            print("战斗已结束")
            return

        url = config.url + "battleScore.html"

        params = {
            "id": self.battle_round_id,
            "at": config.user_id,
            "ci": 63,  # 国籍id？
        }
        resp = requests.get(url, headers=config.headers, params=params)
        data = resp.json()

        if not data["top10Defenders"]:
            self.top_defend_damage = 0
        else:
            self.top_defend_damage = int(data["top10Defenders"][0]["influence"].replace(",", ""))
        if not data["top10Attackers"]:
            self.top_attack_damage = 0
        else:
            self.top_attack_damage = int(data["top10Attackers"][0]["influence"].replace(",", ""))

        # 剩余时间
        self.remaining_time = int(data["remainingTimeInSeconds"])

        for player in data["top10Defenders"]:
            if player["playerName"] == config.username:
                self.my_defend_damage = int(player["influence"].replace(",", ""))
                break
        else:
            self.my_defend_damage = 0

        for player in data["top10Attackers"]:
            if player["playerName"] == config.username:
                self.my_attack_damage = int(player["influence"].replace(",", ""))
                break
        else:
            self.my_attack_damage = 0

    def travel_to_defender(self):
        # 直接旅行到当地即可
        if self.type in ["起义战", "进攻战"]:
            travel(self.driver, self.area_url)
            print("旅行成功")
        print("可能是国家杯，无需旅行")

    def travel_to_attacker(self):
        # 起义战旅行到当地即可
        if self.type == "起义战":
            travel(self.driver, self.area_url)

        elif self.type == "进攻战":
            # 寻找临近的进攻地区
            area_url = find_attack_area(self.driver, self.area_url, self.attacker)
            travel(self.driver, area_url)
        else:
            print("可能是国家杯，无需旅行")
            return
        print("旅行成功")

    # 获取战场倒计时还剩多少秒
    def get_countdown_second(self):
        # "00:12:44"
        time_text = self.driver.find_element_by_class_name("countdown-row.countdown-amount").text
        h, m, s = time_text.split(":")
        return 3600 * int(h) + 60 * int(m) + int(s)

    # 为防御方 输出
    # 除了起义战以外的战场 都只用fightButton1
    # 默认为防守方打1下
    def hit(self, defender=True, berserk=False):
        # 是否暴击
        btn_id = "fightButtonBerserk" if berserk else "fightButton"

        # 默认为防御方输出，国家杯这种比赛也是默认防御方输出即可
        if defender:
            btn_id += "1"
        else:
            btn_id += "2"
        btn = self.driver.find_element_by_id(btn_id)

        btn.click()
        # 显示伤害
        damage = self.driver.find_element_by_id("DamageDone").text.strip().replace(",", "")
        print("damage:", damage)

        # 关闭提示窗口
        close_btn = self.driver.find_element_by_class_name("pico-close")
        close_btn.click()


"""
travel 
"""


# 飞行到某地
def travel(driver, area_url, ticket_level="5"):
    current_area_xpath = "//a[contains(@href, 'region.html')]"
    current_area_id = driver.find_element_by_xpath(current_area_xpath).get_attribute("href").split("=")[-1]
    taget_area_id = area_url.split("=")[-1]
    if current_area_id == taget_area_id:
        print("无需飞行，已在:", area_url)
        return

    driver.get(area_url)
    # 选择机票等级
    ticket_select = Select(driver.find_element_by_id("ticketQuality"))
    ticket_select.select_by_value(ticket_level)

    # 点击旅行按钮
    travel_btn = driver.find_element_by_class_name("travel.button.foundation-style")
    #
    print("travel to:", area_url)
    # travel_btn.click()


def find_attack_area(driver, area_url, country):
    # 去往当地页面
    if area_url != driver.current_url:
        driver.get(area_url)

    xpath = "//*[@id='esim-layout']/table[1]/tbody/tr/td[3]/div[1][contains(@class, '%s')]" % country
    print("进攻方: ", country, xpath)
    tag = driver.find_element_by_xpath(xpath)
    attack_area_url = tag.find_element_by_xpath("../../td/a").get_attribute("href")
    return attack_area_url
