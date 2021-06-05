import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
import tqdm
from league import League


import config
from battle import Battle


class EsimHelper:
    def __init__(self):
        self.options = ChromeOptions()
        # 规避检测
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_argument("user-data-dir=%s" % config.chrome_user_data_path)
        self.driver = webdriver.Chrome(config.driver_path, options=self.options)
        self.driver.implicitly_wait(10)
        self.username = config.username
        self.password = config.password
        self.url = config.url

    def login(self):
        self.driver.get(config.url)
        time.sleep(1)
        try:
            self.driver.find_element_by_id("userAvatar")
            # element = WebDriverWait(self.driver, 30).until(
            #     EC.presence_of_element_located((By.ID, 'indexShortcut'))
            # )
            print("已登录!")
            return
        except Exception as e:
            print(e)
            pass

        username_input = self.driver.find_element_by_id("registeredPlayerLogin")
        password_input = self.driver.find_elements_by_xpath("//input[@name='password']")[0]
        time.sleep(1)
        login_btn = self.driver.find_element_by_xpath("//button[@value='Login']")

        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        time.sleep(1)
        login_btn.click()

        # 保存cookie
        # cookies = driver.get_cookies()
        # with open("cookies.json", "w", encoding="utf8") as f:
        #     json.dump(cookies, f)

    def select_item(self, food="Q5", gift="Q5", weapon="Q1"):
        time.sleep(1)
        self.driver.find_element_by_id("sfood" + food).click()
        self.driver.find_element_by_id("sgift" + gift).click()
        self.driver.find_element_by_id("weapon" + weapon).click()

    # 回复体力
    def recover(self):
        health = self.driver.find_element_by_id("actualHealth")
        health = float(health.text)
        food_limit = int(self.driver.find_element_by_id("foodLimit2").text)
        gift_limit = int(self.driver.find_element_by_id("giftLimit2").text)
        if health > 50:
            print("体力大于50，无需补充")
            return

        if food_limit > 0:
            eat_food_btn = self.driver.find_element_by_id("eatButton2")
            eat_food_btn.click()
            print("use food!")
        elif gift_limit > 0:
            eat_food_btn = self.driver.find_element_by_id("useGiftButton2")
            eat_food_btn.click()
            print("use gift!")

        time.sleep(1)

    # 自动战斗，每场比赛自动打一下
    def auto_fight(self, battle_id):
        battle = Battle(self.driver, battle_id)
        time.sleep(1)
        self.select_item(weapon="Q1")

        while True:
            if battle.is_ended:
                print("战斗结束!")
                break
            battle.page()
            print("damage", battle.my_damage)
            self.recover()
            # 伤害低于一个阈值则攻击
            if battle.my_damage < 100:
                battle.hit()
            time.sleep(60)


def auto_league(league_id):
    # 516
    lea = League(eh.driver, league_id)
    while True:
        if battle_id := lea.get_battle_id():
            eh.auto_fight(battle_id)
        else:
            break
        time.sleep(300)


if __name__ == '__main__':
    eh = EsimHelper()
    eh.login()
    battle1 = Battle(eh.driver, 101883)
    battle2 = Battle(eh.driver, 101882)
