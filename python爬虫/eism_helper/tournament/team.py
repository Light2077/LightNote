from base import BaseManager


# team tournament 至多5场 每场1个1v1
class TeamTournament(BaseManager):
    def __init__(self, driver, id_):
        super().__init__(driver, id_=id_, name="teamTournament")
        self.end_ = False

    # 获得战场id
    def get_battle_id(self):
        if self.is_ended:
            print("%s is finished!" % self.name)
            return

        xpath = "//td[@class='marked']/a/parent::tr/td[4]/a"

        try:
            elements = self.driver.find_elements_by_xpath(xpath)
            if elements:
                return elements[-1].get_attribute("href")
            else:
                print("%s may not begin" % self.name)
        except Exception as e:
            print(str(e))

    @property
    def is_ended(self):
        if self.end_:
            return True
        # self.page()
        element = self.driver.find_element_by_xpath("//li[@class='rc-active']/a")
        if element.get_attribute("href").rsplit("#")[-1] == "slideRank":
            print("%s is finished, close the page!" % self.name)
            self.end_ = True
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[-1])
            return True
        else:
            return False
