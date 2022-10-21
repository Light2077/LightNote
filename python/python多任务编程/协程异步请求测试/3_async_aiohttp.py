## 3_async_aiohttp.py ##
import time
import asyncio
import aiohttp
import requests

async def get(i):
    print(time.strftime('%X'), 'start', i)
    async with aiohttp.ClientSession() as session:
        async with session.get('http://127.0.0.1:5000/') as response:
            html = await response.text()
    print(time.strftime('%X'), 'end', i)

async def main():
    tasks = [asyncio.create_task(get(i)) for i in range(4)]
    await asyncio.gather(*tasks)

asyncio.run(main())