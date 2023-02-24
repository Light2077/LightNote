## 2_async_requests.py ##
import time
import asyncio

import requests

async def get(i):
    print(time.strftime('%X'), 'start', i)
    resp = requests.get('http://127.0.0.1:5000/')
    print(time.strftime('%X'), 'end', i)
    
async def main():
    for i in range(4):
        asyncio.create_task(get(i))
        
asyncio.run(main())