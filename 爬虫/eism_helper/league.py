"""

查看 league 是否结束
查看 battle 是否结束
如果 league 结束 程序结束
如果 battle 结束 等待一段时间再查看

"""
from selenium.webdriver.chrome.webdriver import WebDriver
import config


class League:
    def __init__(self, driver: WebDriver, league_id):
        self.driver = driver
        self.id = league_id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, league_id):
        self._id = league_id
        self.url = config.url + "/tournamentEvent.html?id=%s" % league_id

    def get_battle_id(self):
        self.driver.get(self.url)
        if self.is_ended():
            print("league is finished!")
            return
        xpath = "//table/tbody/tr/td[2][@style='background:lightgreen']/parent::tr/td[4]/a"\
                "|"\
                "//table/tbody/tr/td[6][@style='background:lightgreen']/parent::tr/td[4]/a"
        try:
            battle_link = self.driver.find_elements_by_xpath(xpath)[-1].get_attribute("href")
            battle_id = battle_link.split("=")[-1]
            return battle_id

        except Exception as e:
            print(str(e))

    def is_ended(self):
        ranking_label = self.driver.find_element_by_xpath("//li[@class='rc-active']/a")
        if ranking_label.get_attribute("href").split("#")[-1] == "slide6":
            return True
        else:
            return False
