"""

查看 country tournament 是否结束
查看 battle 是否结束
如果 league 结束 程序结束
如果 battle 结束 等待一段时间再查看

"""
import time

from base import BaseManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# country tournament 共5场 每场2个1v1
class CountryTournament(BaseManager):
    def __init__(self, driver, id_):
        super().__init__(driver, id_=id_, name="countryTournament")
        self.end_ = False

    # 获得战场id
    def get_battle_ids(self):
        if self.is_ended:
            print("%s is finished!" % self.name)
            return

        self.driver.find_element_by_xpath("//a[@href='#slideShedule']").click()
        time.sleep(10)
        xpath = '//*[@id="table-container"]/div[3]/table/tbody/tr[1]/td[%s]//a'

        try:
            for i in range(5, 0, -1):
                elements = self.driver.find_elements_by_xpath(xpath % (i + 2))
                battle_ids = []
                for k in range(0, 4, 2):
                    href = elements[k].get_attribute("href")
                    if href:
                        battle_ids.append(href.split("=")[-1])
                if battle_ids:
                    return battle_ids
            print("country tournament may not begin")
        except Exception as e:
            print(str(e))

    @property
    def is_ended(self):
        if self.end_:
            return True
        self.page()
        xpath = "//li[@class='ajaxDrivenTournament__buttons__wrapper__" \
                "button ajaxDrivenTournament__buttons__wrapper__button--" \
                "active']/a"

        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        print(element.get_attribute("href"))

        if element.get_attribute("href").rsplit("#")[-1] == "slideRank":
            print("country tournament is finished, close the page!")
            self.end_ = True
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[-1])
            return True
        else:
            return False
