import time
from selenium import webdriver
from chaojiying import ocr
from PIL import ImageGrab

driver = webdriver.Chrome('C:\Program Files\Google\Chrome\Application\chromedriver.exe')

driver.get("https://kyfw.12306.cn/otn/resources/login.html")
driver.maximize_window()

tag = driver.find_element_by_xpath("//li[@class='login-hd-account']")
time.sleep(1)
tag.click()
time.sleep(1)

# 下载图片
img = driver.find_element_by_id("J-loginImg")
# 直接截图也可以
# img.screenshot("a.jpg")

# 根据页面坐标来截图
# 确定验证码的左上角和右下角坐标
# 左上角 img.location {'x': 1016, 'y': 292}
# img.size {'height': 188, 'width': 300}
# 右下角就可以计算出来了

# 由于笔记本电脑有放大125%，需要额外乘个系数
x_left = img.location["x"] * 1.25
y_top = img.location["y"] * 1.25

x_right = x_left + img.size["width"] * 1.25
y_bottom = y_top + img.size["height"] * 1.25

rangle = (x_left, y_top, x_right, y_bottom)
# (1016, 292, 1316, 480)

i = ImageGrab.grab(rangle)
# 根据指定区域进行图片裁剪
frame = i.crop(rangle)
i.save("cc.png")


# 使用超级鹰识别验证码图片
def get_verification_result():
    # 9004 就是12306的识别对象
    im = open('a.jpg', 'rb').read()
    res = ocr.PostPic(im, 9004)
    return res


# 对指定坐标进行点击
action = webdriver.ActionChains(driver)
action.move_to_element_with_offset(img, 123, 444).click().perform()

# ps: 这个代码不完整，仅作为参考
