import time
from selenium import webdriver

driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')

driver.get("https://www.taobao.com")
time.sleep(1)
search_input = driver.find_element_by_id("q")
# 文本框输入内容
search_input.send_keys("python")
# 点击搜索按钮

time.sleep(1)
search_btn = driver.find_element_by_class_name("btn-search.tb-bg")
search_btn.click()