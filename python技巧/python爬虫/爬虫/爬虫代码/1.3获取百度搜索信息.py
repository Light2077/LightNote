import requests
url = 'http://www.baidu.com/s' 
#url = 'http://www.so.com/s'  # 360搜索
keyword = 'Python'
try:
    kv = {'wd':keyword}
    #kv = {'q':keyword} # 360搜索的关键词
    r = requests.get(url, params = kv)
    print(r.request.url)
    r.raise_for_status()
    print(len(r.text))
except:
    print('爬取失败')


