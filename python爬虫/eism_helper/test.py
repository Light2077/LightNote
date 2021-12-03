import time
from selenium.webdriver.chrome.webdriver import WebDriver


def test_league(driver: WebDriver):
    from tournament.league import League
    lea = League(driver, "516")

    # 转到国家杯页面
    lea.page()
    time.sleep(1)
    battle_id = lea.get_battle_id()
    print(battle_id)
    # 转到国家杯页面
    lea.page()
    time.sleep(1)
    driver.find_element_by_xpath("//a[@href='#slide5']").click()
    time.sleep(1)
    battle_id = lea.get_battle_id()
    print(battle_id)
