import asyncio
import random

async def consumer(queue, id):
    print(id, 'start')
    while True:
        val = await queue.get()
        queue.task_done()   # indicate complete task
        print('{} get a val: {}'.format(id, val))
        if id == 'consumer_2':
            a = b
        await asyncio.sleep(1)
        

async def producer(queue, id):
    for i in range(5):
        val = random.randint(1, 10)
        await asyncio.sleep(1)
        await queue.put(val)
        print('{} put a val: {}'.format(id, val))


async def main():
    queue = asyncio.Queue()

    # producer_1 = producer(queue, 'producer_1')
    # producer_2 = producer(queue, 'producer_2')
    await queue.put(1)
    await queue.put(3)
    await queue.put(2)
    consumer_1 = asyncio.create_task(consumer(queue, 'consumer_1'))
    consumer_2 = asyncio.create_task(consumer(queue, 'consumer_2'))

    # await asyncio.gather(*[producer_1, producer_2], return_exceptions=True)
    await queue.join()  # wait until the consumer has processed all items
    # consumer_1.cancel()
    # consumer_2.cancel()
    
asyncio.run(main())