from selenium import webdriver
import time
import requests
from lxml import etree
import os

driver = webdriver.Chrome('C:\Program Files\Google\Chrome\Application\chromedriver.exe')


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
}

save_dir = "鬼灭之刃"

def create_dir(dirname):
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
        
        
def get_comic_urls():

    html = requests.get("http://www.mh1234.com/comic/17951.html", headers=headers).text
    tree = etree.HTML(html)
    
    # 获得每话的url
    urls = tree.xpath("//ul[@id='chapter-list-2']/li/a/@href")
    return urls

create_dir(save_dir)
urls = get_comic_urls()

for url in urls:
    
    # http://www.mh1234.com/comic/17951/961925.html
    url = "http://www.mh1234.com" + url
    i = 1
    error_num = 10
    while True:
        params = {
            "p": i
            }
        # resp = requests.get(url, params=params, headers=headers)
        # resp.encoding = "utf8"
        # html = resp.text
        try:
            driver.get(url+"?p="+str(i))
            tree = etree.HTML(driver.page_source)
            
            title = tree.xpath("//body/h1/text()")[0].strip()
            comic_save_dir = os.path.join(save_dir, title)
            create_dir(comic_save_dir)
            
            img_src = tree.xpath("//div[@id='images']/img/@src")[0]
            img_index = tree.xpath("//div[@id='images']/img/@data-index")[0]
            img_info = tree.xpath("//p[@class='img_info']/text()")[0]  # (1/21)
        
        except:
            if error_num <= 0:
                break
            else:
                error_num -= 1
                print("error_num: ", error_num)
                continue

        img_total_page = int(img_info.strip("()").split("/")[-1])
        img_save_path = os.path.join(comic_save_dir, str(img_index) + ".jpg")
        if not os.path.isfile(img_save_path):
            img = requests.get(img_src, headers=headers).content
            with open(img_save_path, "wb") as f:
                f.write(img)
            
        
        if i >= img_total_page:
            break
        i += 1
        time.sleep(1)
        


driver.close()
