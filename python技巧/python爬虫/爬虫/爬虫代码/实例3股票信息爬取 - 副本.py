#CrawBaiduStocksA.py
import requests
from bs4 import BeautifulSoup
import traceback
import re
import os

def getStockList(lst, stockURL):
    html = getHTMLText(stockURL,'GB2312')
    soup = BeautifulSoup(html, 'html.parser') 
    a = soup.find_all('a')
    for i in a:
        try:
            href = i.attrs['href']
            lst.append(re.findall(r"[s][hz]\d{6}", href)[0])
        except:
            continue
 
def getStockInfo(lst, stockURL, fpath):
    for stock in lst:
        url = stockURL + stock + ".html"
        html = getHTMLText(url)
        try:
            if html=="":
                continue
            infoDict = {}     #用于存储当前页面的个股信息
            soup = BeautifulSoup(html, 'html.parser')

            #股票信息所在页面
            stockInfo = soup.find('div',attrs={'class':'stock-bets'})
            #股票名称
            name = stockInfo.find_all(attrs={'class':'bets-name'})[0]
            #将信息增加到字典中
            infoDict.update({'股票名称': name.text.split()[0]})

            #找到所有相关信息。
            keyList = stockInfo.find_all('dt')
            valueList = stockInfo.find_all('dd')
            for i in range(len(keyList)):
                key = keyList[i].text
                val = valueList[i].text
                infoDict[key] = val#直接向字典中新增内容
             
            with open(fpath, 'a', encoding='utf-8') as f:
                f.write( str(infoDict) + '\n' )
        except:
            traceback.print_exc()#获得错误信息
            continue
def checkWebEncode(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        print('这个网站的apparent_encoding是'+r.apparent_encoding)
        print('这个网站的encoding是'+r.encoding)
    except:
        print('获取失败')

def test():
    url = 'http://www.oneone1.net/product/onitokatana/top.html'
    checkWebEncode(url)
#main()
#获得网页源代码
def getHTMLText(url, code='utf-8'):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return ""
#获得图片地址
def getImgUrlList(ImgUrlList, ImgSouce_url):
    try:
        html = getHTMLText(ImgSouce_url, code='utf-8')
        soup = BeautifulSoup(html, 'html.parser') 
        div = soup.find('div',id = 'graphic')
        url = div.find_all(attrs={'class':'sample'})
        for i in range(len(url)):
            ImgUrl = 'http://www.oneone1.net/product/onitokatana/'+url[i].attrs['href']
            ImgUrlList.append(ImgUrl)
            #url[0].img.attrs['src']
    except:
        print('?')
    return ''

#保存图片到指定文件夹
def saveImg(ImgList, output_file):
    root = output_file
    for url in ImgList:
        path = root + url.split('/')[-1]
        if not os.path.exists(root):
            os.mkdir(root)
        if not os.path.exists(path):
            
            r = requests.get(url)
            with open(path, 'wb') as f:
                f.write(r.content)
                f.close()
                print('文件保存成功')
        else:
            print('文件已存在')
    return ''

def main():
    ImgSouce_url = 'http://www.oneone1.net/product/onitokatana/top.html'
    output_file = 'D://picture//'
    ImgUrlList=[]
    getImgUrlList(ImgUrlList, ImgSouce_url)
    saveImg(ImgUrlList, output_file)
main()
