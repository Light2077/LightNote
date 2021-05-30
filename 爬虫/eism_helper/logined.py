import time
import json

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains


# 规避检测
options = ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
path = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"

url = "https://primera.e-sim.org/index.html"

driver = webdriver.Chrome(path, options=options)

driver.get(url)
with open("cookies.json", "r", encoding="utf8") as f:
    cookies = json.load(f)
for cookie in cookies:
    driver.add_cookie(cookie)
time.sleep(1)


def fight():
    fight_btn = driver.find_element_by_id("fightButton1")
    fight_btn.click()
    # fight_again_btn = driver.find_element_by_id("fightagainbutton")
    time.sleep(1)
    ActionChains(driver).move_by_offset(100, 100).click().perform()


def auto_flight(battle_id):

    driver.get("https://primera.e-sim.org/battle.html?id=%s" % battle_id)
    time.sleep(1)
    select_item()

    while True:
        if is_ended():
            print("战斗结束!")
            break

        damage_div = driver.find_element_by_id("topPlayerHit")
        my_damage = int(damage_div.text.replace(",", ""))
        print("damage", my_damage)
        eat()
        if my_damage < 100:
            fight()
        time.sleep(60)
        driver.refresh()
        time.sleep(2)


def select_item():
    driver.find_element_by_id("sfoodQ5").click()
    driver.find_element_by_id("sgiftQ5").click()
    driver.find_element_by_id("weaponQ1").click()


def eat():
    health = driver.find_element_by_id("actualHealth")
    health = float(health.text)
    if health <= 50:
        eat_food_btn = driver.find_element_by_id("eatButton2")
        eat_food_btn.click()
        print("eat food!")
    time.sleep(1)


def time2sec(time_):
    # 00:02:13
    h, m, s = time_.split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)


def check_time():
    end_time = driver.find_element_by_class_name("countdown-row.countdown-amount")
    sec = time2sec(end_time.text)
    return sec


def is_ended():
    defender_ball = driver.find_element_by_xpath("//div[@class='fightRounds fightRoundsDefender']/img[1]")
    defender_color = defender_ball.get_attribute("src").split("/")[-1]

    attacker_ball = driver.find_element_by_xpath("//div[@class='fightRounds fightRoundsAttacker']/img[8]")
    attacker_color = attacker_ball.get_attribute("src").split("/")[-1]

    if defender_color == attacker_color:
        return False
    return True

# countdown-row countdown-amount
if __name__ == '__main__':
    auto_flight(101730)
    # auto_flight(101742)
    # auto_flight(101673)
    pass
