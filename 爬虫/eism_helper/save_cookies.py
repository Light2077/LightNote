import time
import json

from selenium import webdriver
from selenium.webdriver import ChromeOptions

# 规避检测
options = ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
path = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"

url = "https://primera.e-sim.org/index.html"

username = "Light L"
password = "569853885"
driver = webdriver.Chrome(path, options=options)

driver.get(url)

login_section_btn = driver.find_element_by_id("login_section_btn")
login_section_btn.click()
time.sleep(1)
username_input = driver.find_element_by_id("registeredPlayerLogin")
password_input = driver.find_elements_by_xpath("//input[@name='password']")[1]
login_btn = driver.find_element_by_xpath("//button[@value='Login']")


username_input.send_keys(username)
password_input.send_keys(password)
time.sleep(1)
login_btn.click()


cookies = driver.get_cookies()
with open("cookies.json", "w", encoding="utf8") as f:
    json.dump(cookies, f)