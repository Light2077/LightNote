ipv6

```python
import requests
ipv6 = '240e:445:1e06:67f:d48d:2960:3c6b:f486'
resp = requests.get(f'http://ip.zxinc.org/api.php?type=json&ip={ipv6}')
resp.json()
```

```json
{'code': 0,
 'data': {'myip': '2409:8934:7090:3721:85e7:38c8:2759:ac84',
  'ip': {'query': '240e:445:1e06:67f:d48d:2960:3c6b:f486',
   'start': '',
   'end': ''},
  'location': '中国\t山东省\t枣庄市\t峄城区 中国电信\t无线基站网络',
  'country': '中国\t山东省\t枣庄市\t峄城区',
  'local': '中国电信\t无线基站网络'}}
```

