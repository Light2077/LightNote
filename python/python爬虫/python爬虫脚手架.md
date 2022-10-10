# 脚手架

```python

import requests
import time
from lxml import etree
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                  ' (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'
}

page = 3 # 第几页
url = f'https://nj.ke.com/xiaoqu/jianye/pg{page}/'

resp = requests.get(url, headers=headers)
root = etree.HTML(resp.text)
tags = root.xpath('//a[@class="maidian-detail"]/@title')
for t in tags:
    print(t)
```

