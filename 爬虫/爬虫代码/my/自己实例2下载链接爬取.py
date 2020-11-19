#CrawBaiduStocksA.py
import requests
from bs4 import BeautifulSoup
import re
import os
'''
url = 'https://blog.reimu.net/archives/26519'
r = requests.get(url)
print(r.status_code)
html = r.text
soup = BeautifulSoup(html, 'html.parser')
linka = soup(attrs={'href':re.compile('pan.baidu')})
'''

def getHTMLText(url, code='utf-8'):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return ""
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
#获得文章链接
def getArticlList(ArticlLinkList, all_articl_url):
    html = getHTMLText(all_articl_url, code='utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    all_url = soup.find_all('h2',attrs={'class':'entry-title'})
    for url in all_url:
        link = url.a.attrs['href']
        ArticlLinkList.append(link)
        
def saveDownloadLink(ArticlLinkList, all_download_link):
    p = re.compile(r'提取码.*[：:]+ *[a-zA-Z0-9]{4}')
    secret_code_p = re.compile(r'解压密码.*|解压码.*')
    for link in ArticlLinkList:
        html = getHTMLText(link, code='utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        downloaddiv = soup.find('pre')
        if downloaddiv == None:
            linka = soup(attrs={'href':re.compile('pan.baidu')})
            extract_code = linka[0].parent(string = re.compile(r'提取码'))[0]
            extract_code = p.findall(extract_code)[0]
            download_link = linka[0].attrs['href']
            try:
                secret_code = linka[0].parent(string = re.compile(r'解压密码'))[0]
                secret_code = secret_code_p.findall(secret_code)[0]
            except:
                secret_code = '无'
        else:
            try:
                download_link = downloaddiv.a.attrs['href']
                extract_code = downloaddiv(string = re.compile(r'提取码'))[0]
                extract_code = p.findall(extract_code)[0]
                try:    
                    secret_code = downloaddiv(string = re.compile(r'解压密码'))[0]
                    secret_code = secret_code_p.findall(secret_code)[0]
                except:
                    secret_code = '无'
            except:
                download_link = 'aaaaaa'
        print('成功爬取一个地址'+download_link+'\t'+extract_code+secret_code)
        all_download_link.append(download_link) 
        extract_code = 0
        
    pass
def main():
    all_articl_url = 'https://blog.reimu.net/archives/category/picture'
    output_file = 'D://picture//'
    ArticlLinkList=[]
    all_download_link = []
    print('获取文章地址')
    getArticlList(ArticlLinkList, all_articl_url)
    print('')
    saveDownloadLink(ArticlLinkList, all_download_link)
    for link in all_download_link:
        print(link)




def checkWebEncode(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        print('这个网站的apparent_encoding是'+r.apparent_encoding)
        print('这个网站的encoding是'+r.encoding)
    except:
        print('获取失败')
