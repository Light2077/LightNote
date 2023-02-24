## 1_threading_requests.py ##
import time
import threading

import requests

def get(i):
    print(time.strftime('%X'), 'start', i)
    resp = requests.get('http://127.0.0.1:5000/')
    print(time.strftime('%X'), 'end', i)

for i in range(4):
    threading.Thread(target=get, args=(i,)).start()