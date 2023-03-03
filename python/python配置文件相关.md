个人的配置文件习惯，创建一个配置文件夹，在代码的上一级

然后代码中要有个`settings.py`文件

```
|-project_name
  |-project_code
    |-__init__.py
    |-main.py
    |-settings.py
  |-.config
    |-config.json
  |-.venv
  |-README.md
```

`settings.py`文件一般用来配置各种目录

加载时

```python
import os

SRC_DIR = os.path.dirname(__file__)  # 代码根目录
BASE_DIR = os.path.dirname(SRC_DIR)  # 项目根目录

# 配置文件夹 一般配置文件不多的话就只有一个config.json
CONFIG_DIR = os.path.dirname(BASE_DIR, ".config")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")
```



Python编程中常用的配置文件格式包括：

1. INI文件格式：INI文件是一种简单的文本文件格式，通常使用扩展名为".ini"。INI文件中包含了一系列的键值对，以节(section)的形式进行组织，例如：

```ini
[database]
host = localhost
port = 3306
username = root
password = password123
database = mydatabase
```

1. YAML文件格式：YAML是一种层次化的数据格式，通常使用扩展名为".yaml"或".yml"。YAML文件可以包含多个文档，每个文档以"---"分隔，例如：

```yaml
database:
  host: localhost
  port: 3306
  username: root
  password: password123
  database: mydatabase
```

1. JSON文件格式：JSON是一种轻量级的数据交换格式，通常使用扩展名为".json"。JSON文件中包含了一组键值对，以大括号和方括号进行组织，例如：

```json
{
  "database": {
    "host": "localhost",
    "port": 3306,
    "username": "root",
    "password": "password123",
    "database": "mydatabase"
  }
}
```

在Python中，可以使用ConfigParser模块来读取INI文件格式的配置文件，使用PyYAML或ruamel.yaml模块来读取YAML文件格式的配置文件，使用json模块来读取JSON文件格式的配置文件。这些模块提供了一些方法和类来方便地解析和读取配置文件中的键值对，例如：

读取INI文件格式的配置文件：

```python
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

host = config.get('database', 'host')
port = config.getint('database', 'port')
username = config.get('database', 'username')
password = config.get('database', 'password')
database = config.get('database', 'database')
```

读取YAML文件格式的配置文件：

```python
import yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

host = config['database']['host']
port = config['database']['port']
username = config['database']['username']
password = config['database']['password']
database = config['database']['database']
```

读取JSON文件格式的配置文件：

```python
import json

with open('config.json', 'r') as f:
    config = json.load(f)

host = config['database']['host']
port = config['database']['port']
username = config['database']['username']
password = config['database']['password']
database = config['database']['database']
```

需要注意的是，在读取配置文件时，应该检查文件是否存在，并且应该处理文件读取过程中可能出现的异常情况。



INI文件格式详细案例

```ini
; 注释行以分号（;）开头
# 也可以用井号（#）作为注释行的开头

[database]
host = localhost
port = 3306
username = root
password = password123
database = mydatabase

[web]
host = 0.0.0.0
port = 8000
debug = True

[logging]
file = /var/log/myapp.log
level = INFO
```

```python
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# 获取数据库连接相关的配置信息
db_host = config.get('database', 'host')
db_port = config.getint('database', 'port')
db_username = config.get('database', 'username')
db_password = config.get('database', 'password')
db_database = config.get('database', 'database')

# 获取Web应用程序相关的配置信息
web_host = config.get('web', 'host')
web_port = config.getint('web', 'port')
web_debug = config.getboolean('web', 'debug')

# 获取日志相关的配置信息
log_file = config.get('logging', 'file')
log_level = config.get('logging', 'level')

```



> ini文件格式、yaml文件格式、json文件格式。这三种配置文件的格式该如何选择，他们的各自的优缺点是什么

在选择使用INI、YAML或JSON格式的配置文件时，需要根据实际情况进行权衡和选择。下面是它们各自的优缺点：

1. INI文件格式

INI文件格式最早出现于Windows操作系统，它的语法简单、易于理解和使用，适合于存储小型配置信息。INI文件格式使用节（section）和键值对（key-value pairs）的方式进行组织，方便人类阅读和编辑，但缺少一些复杂的数据类型和数据结构。如果需要存储复杂的数据类型，如列表、字典等，则INI文件格式的应用受限。

优点：

- 语法简单、易于理解和使用。
- 可以方便地组织和管理配置信息。
- 适合存储小型配置信息。

缺点：

- 缺少复杂的数据类型和数据结构支持。
- 不适合存储大量和复杂的配置信息。

1. YAML文件格式

YAML文件格式是一种轻量级的数据交换格式，它的语法灵活、丰富和易于理解，支持多种数据类型和数据结构，可以用于存储各种类型的配置信息。YAML文件格式使用缩进和换行的方式进行组织，对于人类阅读和编辑非常友好，但也因此可能存在缩进格式不一致的问题。此外，YAML文件格式在解析时可能存在一定的安全隐患，因此需要注意配置文件的安全性。

优点：

- 语法灵活、丰富和易于理解。
- 支持多种数据类型和数据结构。
- 可以用于存储各种类型的配置信息。

缺点：

- 可能存在缩进格式不一致的问题。
- 在解析时可能存在一定的安全隐患。

1. JSON文件格式

JSON文件格式是一种轻量级的数据交换格式，它的语法简单、明确和规范，支持多种数据类型和数据结构，可以用于存储各种类型的配置信息。JSON文件格式使用大括号和方括号的方式进行组织，对于人类阅读和编辑不太友好，但可以使用各种编程语言的JSON库进行解析和处理。此外，JSON文件格式在解析时比较安全，不容易受到注入攻击等安全问题。

优点：

- 语法简单、明确和规范。
- 支持多种数据类型和数据结构。
- 可以用于存储各种类型的配置信息。
- 在解析时比较安全。

缺点：

- 对于人类阅读和编辑不太友好。

综上所述，INI文件格式适合存储小型配置信息，YAML文件格式适合存储各种类型的配置信息，JSON文件