https://websockets.readthedocs.io/en/stable/intro.html

关于协程

- https://realpython.com/async-io-python/
- https://medium.com/@jimmy_huang/python-asyncio-%E5%8D%94%E7%A8%8B-d84b5b945b5b
- https://ithelp.ithome.com.tw/articles/10199408

# 简单例子

简单构建一个基于websocket的服务端，当收到包含姓名的消息时，会自动对该姓名打招呼。

创建`server.py`

```python
# server.py
import asyncio
import websockets

async def hello(websocket, path):
    name = await websocket.recv()
    print(f"< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f"> {greeting}")

start_server = websockets.serve(hello, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
```

构建与之对应的客户端

输入名字就能得到客户端的回复

```python
# client.py
import asyncio
import websockets

async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        name = input("What's your name? ")

        await websocket.send(name)
        print(f"> {name}")

        greeting = await websocket.recv()
        print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())
```

