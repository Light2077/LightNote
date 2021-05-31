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
import requests
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import Select
import config

BATTLE_TYPE = ("起义战", "进攻战")


class Battle:
    def __init__(self, driver, battle_id):
        self.driver = driver
        # 打开战斗界面
        self.url = config.url + "battle.html?id=%s" % battle_id
        self.driver.get(self.url)

        self.defender = self.driver.find_element_by_class_name("alliesList.leftList.fightFont").text
        self.attacker = self.driver.find_element_by_class_name("alliesList.rightList.fightFont").text

        # 地区地址和url
        self.area = self.driver.find_element_by_xpath("//div[@id='fightName']/span/a").text
        self.area_url = self.driver.find_element_by_xpath("//div[@id='fightName']/span/a").get_attribute(
            "href")

        # 战斗类型
        self.battle_type = self.get_battle_type()

        #
        self.update_battle()

    # 必须要在战斗页面才能访问battle的属性
    # 是哪一轮战斗
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

    def get_battle_type(self):
        tags = self.driver.find_elements_by_xpath("//div[@id='fightName']/span/*[2]")
        if tags:
            tag = tags[0]
            if tag.text[:3] == "起义战":
                return "起义战"
            else:
                return "未知战"
        return "进攻战"

    def update_battle(self):
        """
        更新战斗数据
        :return:
        """
        if self.is_ended():
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
        if self.battle_type in ["起义战", "进攻战"]:
            travel(self.driver, self.area_url)
            print("旅行成功")
        print("可能是国家杯，无需旅行")

    def travel_to_attacker(self):
        if self.battle_type == "起义战":
            travel(self.driver, self.area_url)

        elif self.battle_type == "进攻战":
            # 寻找临近的进攻地区
            area_url = self.find_attack_area()
            travel(self.driver, area_url)
        else:
            print("可能是国家杯，无需旅行")
            return

        print("旅行成功")

    def find_attack_area(self):
        self.driver.get(self.area_url)
        tags = self.driver.find_elements_by_xpath("//*[@id='esim-layout']/table[1]/tbody/tr")
        for tag in tags[1:]:

            pass

    # 获取战场倒计时还剩多少秒
    def get_countdown_second(self):
        # "00:12:44"
        time_text = self.driver.find_element_by_class_name("countdown-row.countdown-amount").text
        h, m, s = time_text.split(":")
        return 3600 * int(h) + 60 * int(m) + int(s)

    # 检测是否在战斗页面
    def is_battle_page(self):
        return "battle" in self.driver.current_url

    # 检查战斗是否已结束
    def is_ended(self):
        if self.defender_score == 8 or self.attacker_score == 8:
            return True
        return False


"""
travel 

"""


# 飞行到某地
def travel(driver, area_url, ticket_level="5"):
    driver.get(area_url)
    # 选择机票等级
    ticket_select = Select(driver.find_element_by_id("ticketQuality"))
    ticket_select.select_by_value(ticket_level)

    # 点击旅行按钮
    travel_btn = driver.find_element_by_class_name("travel.button.foundation-style")
    travel_btn.click()