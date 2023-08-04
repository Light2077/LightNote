官网：[go-cqhttp 帮助中心](https://docs.go-cqhttp.org/)

> 🚨现在，在用go-cqhttp登录前需要先搞一个数字签名的东西，否则可能会被封号
>
> [fuqiuluo/unidbg-fetch-qsign: 获取QQSign通过Unidbg (github.com)](https://github.com/fuqiuluo/unidbg-fetch-qsign)
>
> 使用docker的部署方案会比较简单
>
> [部署在Docker · fuqiuluo/unidbg-fetch-qsign Wiki (github.com)](https://github.com/fuqiuluo/unidbg-fetch-qsign/wiki/部署在Docker)

安装和基础见官网，该笔记仅记录重点内容。

# 配置cqhttp

下载好go-cqhttp后，在启动前需要先配置两个文件：

- `config.yml`
- `filter.json`

## config.yml

`config.yml`的关键配置

- 配置账号密码
- 配置`sign-server`
- 配置事件过滤文件的路径
- 配置正向ws服务器
- 配置反向ws服务器

### 配置账号密码

```yml
account: # 账号相关
  uin: 123456789 # QQ账号
  password: '123456' # 密码为空时使用扫码登录
```

注：go-cqhttp 配置文件可以使用占位符来读取**环境变量**的值。

```yml
account: # 账号相关
  uin: ${CQ_UIN} # 读取环境变量 CQ_UIN
  password: ${CQ_PWD:123456} # 当 CQ_PWD 为空时使用默认值 123456
```



### 配置`sign-server`

```yml
account: # 账号相关
  # ...
  # 数据包的签名服务器
  # 兼容 https://github.com/fuqiuluo/unidbg-fetch-qsign
  # 如果遇到 登录 45 错误, 或者发送信息风控的话需要填入一个服务器
  # 示例:
  # sign-server: 'http://127.0.0.1:8080' # 本地签名服务器
  # sign-server: 'https://signserver.example.com' # 线上签名服务器
  # 服务器可使用docker在本地搭建或者使用他人开放的服务
  sign-server: 'http://127.0.0.1:8080'
```

### 配置事件过滤文件的路径

```yml
# 默认中间件锚点
default-middlewares: &default
  # ...
  # 事件过滤器文件目录
  filter: 'myfilter.json'
```

### 配置正向ws服务器

正向ws服务器的作用是，我们可以主动发送 ws 请求到这个地址，让机器人去执行对应的行为。

```yml
 servers:
  # 正向WS设置
  - ws:
      # 正向WS服务器监听地址
      address: 127.0.0.1:8090
      middlewares:
        <<: *default # 引用默认中间件
```

### 配置反向ws服务器

反向ws服务的作用是可以连接到nonebot2等框架。

这里演示的地址是用于适配nonebot2的。

```yml
# 连接服务列表
servers:
  # ...
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

### 完整的config.yml样例

```yml
# go-cqhttp 默认配置文件

account: # 账号相关
  uin: 123456 # QQ账号
  password: '123123' # 密码为空时使用扫码登录
  encrypt: false  # 是否开启密码加密
  status: 0      # 在线状态 请参考 https://docs.go-cqhttp.org/guide/config.html#在线状态
  relogin: # 重连设置
    delay: 3   # 首次重连延迟, 单位秒
    interval: 3   # 重连间隔
    max-times: 0  # 最大重连次数, 0为无限制

  # 是否使用服务器下发的新地址进行重连
  # 注意, 此设置可能导致在海外服务器上连接情况更差
  use-sso-address: true
  # 是否允许发送临时会话消息
  allow-temp-session: false

  # 数据包的签名服务器
  # 兼容 https://github.com/fuqiuluo/unidbg-fetch-qsign
  # 如果遇到 登录 45 错误, 或者发送信息风控的话需要填入一个服务器
  # 示例:
  # sign-server: 'http://127.0.0.1:8080' # 本地签名服务器
  # sign-server: 'https://signserver.example.com' # 线上签名服务器
  # 服务器可使用docker在本地搭建或者使用他人开放的服务
  sign-server: 'http://127.0.0.1:8080'

heartbeat:
  # 心跳频率, 单位秒
  # -1 为关闭心跳
  interval: 5

message:
  # 上报数据类型
  # 可选: string,array
  post-format: string
  # 是否忽略无效的CQ码, 如果为假将原样发送
  ignore-invalid-cqcode: false
  # 是否强制分片发送消息
  # 分片发送将会带来更快的速度
  # 但是兼容性会有些问题
  force-fragment: false
  # 是否将url分片发送
  fix-url: false
  # 下载图片等请求网络代理
  proxy-rewrite: ''
  # 是否上报自身消息
  report-self-message: false
  # 移除服务端的Reply附带的At
  remove-reply-at: false
  # 为Reply附加更多信息
  extra-reply-data: false
  # 跳过 Mime 扫描, 忽略错误数据
  skip-mime-scan: false
  # 是否自动转换 WebP 图片
  convert-webp-image: false
  # http超时时间
  http-timeout: 0

output:
  # 日志等级 trace,debug,info,warn,error
  log-level: warn
  # 日志时效 单位天. 超过这个时间之前的日志将会被自动删除. 设置为 0 表示永久保留.
  log-aging: 15
  # 是否在每次启动时强制创建全新的文件储存日志. 为 false 的情况下将会在上次启动时创建的日志文件续写
  log-force-new: true
  # 是否启用日志颜色
  log-colorful: true
  # 是否启用 DEBUG
  debug: false # 开启调试模式

# 默认中间件锚点
default-middlewares: &default
  # 访问密钥, 强烈推荐在公网的服务器设置
  access-token: ''
  # 事件过滤器文件目录
  filter: 'myfilter.json'
  # API限速设置
  # 该设置为全局生效
  # 原 cqhttp 虽然启用了 rate_limit 后缀, 但是基本没插件适配
  # 目前该限速设置为令牌桶算法, 请参考:
  # https://baike.baidu.com/item/%E4%BB%A4%E7%89%8C%E6%A1%B6%E7%AE%97%E6%B3%95/6597000?fr=aladdin
  rate-limit:
    enabled: false # 是否启用限速
    frequency: 1  # 令牌回复频率, 单位秒
    bucket: 1     # 令牌桶大小

database: # 数据库相关设置
  leveldb:
    # 是否启用内置leveldb数据库
    # 启用将会增加10-20MB的内存占用和一定的磁盘空间
    # 关闭将无法使用 撤回 回复 get_msg 等上下文相关功能
    enable: true
  sqlite3:
    # 是否启用内置sqlite3数据库
    # 启用将会增加一定的内存占用和一定的磁盘空间
    # 关闭将无法使用 撤回 回复 get_msg 等上下文相关功能
    enable: false
    cachettl: 3600000000000 # 1h

# 连接服务列表
servers:
  # 添加方式，同一连接方式可添加多个，具体配置说明请查看文档
  #- http: # http 通信
  #- ws:   # 正向 Websocket
  #- ws-reverse: # 反向 Websocket
  #- pprof: #性能分析服务器
  # 正向WS设置
  - ws:
      # 正向WS服务器监听地址
      address: 127.0.0.1:8090
      middlewares:
        <<: *default # 引用默认中间件
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



## 事件过滤配置

事件过滤配置对应`config.yml`中的事件过滤文件的路径，文件名要一致

```yml
# 默认中间件锚点
default-middlewares: &default
  # ...
  # 事件过滤器文件目录
  filter: 'myfilter.json'
```

常用配置如下，效果为：

- 上报私人消息
- **或**指定的群的非匿名消息

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

其他示例参考：[事件过滤器 | go-cqhttp 帮助中心](https://docs.go-cqhttp.org/guide/eventfilter.html#示例)

更多进阶语法请参考[GJSON语法](https://github.com/tidwall/gjson/blob/master/SYNTAX.md)

# 使用aiohttp

部署好机器人后编写如下代码

```python
import json
import asyncio
import aiohttp

# 配置基本信息
GROUP_ID = 123456
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
            await send_group_msg(ws, GROUP_ID, "确实")

if __name__ == "__main__":
    asyncio.run(main())
```

在`GROUP_ID`处填写你要发送测试消息的群，就会在对应的群发送一个“确实”

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

