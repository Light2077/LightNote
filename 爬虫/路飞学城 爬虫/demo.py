import requests
import time
from lxml import etree
from chaojiying import ocr

import os

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/90.0.4430.93 Safari/537.36"
}
# url = "http://www.renren.com/SysHome.do"

# text = requests.get(url, headers=headers)
# tree = etree.HTML(text)

# code_img_src = tree.xpath('//*[@id="verifyPic_login"]/@src')[0]
code_path = "code.png"
session = requests.session()

data = {
    "email": "15261813289",
    "password": "renren1996social",
    "icode": "",
    "origURL": "http://www.renren.com/home",
    "domain": "renren.com",
    "key_id": "1",
    "captcha_type": "web_login"
}

resp = session.post("http://www.renren.com/PLogin.do", headers=headers, data=data)

