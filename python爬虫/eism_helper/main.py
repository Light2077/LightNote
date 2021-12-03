import time

import tqdm
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from tournament.league import League
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import asyncio
from tournament.country import CountryTournament

import config
from battle import Battle


class EsimHelper:
    def __init__(self):
        self.options = ChromeOptions()
        # 规避检测
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_argument("user-data-dir=%s" % config.chrome_user_data_path)
        desired_capabilities = DesiredCapabilities.CHROME
        desired_capabilities["pageLoadStrategy"] = "none"

        self.driver = webdriver.Chrome(config.driver_path, options=self.options,
                                       desired_capabilities=desired_capabilities)
        self.driver.implicitly_wait(15)
        self.username = config.username
        self.password = config.password
        self.url = config.url

    def login(self):
        # 如果不开代理的话，会因为要加载谷歌的服务而等待很久
        self.driver.get(config.url)
        try:
            self.driver.find_element_by_id("indexShortcut")
            # element = WebDriverWait(self.driver, 10).until(
            #     EC.presence_of_element_located((By.ID, 'indexShortcut'))
            # )
            print("已登录!")
            return
        except Exception as e:

            print("未登录!", e)
            pass

        self.driver.find_element_by_id("login_section_btn").click()
        username_input = self.driver.find_element_by_id("registeredPlayerLogin")
        password_input = self.driver.find_elements_by_xpath("//input[@name='password']")[1]
        login_btn = self.driver.find_element_by_xpath("//button[@value='Login']")

        username_input.clear()
        password_input.clear()
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
        print("select food %s, gift %s, weapon %s" % (food, gift, weapon))
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
        else:
            raise ValueError("Food/Gift limit not enough!")

        time.sleep(1)

    # 自动战斗
    async def auto_fight(self, battle_id, min_damage=100):
        battle = Battle(self.driver, battle_id)
        print("auto battle:", battle_id)
        self.select_item(weapon="Q1")
        error_count = 0
        while True:

            try:
                battle.page()
                if battle.is_ended:
                    print("战斗结束!")
                    break
                print("current damage", battle.my_damage)
                self.recover()
                # 伤害低于一个阈值则攻击
                if battle.my_damage < min_damage:
                    battle.hit()

            except Exception as e:
                print(e)
                error_count += 1

                if error_count > 3:
                    break

                continue

            # 等待60秒
            print("wait 60 sec")
            await asyncio.sleep(60)
            error_count = 0


async def auto_country_tournament(driver, tournament_id):
    ct = CountryTournament(driver, tournament_id)
    while True:
        ct.page()
        battle_id = ct.get_battle_ids()
        if not battle_id:
            break
        tasks = [
            asyncio.create_task(eh.auto_fight(battle_id[0])),
            asyncio.create_task(eh.auto_fight(battle_id[1])),
        ]
        done, pending = await asyncio.wait(tasks)
        print("battle is end!")

        time.sleep(300)


async def auto_league(driver, tournament_id):
    # 516
    lea = League(driver, tournament_id)
    count = 0
    while True:
        if count > 0:
            time.sleep(150)

        battle_id = lea.get_battle_id()
        if battle_id:
            await eh.auto_fight(battle_id)
        else:
            break
        count += 1


async def auto_team_tournament(driver, tournament_id):
    from tournament.team import TeamTournament
    # 8
    tournament = TeamTournament(driver, tournament_id)
    while True:
        battle_id = tournament.get_battle_id()
        if battle_id:
            await eh.auto_fight(battle_id)
        else:
            break
        time.sleep(300)


async def auto_cup_tournament(driver, tournament_id):
    from tournament.cup import CupTournament
    # 8
    tournament = CupTournament(driver, tournament_id)
    while True:

        battle_id = tournament.get_battle_id()
        if battle_id:
            await eh.auto_fight(battle_id)
        else:
            break
        print("wait 60 sec")
        time.sleep(60)
        tournament.page()


# ct = CountryTournament(eh.driver, 38)
if __name__ == '__main__':
    eh = EsimHelper()
    eh.login()
    # 自动 country tournament
    # asyncio.run(auto_country_tournament(eh.driver, 39))
    # asyncio.run(eh.auto_fight(102864))
    asyncio.run(auto_cup_tournament(eh.driver, 525))
    # 自动 league
    # asyncio.run(auto_league(eh.driver, 524))

    # 自动 team tournament
    # asyncio.run(auto_team_tournament(eh.driver, 8))
