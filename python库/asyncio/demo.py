import time
from concurrent.futures import Future
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures.process import ProcessPoolExecutor

def func(value):
    time.sleep(1)
    print(value)
    
pool = ThreadPoolExecutor(max_workers=5)

for i in range(5):
    future = pool.submit(func, i)
    print(future)