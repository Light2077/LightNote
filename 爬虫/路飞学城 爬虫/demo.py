import requests

url = "http://www.baidu.com"
resp = requests.get(url)
cookies = resp.cookies

