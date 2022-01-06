> 前置知识：
>
> - 什么是websocket

django默认不支持websocket，需要下载依赖库

在Django部署的时候，通常使用的都是WSGI（Web Server Gateway Interface）既通用服务网关接口，该协议仅用来处理 Http 请求，更多关于WSGI的说明请参见[廖雪峰博客](https://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001386832689740b04430a98f614b6da89da2157ea3efe2000)。

当网址需要加入 WebSocket 功能时，WSGI 将不再满足我们的需求，此时我们需要使用ASGI既异步服务网关接口，该协议能够用来处理多种通用协议类型，包括HTTP、HTTP2 和 WebSocket，更多关于 ASGI 的说明请参见[此处](https://blog.ernest.me/post/asgi-draft-spec-zh)。

# 配置channels

https://channels.readthedocs.io/en/stable/installation.html

注此处django为3.1版本，如果是django2.2可能会有错，具体参考上面的文档

1. 下载channels

   ```
   python -m pip install -U channels
   ```

2. 修改`settings.py`

   ```python
   # 注册channles应用
   INSTALLED_APPS = [
       ...
       'channels'
   ]
   ```

3. 修改项目的`asgi.py`文件，假设项目名为mysite，这个文件就在`mysite/asgi.py`

   原本的文件是这样的

   ```python
   import os
   
   from django.core.asgi import get_asgi_application
   
   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
   
   application = get_asgi_application()
   ```

   新的文件

   ```python
   import os
   
   from channels.routing import ProtocolTypeRouter
   from django.core.asgi import get_asgi_application
   
   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
   
   application = ProtocolTypeRouter({
       "http": get_asgi_application(),
       # Just HTTP for now. (We can add other protocols later.)
   })
   ```

4. 设置`settings.py`

   ```python
   ASGI_APPLICATION = "mysite.asgi.application"
   ```

   

# 基于websocket的聊天室例子

https://channels.readthedocs.io/en/stable/tutorial/index.html

参考了https://www.cnblogs.com/guapitomjoy/p/12381293.html



channels文档提供了一个例子教你怎么做一个简单的聊天室

一共有两个页面：

- index页面：输入聊天室的名称以加入聊天室
- room页面：在房间里聊天

room页面将使用WebSocket与Django服务器通信，并监听任何发布的消息。

>版本需求：Channels 3.0 Python 3.6+ Django 2.2+
>
>软件需求：安装了redis

## 1 基础设置

### 创建项目

```
django-admin startproject mysite
```

此时的目录如下

```
mysite/
    manage.py
    mysite/
        __init__.py
        asgi.py
        settings.py
        urls.py
        wsgi.py
```

### 创建chat app

```
python manage.py startapp chat
```

此时目录如下

```
chat/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    views.py
```

在这个项目里，只用到了`__init__.py`和`view.py`这两个文件，其他都可以删了。

所以现在的情况是

```
chat/
    __init__.py
    views.py
```

在`mysite/settings.py`中注册`chat`app

```python
# mysite/settings.py
INSTALLED_APPS = [
	...
    'chat',
]
```

### 增加index页面

在`chat/`目录下创建一个`templates`目录用来存放所需页面

```python
chat/
    __init__.py
    templates/
        chat/
            index.html
    views.py
```

创建`chat/templates/chat/index.html`，并写入如下代码

```html
<!-- chat/templates/chat/index.html -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <title>Chat Rooms</title>
</head>
<body>
    What chat room would you like to enter?<br>
    <input id="room-name-input" type="text" size="100"><br>
    <input id="room-name-submit" type="button" value="Enter">

    <script>
        document.querySelector('#room-name-input').focus();
        document.querySelector('#room-name-input').onkeyup = function(e) {
            if (e.keyCode === 13) {  // enter, return
                document.querySelector('#room-name-submit').click();
            }
        };

        document.querySelector('#room-name-submit').onclick = function(e) {
            var roomName = document.querySelector('#room-name-input').value;
            window.location.pathname = '/chat/' + roomName + '/';
        };
    </script>
</body>
</html>
```

在`chat/views.py`文件中

```python
# chat/views.py
from django.shortcuts import render

def index(request):
    return render(request, 'chat/index.html')
```

创建`chat/urls.py`

```python
# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

在`mysite/urls.py`中

```python
# mysite/urls.py
from django.conf.urls import include
from django.urls import path
from django.contrib import admin

urlpatterns = [
    path('chat/', include('chat.urls')),
    path('admin/', admin.site.urls),
]
```

启动服务器

```
python manage.py runserver
```

访问http://127.0.0.1:8000/chat/看看能否出现页面

此时的chat app的文件目录应该是

```
chat/
    __init__.py
    templates/
        chat/
            index.html
            room.html
    urls.py
    views.py
```



### 使用channels库

参考本文第一部分：**配置channels**

## 实现聊天服务器

创建room页面`chat/templates/chat/room.html`

```html
<!-- chat/templates/chat/room.html -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <title>Chat Room</title>
</head>
<body>
    <textarea id="chat-log" cols="100" rows="20"></textarea><br>
    <input id="chat-message-input" type="text" size="100"><br>
    <input id="chat-message-submit" type="button" value="Send">
    {{ room_name|json_script:"room-name" }}
    <script>
        const roomName = JSON.parse(document.getElementById('room-name').textContent);

        const chatSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/chat/'
            + roomName
            + '/'
        );

        chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            document.querySelector('#chat-log').value += (data.message + '\n');
        };

        chatSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };

        document.querySelector('#chat-message-input').focus();
        document.querySelector('#chat-message-input').onkeyup = function(e) {
            if (e.keyCode === 13) {  // enter, return
                document.querySelector('#chat-message-submit').click();
            }
        };

        document.querySelector('#chat-message-submit').onclick = function(e) {
            const messageInputDom = document.querySelector('#chat-message-input');
            const message = messageInputDom.value;
            chatSocket.send(JSON.stringify({
                'message': message
            }));
            messageInputDom.value = '';
        };
    </script>
</body>
</html>
```

修改`chat/views.py`

```python
# chat/views.py
from django.shortcuts import render

def index(request):
    return render(request, 'chat/index.html', {})

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })
```

创建路由

```python
# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
]
```

Go to http://127.0.0.1:8000/chat/ 

现在可以进入房间，只不过发送聊天信息是没有效果的

### 创建consumer

当Django接受一个HTTP请求时，它会咨询根URLconf来查找一个视图函数，然后调用view函数来处理这个请求。类似地，当通道接受WebSocket连接时，它会咨询根路由配置来查找消费者，然后调用消费者上的各种函数来处理来自连接的事件。

接下来会教你写一个基础的consumer，在`/ws/chat/ROOM_NAME`接收websocket连接请求。

> 使用`/ws/`作为区分websocket和http请求的前缀。

创建`chat/consumers.py`

现在的目录为

```
chat/
    __init__.py
    consumers.py
    templates/
        chat/
            index.html
            room.html
    urls.py
    views.py
```

复制代码到`chat/consumers.py`

```python
# chat/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))

```

这是一个同步的WebSocket消费者，它接受所有的连接，从它的客户端接收消息，并将这些消息回传给同一个客户端。目前，它不会向同一房间的其他客户端广播消息。

> 
>
> Channels还支持编写异步消费者以获得更好的性能。然而，任何异步使用者都必须小心避免直接执行阻塞操作，比如访问Django模型。有关写入异步使用者的更多信息，请参阅[Consumers](https://channels.readthedocs.io/en/stable/topics/consumers.html) 。

类似于`urls.py`还需要创建`routing.py`

```
chat/
    __init__.py
    consumers.py
    routing.py  # new
    templates/
        chat/
            index.html
            room.html
    urls.py
    views.py
```

在`chat/routing.py`写入如下代码

```python
# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
```

- `as_asgi()`类似于`as_view()`为了得到一个为每个用户连接实例化我们的消费者实例的asgi应用程序。

修改`mysite/asgi.py`

```python
# mysite/asgi.py
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import chat.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
```

此根路由配置指定在与Channels开发服务器建立连接时，ProtocolTypeRouter将首先检查连接的类型。 如果是WebSocket连接（ws：//或wss：//），则该连接将分配给AuthMiddlewareStack。

AuthMiddlewareStack将用当前认证用户的引用填充连接的作用域，类似于Django的

AuthenticationMiddleware用当前认证用户填充view函数的request对象。(范围将在本教程的后面讨论。)然后连接将被给予URLRouter。

URLRouter将根据提供的url模式检查连接的HTTP路径，以将其路由到特定使用者。

让我们验证`/ws/chat/<ROOM_NAME>/`路径的consumer是否可以使用。 运行迁移以应用数据库更改（Django的会话框架需要数据库），然后启动Channels开发服务器：

```
python manage.py migrate
```

迁移以后启动服务器进行测试，现在可以自言自语了。

## Enable a channel layer

信道层是一种通信系统。它允许多个消费者实例相互通信，并与Django的其他部分通信。

- channel 可以理解为信箱，大家都可以往这个信箱里发信息。每个channel都有自己的名字，只要知道这个channel的名字，其他人就可以给channel发信箱。
- group是channel的集合，一个group也有名字，任何人只要有group的名字，就根据channel的名字往group里增加或移除channel，也可以给这个组里的所有channel发信息。但是不能知道这个组的所有channel的名字。

每个consumer实例都有一个自动分配的唯一channel名，因此可以通过信道层进行通信

在chat app中，为了通信，我们需要有很多个在同一个房间的`ChatConsumer`实例。

为此，我们将让每个`ChatConsumer`将其channel添加到以房间名称为基础的group中。这将允许聊天用户向同一房间的所有其他聊天用户传递消息。

接下来会建立一个channel层，用redis作为后端存储数据库。

需要安装`channels_redis`

```python
python -m pip install channels_redis
```

还需要在`mysite/settings.py`中配置

```python
# mysite/settings.py
# Channels
ASGI_APPLICATION = 'mysite.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
```



测试是否构建成功，一下语句执行成功即可

```
python manage.py shell
>>> import channels.layers
>>> channel_layer = channels.layers.get_channel_layer()
>>> from asgiref.sync import async_to_sync
>>> async_to_sync(channel_layer.send)('test_channel', {'type': 'hello'})
>>> async_to_sync(channel_layer.receive)('test_channel')
{'type': 'hello'}
```



修改`chat/consumers.py`文件

```python
# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
```

当一个用户发送消息时，javascript函数会把信息通过WebSocket发送给ChatConsumer。然后ChatConsumer将会收到该信息，并将信息转发到与房间名称对应的组里。每个在同一个房间的ChatConsumer都会收到这条消息。

- `self.scope['url_route']['kwargs']['room_name']`
  - 通过WebSocket的url路由获取房间名称
  - 每个consumer都有个包含关于自身连接信息的 [scope](https://channels.readthedocs.io/en/stable/topics/consumers.html#scope) 属性
- `self.room_group_name = 'chat_%s' % self.room_name`
  - 直接从用户指定的房间名构造channels group名，不使用任何引号或转义。
  - 组名只能包含字母、数字、下划线以及periods(？)
- `async_to_sync(self.channel_layer.group_add)(...)`
  - 加入一个组
  - 需要使用async to sync()包装器，因为ChatConsumer是一个同步WebsocketConsumer，但它调用的是一个异步通道层方法。(所有的通道层方法都是异步的。)
- `self.accept()`
  - 接受WebSocket连接
  - 如果你没有使用connect() 调用accept()方法，这个连接会被拒绝并关闭。如果用户没有权限进入这个组，就可能会拒绝。
  - 如果您选择接受连接，建议将accept()作为connect()中的最后一个操作调用。
- `async_to_sync(self.channel_layer.group_discard)(...)`
  - 离开一个组
- `async_to_sync(self.channel_layer.group_send)`
  - 将事件发送到组。
  - 事件有一个特殊的“type”键，对应于应该在接收事件的消费者上调用的方法名称。

至此，一个可以聊天的聊天室就建好了。

## 异步聊天服务器

https://channels.readthedocs.io/en/stable/tutorial/part_3.html

官方说主要是为了提高性能，这个提高性能怎么理解呢？

### 重写consumer

我们编写的ChatConsumer当前处于同步状态。 同步consumer很方便，因为他们可以调用常规的同步I / O函数，例如无需编写特殊代码即可访问Django模型的函数。 但是，异步使用者可以提供更高的性能，因为它们在处理请求时不需要创建其他线程。

ChatConsumer仅使用python原生的async库（通道和通道层），尤其是它不访问同步Django模型。 因此，可以将其重写为异步的，而不会带来复杂性。

修改`chat/consumers.py`

```python
# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                # 相当于给chat_message这个函数发消息，会调用该函数
                'type': 'chat_message',  
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
```

- ChatConsumer现在继承AsyncWebsocketConsumer
- 定义函数方式变了，多了个`async`前缀
- await用于调用执行I/O的异步函数。
- 在通道层上调用方法时，不再需要async_to_sync包裹方法