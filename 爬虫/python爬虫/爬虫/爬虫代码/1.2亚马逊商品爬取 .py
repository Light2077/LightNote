import requests
url = 'https://www.amazon.cn/dp/B07D429Z8D'
try:
    kv = { 'user-agent': 'Mozilla/5.0' }
    r = requests.get(url, headers = kv) # 模拟浏览器
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    print(r.text[0:1000])
except:
    print('爬取失败')

#更改用户访问头文件
#kv = {'user-agent': 'Mozilla/5.0'}
#r = requests.get(url, headers = kv)
#r.request.headers # 查看user-agent
