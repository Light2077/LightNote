#!usr/bin/python
# -*- coding:utf8 -*-
import time
import random
import asyncio


async def consumer(queue, name):
    while True:
        val = await queue.get()
        print(f'{name} get a val: {val} at {time.strftime("%X")}')
        await asyncio.sleep(1)


async def producer(queue, name):
    for i in range(20):
        await queue.put(i)
        print(f'{name} put a val: {i}')
        await asyncio.sleep(0.1)


async def main():
    queue = asyncio.Queue()

    tasks = [asyncio.create_task(producer(queue, 'producer'))]
    for i in range(3):
        tasks.append(asyncio.create_task(consumer(queue, f'consumer_{i}')))

    # await asyncio.sleep(10)

    await asyncio.gather(*tasks, return_exceptions=True)


# start = time.perf_counter()
asyncio.run(main())
# end = time.perf_counter()
# print(end - start)
