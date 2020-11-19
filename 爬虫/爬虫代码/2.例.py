import requests
url = 'https://www.amazon.cn/dp/B07D429Z8D'
try:
    kv = {'user-agent': 'Mozilla/5.0'}
    r = requests.get(url)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    print(r.text[1000:2000])
except:
    print('爬取失败')


