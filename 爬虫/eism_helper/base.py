"""
管理者基类
- 管理战斗页面
- 管理国家杯页面
- 管理拍卖页面

未应用到战斗页面
"""
from selenium.webdriver.chrome.webdriver import WebDriver
import config


class BaseManager:
    def __init__(self, driver: WebDriver, name, id_):
        self.driver = driver
        self.server = config.server_name
        self.name = name
        self.id = str(id_)
        # https://primera.e-sim.org/battle.html?id=100655
        # server: primera type_: battle id_: 100655
        self.url = f"https://{self.server}.e-sim.org/{self.name}.html?id={self.id}"
        self.handle = self.open_new_tab(self.url)

    # 是否在当前页面
    @property
    def in_page(self):
        return self.name in self.driver.current_url and self.id in self.driver.current_url

    # 转至当前页
    def page(self):
        if self.handle not in self.driver.window_handles:
            self.handle = self.open_new_tab(self.url)
        else:
            print("刷新界面:", self.url)
            self.driver.switch_to.window(self.handle)
            self.driver.refresh()

    def open_new_tab(self, url):
        self.driver.switch_to.window(self.driver.window_handles[-1])
        new_page = f'window.open("{url}");'
        self.driver.execute_script(new_page)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        return self.driver.window_handles[-1]
