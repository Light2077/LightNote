官网：[go-cqhttp 帮助中心](https://docs.go-cqhttp.org/)

> 🚨现在，在用go-cqhttp登录前需要先搞一个数字签名的东西，否则可能会被封号
>
> [fuqiuluo/unidbg-fetch-qsign: 获取QQSign通过Unidbg (github.com)](https://github.com/fuqiuluo/unidbg-fetch-qsign)
>
> 使用docker的部署方案会比较简单
>
> [部署在Docker · fuqiuluo/unidbg-fetch-qsign Wiki (github.com)](https://github.com/fuqiuluo/unidbg-fetch-qsign/wiki/部署在Docker)

安装和基础见官网，该笔记仅记录重点内容。

# 配置

## 启动配置

`config.yml`的关键配置

- 配置账号密码
- 配置`sign-server`
- 配置正向ws服务器

```yml
  # 正向WS设置
  - ws:
      # 正向WS服务器监听地址
      address: 0.0.0.0:8080
      middlewares:
        <<: *default # 引用默认中间件
```

注：go-cqhttp 配置文件可以使用占位符来读取**环境变量**的值。

```yml
account: # 账号相关
  uin: ${CQ_UIN} # 读取环境变量 CQ_UIN
  password: ${CQ_PWD:123456} # 当 CQ_PWD 为空时使用默认值 123456
```

## 过滤器配置

常用配置

只上报私聊或特定群组的非匿名消息

更多进阶语法请参考[GJSON语法](https://github.com/tidwall/gjson/blob/master/SYNTAX.md)

```json
{
    ".or": [
        {
            "message_type": "private"
        },
        {
            "message_type": "group",
            "group_id": {
                ".in": [
                    123456
                ]
            },
            "anonymous": {
                ".eq": null
            }
        }
    ]
}
```



# 使用aiohttp

部署好机器人后编写如下代码

```python
import json
import asyncio
import aiohttp

# 配置基本信息
WS_URL = "ws://127.0.0.1:8090"

# 发送群聊消息
async def send_group_msg(ws, group_id, message):
    data = {
        "action": "send_group_msg",
        "params": {'group_id': group_id, 'message': message}
    }
    await ws.send_str(json.dumps(data))
    
async def main():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(WS_URL) as ws:
            await send_group_msg(ws, 123456, "确实")

if __name__ == "__main__":
    asyncio.run(main())
```

# 使用nonebot2



## 配置

首先cqhttp要配置反向ws

```yml
  - ws-reverse:
      # 反向WS Universal 地址
      # 注意 设置了此项地址后下面两项将会被忽略
      universal: ws://127.0.0.1:8070/onebot/v11/ws
      # 反向WS API 地址
      api: ws://your_websocket_api.server
      # 反向WS Event 地址
      event: ws://your_websocket_event.server
      # 重连间隔 单位毫秒
      reconnect-interval: 3000
      middlewares:
        <<: *default # 引用默认中间件
```



在虚拟环境下使用

```
conda activate qqbot
```



[快速上手 | NoneBot (baka.icu)](https://nb2.baka.icu/docs/quick-start)

安装必要的工具

安装pipx

```
python -m pip install --user pipx
python -m pipx ensurepath
```

安装脚手架

```
pipx install nb-cli
```

创建项目

```
nb create
```

协议选[one-botv11](https://onebot.dev/)

创建插件目录

```
|- plugins
  |- demo.py
```

编写插件内容 `demo.py`

```python
from nonebot import on_command

确实 = on_command("确实")

@确实.handle()
async def handle_function():
    await 确实.finish("确实")
```



在项目目录下创建一个主文件`bot.py`

```python
import nonebot
from nonebot.adapters import onebot

# 初始化 NoneBot
nonebot.init()

# 注册适配器
driver = nonebot.get_driver()
driver.register_adapter(onebot.v11.Adapter)

# 在这里加载插件
nonebot.load_builtin_plugins("echo")  # 内置插件
nonebot.load_plugins("bot-demo/plugins")  # 本地插件

if __name__ == "__main__":
    nonebot.run()
```



配置 `.env`

```
HOST = 127.0.0.1
PORT = 8070
```

运行项目

```
nb run
```





如何安装新依赖包

激活虚拟环境

```
source ./venv/bin/activate	
```

安装包即可

> 应该不是推荐的方案



bot的api参考

[nonebot.adapters.onebot.v11.bot | NoneBot](https://onebot.adapters.nonebot.dev/docs/api/v11/bot/#Bot-send_group_msg)

