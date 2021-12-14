# 1. requests库

## 1.1 通用代码框架

```python
import requests

url = "http://www.baidu.com"
r = requests.get(url, timeout=30)
r.raise_for_status()
r.encoding = r.apparent_encoding

html = r.text
```

requests库的方法`requests.`

| 方法         | 说明                                           |
| ------------ | ---------------------------------------------- |
| `.request()` | 构造一个请求，支持以下各方法                   |
| `.get()`     | 获取HTML网页的主要方法，对应于HTTP的GET        |
| `.head()`    | 获取HTML网页头信息的方法，对应于HTTP的HEAD     |
| `.post()`    | 向HTML网页提交POST请求的方法，对应于HTTP的POST |
| `.put()`     | 向HTML网页提交PUT请求的方法，对应于HTTP的PUT   |
| `.patch()`   | 向HTML网页提交局部修改请求，对应于HTTP的PATCH  |
| `.delete()`  | 向HTML网页提交删除请求，对应于HTTP的DELETE     |

`request.get(url, params=None, **kwargs)`完整格式

- params: url中的额外参数，字典或字节流格式，可选
- **kwargs: 12个控制访问的参数

**构造**一个向服务器请求资源的Request对象

**返回**一个包含服务器资源的Response对象



Response对象的属性

<font color="orange">**务必要牢记**</font>

| 属性                 | 说明                                             |
| -------------------- | ------------------------------------------------ |
| r.status_code        | HTTP请求的返回状态，200表示连接成功，404表示失败 |
| r.text               | HTTP响应内容的字符串形式，即，url对应的页面内容  |
| r.encoding           | 从HTTP header中猜测的响应内容编码方式            |
| r.apparent_enconding | 从内容中分析出的响应内容编码方式（备选编码方式） |
| r.content            | HTTP响应内容的二进制形式                         |
| r.headers            | 返回url页面的头部信息                            |

## 1.2 Requests库的异常

| 异常                     | 说明                                      |
| ------------------------ | ----------------------------------------- |
| request.ConnectionError  | 网络连接错误异常，如DNS查询失败、拒绝连接 |
| request.HTTPError        | HTTP错误异常                              |
| request.URLRequired      | URL缺失异常                               |
| request.TooManyRedirects | 超过最大重定向次数，产生重定向异常        |
| request.ConnectTimeout   | 连接远程服务器超时异常                    |
| request.Timeout          | 请求URL超时，产生超时异常                 |

`r.raise_for_staturs()`: r.status_code如果不是200，产生异常request.HTTPError

## 1.3 HTTP协议及Requests库方法

这些方法的功能

| 方法   | 说明                                                      |
| ------ | --------------------------------------------------------- |
| GET    | 请求获取URL位置的资源                                     |
| HEAD   | 请求获取URL位置资源的响应消息报告，即获得该资源的头部信息 |
| POST   | 请求向URL位置的资源后附加新的数据                         |
| PUT    | 请求向URL位置存储一个资源，覆盖原URL位置的资源            |
| PATCH  | 请求局部更新URL位置的资源，即改变该处资源的部分内容       |
| DELETE | 请求删除URL位置存储的资源                                 |

PATCH与PUT的区别

PATCH：节省带宽资源

## 1.4 requests库主要方法解析

`requests.reuqest(method,url,**kwargs)`

- `medthd`: 请求方式，GET/PUT/POST等
- `url`: 连接
- `**kwargs`: 13个控制请求方式
    - params: 字典或字节序列，作为参数增加到url中（修改url的字段）
    - data: 字典、字节序列或文件对象，作为Request的内容
    - json: 作为requeset的内容
    - headers: HTTP定制头
    
    - cookies: 字典或CookieJar, request中的cookie
    - auth: 元组，支持HTTP认证功能
    - files: 字典类型，传输文件
    - timeout: 设置超时时间
    - proxies: 设定访问代理服务器，可以增加登录认证
    
    - stream: Ture/False, 重定向开关
    - verify: Ture/Fals, 获取内容立即下载开关
    - allow_redirects: Ture/Fals, 认证SSL证书开关
    - cert: 本地SSL证书路径

method的功能，跟.get()之类的方法一样

`requests.get(url, params=None, **kwargs)` 12个

`requests.head(url, **kwargs)` 13全有

`requests.post(url, data=None, json=None, **kwargs)` 11个

`requests.put(url, data=None, **kwargs)` 12个

`requests.patch(url, data=None, **kwargs)` 12个

`requests.delete(url, **kwargs)` 13个

## 1.5 robots协议

/robots.txt

## 1.6 小结

通用代码框架

requests的主要方法



# 2. BeautifulSoup库

这个[网页](https://python123.io/ws/demo.html)的长相



它的html代码格式

```html

<!-- saved from url=(0033)https://python123.io/ws/demo.html -->
<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><title>This is a python demo page</title></head>
<body>
<p class="title"><b>The demo python introduces several python courses.</b></p>
<p class="course">Python is a wonderful general-purpose programming language. You can learn Python from novice to professional by tracking the following courses:
<a href="http://www.icourse163.org/course/BIT-268001" class="py1" id="link1">Basic Python</a> and <a href="http://www.icourse163.org/course/BIT-1001870001" class="py2" id="link2">Advanced Python</a>.</p>
</body></html>
```

## 2.1 BeautifulSoup库的基本元素

BS库是解析、遍历、维护“标签树”的功能库

是把html文档(str)转换成了BeautifulSoup类

BS类就看做一整个HTML文档的全部内容即可

**BS库解析器**

| 解析器           | 使用方法                        | 条件                 |
| ---------------- | ------------------------------- | -------------------- |
| bs4的HTML解析器  | BeautifulSoup(mk,'html.parser') | 安装bs4库            |
| lxml的HTML解析器 | BeautifulSoup(mk,'lxml')        | pip install lxml     |
| lxml的XML解析器  | BeautifulSoup(mk,'xml')         | pip install lxml     |
| html5lib的解析器 | BeautifulSoup(mk,'html5lib')    | pip install html5lib |

**BS类基本元素**

| 基本元素        | 说明                                                      |
| --------------- | --------------------------------------------------------- |
| Tag             | 比如`<body></body>`  `<p></p>`                            |
| Name            | 比如"body", "p"                                           |
| Attributes      | 标签的属性，字典形式组织，格式:<tag>.attrs                |
| NavigableString | 标签内非属性字符串，<>...</>中的字符串，格式:<tag>.string |
| Comment         | 标签内字符串的注释部分，一种特殊的Comment类型             |

## 2.2 基于bs4库的HTML内容遍历方法

![2](images/图2.jpg)

### 标签树的下行遍历

| 属性           | 说明                                                    |
| -------------- | ------------------------------------------------------- |
| `.contents`    | 子节点的列表，将<tag>所有儿子节点存入列表               |
| `.children`    | 子节点的迭代类型，与.contents类似，用于循环遍历儿子节点 |
| `.descendants` | 子孙借贷你的迭代类型，包含所有子孙节点，用于循环遍历    |

### 标签树的上行遍历

| 属性       | 说明                                         |
| ---------- | -------------------------------------------- |
| `.parent`  | 节点的父亲标签                               |
| `.parents` | 节点先辈标签的迭代类型，用于循环遍历先辈节点 |

### 标签树的平行遍历

| 属性                 | 说明                                                     |
| -------------------- | -------------------------------------------------------- |
| `.next_sibling`      | 返回按照HTML文本顺序的下一个平行节点标签                 |
| `.previous_sibling`  | 返回按照HTML文本顺序的上一个平行节点标签                 |
| `.next_siblings`     | 迭代类型，返回按照HTML文本顺序的**后**续所有平行节点标签 |
| `.previous_siblings` | 迭代类型，返回按照HTML文本顺序的**前**续所有平行节点标签 |

条件：平行遍历发生在**同一个父节点**下的各节点之间

## 2.3 基于bs4库的HTML格式化和编码

如何让HTML内容更加友好的显示

都是utf-8编码

``soup.prettify()`

`print(soup.a.prettify())`

## 2.4 信息标记的三种形式

- 标记后的信息可形成信息组织结构，增加了信息维度
- 标记后的信息可用于通信、存储或展示
- 标记的结构与信息一样具有重要价值
- 标记后的信息更利于程序理解和运用

HTML通过标签组织各种信息



### XML: eXtensible Markup Language

类似于HTML，XML是后有的`<name></name>`

### JSON: JavsScript Object Notation

有类型的键值对key:value("name":"北京理工大学")

可以用大括号嵌套使用键值对

对于java编程很方便

### YAML: YAML Ain't Markup Language

```
name:
    newName: 北京理工大学
    oldName: 延安自然科学院
# 并列关系
name:
    - xx
    - xxx
# | 表达整块数据
text: |
xxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxx
xxxxxxxxxxxxxxx
xxxxxxxxxxxx
```

通过缩进表达所属信息

### 比较

XML有效信息比例低，可扩展性好，但繁琐。(互联网流通中使用)

JSON各种{[(比较多，更适合程序 (移动应用云端，但是不能有注释)

YAML较为简洁，有效信息比例最高，可读性好(系统的配置文件)

## 2.5 信息提取的一般方法

法一：完整解析信息的标记形式，再提取关键信息。

XML JSON YAML
需要标记解析器 例如：bs4库的标签树遍历

优点：信息解析准确
缺点：提取过程繁琐，速度慢

法二：无视标记，直接搜索关键信息

搜索

对信息的文本查找函数即可。

优点：提取过程简洁，速度较快。

缺点：提取结果准确性与信息内容相关。

法三：融合上述两种方法。

例：提取HTML中所有URL链接

思路：

- 搜索所有`<a>`标签
- 解析`<a>`标签，提取href后的链接内容

## 2.6 基于bs4库的HTML内容查找方法

### `soup.find_all()`

`soup.find_all(name, attrs, recursive, string, **kwargs)`

返回一个列表类型，存储查找的结果。

name: 对标签名称的检索字符串。

attrs: 对标签属性值的检索字符串，可标注属性检索。

recursive: 是否对子孙全部检索，默认True

string: <>...</>中字符串区域的检索字符串



<tag>()等价于<tag>.find_all()

soup()等价于soup.find_all()


| 方法                      | 说明                                                        |
| ------------------------- | ----------------------------------------------------------- |
| .find()                   | 搜索且只返回一个结果，字符串类型，参数同.find_all()         |
| .find_parents()           | 在先辈节点中搜索，返回列表类型，参数同.find_all()           |
| .find_parent()            | 在先辈节点中返回一个结果，字符串类型，参数同.find_all()     |
| .find_next_siblings()     | 在后序平行节点中搜索，返回列表类型，参数同.find_all()       |
| .find_next_sibling()      | 在后序平行节点中返回一个结果，字符串类型，参数同.find_all() |
| .find_previous_siblings() | 在前序平行节点中搜索，返回列表类型，参数同.find_all()       |
| .find_previous_sibling()  | 在前序平行节点中返回一个结果，字符串类型，参数同.find_all() |

# 3. 正则表达式

## 3.1 基本概念

RE Regular Expression

作用

- 用来<font color="orange">**简洁**</font>表达一组字符串的表达式

- 是一种通用的字符串表达框架

- 针对字符串表达“简介”和“特征”思想的工具

- 判断某字符串的特征归属

在文本处理中的应用

- 表达文本类型的特征（病毒、入侵等）
- 同时查找或替换一组字符串
- 匹配字符串的全部或部分

正则表达式的使用

- 编译：将符合正则表达式语法的字符串转换成正则表达式

## 3.2 语法

RE由字符和操作符构成

| 操作符 | 说明                             | 实例                                    |
| ------ | -------------------------------- | --------------------------------------- |
| .      | 表示任何单个字符                 |                                         |
| []     | 字符集，对单个字符给出取值范围   | [abc]表示a、b、c，[a-z]表示某个小写字母 |
| [^ ]   | 非字符集，对单个字符给出排除范围 | [^abc]表示非a或非b或非c的单个字符       |
| *      | 前一个字符0次或无限次扩展        | abc*表示ab、abc、abcc、abccc…           |
| +      | 前一个字符1次或无限次扩展        | abc+表示abc、abcc、abccc…               |
| ?      | 前一个字符0次或1次扩展           | abc?表示ab、abc                         |
| \|     | 左右表达式任意一个               | abc\|def表示abc、def                    |
| {m}    | 扩展前一个字符m次                | ab{2}c=abbc                             |
| {m,n}  | 扩展前一个字符m次到n次（含n）    | ab{1,2}c=abc、abbc                      |
| ^      | 匹配字符串开头                   | ^abc表示abc且在一个字符串的开头         |
| $      | 匹配字符串结尾                   | abc$表示abc且在一个字符串的结尾         |
| ()     | 分组标记，内部只能使用 \| 操作符 | (abc)表示abc，(abc\|def)表示abc、def    |
| \d     | 数字，等价于[0-9]                |                                         |
| \w     | 单词字符，等价于[A-Za-z0-9_]     |                                         |

例：经典字符串

| 正则表达式                | 对应字符串                   |
| ------------------------- | ---------------------------- |
| `P(Y\|YT\|YTH\|YTHO)?N`   | PN、PYN、PYTN、PYTHN、PYTHON |
| `PY[TH]ON`                | PYTON、PYHON                 |
| `PY[^TH]?ON`              | PYON、PYaON、PYAON……         |
| `PY{:3}N`                 | PN、PYN、PYYN、PYYYN         |
| `^[A-Za-z]+$`             | 由26个字母组成的字符串       |
| `^[A-Za-z0-9]+$`          | 由26个字母和数字组成的字符串 |
| `^-?\d+$`                 | 整数形式的字符串             |
| `^[0-9]*[1-9][0-9]*$`     | 正整数字符串                 |
| `[1-9]\d{5}`              | 6位中国境内邮政编码          |
| `[\u4e00-\u9fa5]`         | 匹配中文字符                 |
| `\d{37}-\d{8}|d{4}-\d{7}` | 国内电话号码，010-68913536   |
| `[1-9]?\d`                | 0-99                         |
| `1\d{2}`                  | 100-199                      |
| `2[0-4]\d`                | 200-249                      |
| `25[0-5]`                 | 250-255                      |
|                           |                              |
|                           |                              |
|                           |                              |
|                           |                              |

## 3.3 Re库的基本使用

re库采用raw string类型表示正则表达式，表示为：`r'text'`

raw string 是不包含转义符(`'\'`)的字符串

string类型，更加繁琐，别用了`'text'`

**主要功能函数**

| 函数          | 说明                                                         |
| ------------- | ------------------------------------------------------------ |
| re.search()   | 在一个字符串中搜索匹配正则表达式的第一个位置，返回match对象  |
| re.match()    | 从一个字符串的**开始位置**起匹配正则表达式，返回match对象    |
| re.findall()  | 搜索字符串，以列表类型返回全部能匹配的字符串                 |
| re.split()    | 将一个字符串按照正则表达式匹配结果进行分割，返回列表类型     |
| re.finditer() | 搜索字符串，返回一个匹配结果的迭代类型，每个迭代元素是match对象 |
| re.sub()      | 在一个字符串中替换所有匹配正则表达式的子串，返回替换后的字符串 |

### `re.search(pattern,string,flags=0)`

- pattern: 正则表达式的字符串或原生字符串表示
- string: 待匹配字符串
- flags: 正则表达式使用时的控制标记

| 常用标记               | 说明                                                         |
| ---------------------- | ------------------------------------------------------------ |
| `re.I` `re.IGNORECASE` | 忽略正则表达式的大小写，[A-Z]能够匹配小写字符                |
| `re.M` `re.MULTILINE`  | 正则表达式中的`^`操作符能够将给定字符串的每行当做匹配开始（文章中的每一行匹配一次） |
| `re.S` `re.DOTALL`     | 正则表达式中的`.`操作符能够匹配所有字符，默认匹配除换行外的所有字符 |

### `re.match(pattern,string,flags=0)`

### `re.findall(pattern,string,flags=0)`

### `re.split(pattern,string,maxsplit=0,flags=0)`

- maxsplit: 最大分割数，剩余部分作为最后一个元素输出

### `re.finditer(pattern,string,flags=0)`

### `re.sub(pattern,repl,string,count=0,flags=0)`

- repl: 替换匹配字符串的字符串
- 匹配最大替换次数

### Re库的另一种等价用法

函数式用法：一次性操作

`match = re.search(r"[1-9]\d{5}", "BIT 100081")`

面向对象用法：编译后的多次操作

`pat = re.compile(r"[1-9]\d{5}")`

`rst = pat.search("BIT 100081")`



`regex = re.compile(pattern,flags=0)`

可以把这个regex看做一组字符串

regex.search()  regex.match() ... ...

## 3.4 match对象

一次匹配的结果

| 属性    | 说明                                |
| ------- | ----------------------------------- |
| .string | 待匹配文本                          |
| .re     | 匹配时用的pattern对象（正则表达式） |
| .pos    | 正则表达式搜索文本的开始位置        |
| .endpos | 正则表达式搜索文本的结束位置        |



| 方法      | 说明                             |
| --------- | -------------------------------- |
| .group(0) | 获得匹配后的字符串               |
| .start()  | 匹配字符串在原生字符串的开始位置 |
| .end()    | 匹配字符串在原生字符串的结束位置 |
| .span()   | 返回(.start(),.end())            |

## 3.5 re库的贪婪匹配和最小匹配

| 操作符 | 说明                              |
| ------ | --------------------------------- |
| *?     | 前一字符0次或无限次扩展，最小匹配 |
| +?     | 前一字符1次或无限次扩展，最小匹配 |
| ??     | 前一字符0次或1次扩展，最小匹配    |
| {m,n}? | 前一字符扩展m~n次(含n)，最小匹配  |

