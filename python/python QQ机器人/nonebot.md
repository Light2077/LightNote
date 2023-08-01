创建一个虚拟环境并激活

```
python -m venv .venv
source .venv/bin/activate
```

安装pipx

```
pip install pipx
```

```
pipx ensurepath
```

安装脚手架

```
pipx install nb-cli
```

创建项目

```
nb create
```

填写项目基本信息

```
Project Name: awesome-bot
```

### 依赖注入的概念理解

[获取事件信息 | NoneBot (baka.icu)](https://nb2.baka.icu/docs/tutorial/event-data)

> 就是在类外创建类

依赖注入（Dependency Injection，简称 DI）是一种设计模式，主要用于降低软件组件之间的耦合度。依赖注入允许将一个对象的依赖项（通常是其他对象或服务）通过外部方式（例如函数参数或属性）提供给它，而不是在对象内部创建。这使得对象更加灵活、可复用和可测试。

在上面提到的 NoneBot 文档中，依赖注入用于获取事件处理流程中的上下文信息。通过依赖注入，你可以在事件处理函数中按需获取所需的上下文信息，而不是硬编码依赖关系。这使得代码更加灵活和可维护。

以文档中的示例为例，要实现一个天气查询功能，你可能需要根据用户提供的地名参数返回相应的天气信息。在这个示例中，依赖注入允许你在事件处理函数中获取用户提供的地名参数（通过 CommandArg()），并据此执行相应的逻辑。

具体来说，在这个示例中，依赖注入的使用方法如下：

1. 在事件处理函数的参数中声明所需的依赖（在这个例子中是 CommandArg()）。
2. 确保函数被正确添加为事件处理依赖。
3. 在函数体中，通过依赖注入的参数（在这个例子中是 args）访问所需的上下文信息。

这种做法的优点在于，你可以根据需要灵活地添加或删除依赖项，而不会影响其他部分的代码。这使得代码更容易维护和测试。

总之，依赖注入是一种编程方法，用于降低代码组件之间的耦合度，提高代码的可维护性和可测试性。在 NoneBot 中，依赖注入用于按需获取事件处理流程中的上下文信息。



以下是一个简化的例子，用于演示使用依赖注入和不使用依赖注入的代码差异。

假设我们有一个简单的应用程序，该应用程序可以将消息发送给用户。我们有一个 `MessageSender` 类，它有一个 `send` 方法，用于将消息发送给用户。我们还有一个 `User` 类，它有一个 `notify` 方法，用于通知用户。

不使用依赖注入的代码示例：

```python
class EmailSender:
    def send(self, message):
        print(f"Sending email: {message}")

class User:
    def __init__(self, name):
        self.name = name
        self.message_sender = EmailSender()

    def notify(self, message):
        self.message_sender.send(message)

user = User("Alice")
user.notify("Hello, Alice!")

```

在这个例子中，`User` 类直接创建了一个 `EmailSender` 实例。这导致了紧密耦合，如果我们想要改变发送消息的方式（例如使用短信而不是电子邮件），我们需要修改 `User` 类的代码。

现在让我们看一个使用依赖注入的代码示例：

```python
class EmailSender:
    def send(self, message):
        print(f"Sending email: {message}")

class SmsSender:
    def send(self, message):
        print(f"Sending SMS: {message}")

class User:
    def __init__(self, name, message_sender):
        self.name = name
        self.message_sender = message_sender

    def notify(self, message):
        self.message_sender.send(message)

email_sender = EmailSender()
sms_sender = SmsSender()

# 使用 EmailSender
user1 = User("Alice", email_sender)
user1.notify("Hello, Alice!")

# 使用 SmsSender
user2 = User("Bob", sms_sender)
user2.notify("Hello, Bob!")
	
```

在这个例子中，我们使用依赖注入将 `MessageSender` 实例作为参数传递给 `User` 类。这使得 `User` 类与特定的消息发送方式解耦，使得代码更加灵活和可维护。我们可以在不修改 `User` 类的情况下，轻松地切换消息发送方式（例如使用短信而不是电子邮件）。

通过比较这两个示例，你可以看到使用依赖注入的代码更加灵活和可维护，因为它降低了代码组件之间的耦合度。

使用了依赖注入的Nonebot代码示例





其中

```python
handle_function(args: Message = CommandArg())
```

表示：

`args` 参数的预期类型是 `Message`。默认值是 `CommandArg()`。