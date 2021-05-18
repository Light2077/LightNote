import asyncio


# 定义协程
async def get_html(url):
    print('get url: ', url)
    return url


def callback_func(task):
    print("success get: ", task.result())


# 获得协程对象
c = get_html("www.baidu.com")

# 创建事件循环对象
loop = asyncio.get_event_loop()
task = asyncio.ensure_future(c)

# 将回调函数绑定到任务对象中
task.add_done_callback(callback_func)
loop.run_until_complete(task)
