import requests
import time
from lxml import etree

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/90.0.4430.93 Safari/537.36"
}


def get_html():
    url = "http://bj.58.com/ershoufang/"
    text = requests.get(url, headers=headers).text
    return text


# 解析一页的房屋数据
def parse(html):
    tree = etree.HTML(html)
    houses = tree.xpath("//div[@class='property']")
    for house in houses:
        data = dict()
        # 标题
        data['title'] = house.xpath(".//h3[@class='property-content-title-name']/text()")[0]
        # 户型
        unit_type = house.xpath(".//p[@class='property-content-info-text property-content-info-attribute']//text()")
        data['unit_type'] = "".join(unit_type)
        # 面积
        data['aera'] = house.xpath(".//p[@class='property-content-info-text'][1]//text()")[0].strip()
        # 朝向
        data['ori'] = house.xpath(".//p[@class='property-content-info-text'][2]//text()")[0].strip()

        # 小区名
        data['community_name'] = house.xpath(".//p[@class='property-content-info-comm-name']//text()")[0].strip()
        # 小区地址
        community_addr = house.xpath(".//p[@class='property-content-info-comm-address']//text()")
        data['community_addr'] = " ".join(community_addr)

        # 总价
        price = house.xpath(".//p[@class='property-price-total']//text()")
        data["price"] = "".join(price)

        # 每平米均价
        data["avg_price"] = house.xpath(".//p[@class='property-price-average']//text()")[0]

        # 链接
        data["url"] = house.xpath(".//a[@class='property-ex']/@href")[0]
        print(data['title'])
        # 把这条数据存入数据库内
        # save_data()

        time.sleep(1)
