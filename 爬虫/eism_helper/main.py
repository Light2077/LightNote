# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.




import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions

# 规避检测
options = ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
path = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
url = "https://roxa.e-sim.org/battle.html?id=3454"


driver = webdriver.Chrome(path, options=options)

driver.get('https://www.baidu.com')
driver.save_screenshot("baidu.png")
print(driver.page_source)