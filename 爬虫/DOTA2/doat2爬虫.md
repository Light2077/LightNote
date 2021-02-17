https://dev.dota2.com/forum/dota-2/spectating/replays/webapi/48733-dota-2-match-history-webapi

https://wiki.teamfortress.com/wiki/WebAPI#Dota_2

https://blog.csdn.net/lv19980523/article/details/82156259

https://zhuanlan.zhihu.com/p/36776967



超强：

https://docs.opendota.com/#section/Introduction

https://api.opendota.com/api/matches/3903099199

https://api.opendota.com/api//players/137867515

## 您的 Steam 网页 API 密钥

密钥: C3C004D7995CE21FCCDFA669A6EEFE17

域名名称: light2077

首先要登录steam获得开发者key

http://steamcommunity.com/dev/apikey

```python
import requests
url = "https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/" \
      "?key=C3C004D7995CE21FCCDFA669A6EEFE17"
proxies = {'http': 'http://127.0.0.1:4780' , 'https': 'http://127.0.0.1:4780'}
res = requests.get(url, proxies=proxies)
print(res.json())
```

这就是最简单的获取比赛数据的方法

会获取100场比赛的简洁

### 获取单场比赛详细数据

```python
import requests
match_id = "27110133"
key = "C3C004D7995CE21FCCDFA669A6EEFE17"
url = "https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?match_id=%s&key=%s" % (match_id, key)
proxies = {'http': 'http://127.0.0.1:4780' , 'https': 'http://127.0.0.1:4780'}
res = requests.get(url, proxies=proxies)
print(res.json())

```

英雄id在这个文件夹下查找：·`dota/scripts/npc/npc_heroes.txt `

