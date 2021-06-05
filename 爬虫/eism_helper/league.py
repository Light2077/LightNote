"""

查看 league 是否结束
查看 battle 是否结束
如果 league 结束 程序结束
如果 battle 结束 等待一段时间再查看

"""
from base import BaseManager


# 国家杯 共5场 每场一个1v1
class League(BaseManager):
    def __init__(self, driver, id_):
        super().__init__(driver, id_=id_, name="tournamentEvent")
        self.end_ = False

    # 获得战场id
    def get_battle_id(self):
        if self.is_ended:
            print("league is finished!")
            return
        xpath = "//table/tbody/tr/td[2][@style='background:lightgreen']/parent::tr/td[4]/a"\
                "|"\
                "//table/tbody/tr/td[6][@style='background:lightgreen']/parent::tr/td[4]/a"
        try:
            links = self.driver.find_elements_by_xpath(xpath)
            if not links:
                print("league is not begin!")
                return

            battle_id = links[-1].get_attribute("href").split("=")[-1]
            return battle_id

        except Exception as e:
            print(str(e))

    @property
    def is_ended(self):
        if self.end_:
            return True
        self.page()
        ranking_label = self.driver.find_element_by_xpath("//li[@class='rc-active']/a")
        if ranking_label.get_attribute("href").split("#")[-1] == "slide6":
            self.end_ = True
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[-1])
            return True
        else:
            return False
