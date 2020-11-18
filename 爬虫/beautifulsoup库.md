# request

`requests.`

| 方法         | 说明                                           |
| ------------ | ---------------------------------------------- |
| `.request()` | 构造一个请求，支持以下各方法                   |
| `.get()`     | 获取HTML网页的主要方法，对应于HTTP的GET        |
| `.head()`    | 获取HTML网页头信息的方法，对应于HTTP的HEAD     |
| `.post()`    | 向HTML网页提交POST请求的方法，对应于HTTP的POST |
| `.put()`     | 向HTML网页提交PUT请求的方法，对应于HTTP的PUT   |
| `.patch()`   | 向HTML网页提交局部修改请求，对应于HTTP的PATCH  |
| `.delete()`  | 向HTML网页提交删除请求，对应于HTTP的DELETE     |



`r=requests.get(url)`:

**构造**一个向服务器请求资源的Request对象

**返回**一个包含服务器资源的Response对象

`request.get(url, params=None, **kwargs)`完整格式

- params: url中的额外参数，字典或字节流格式，可选

- **kwargs: 12个控制访问的参数



`respons`对象的属性

<font color="orange">**务必要牢记**</font>

| 属性                 | 说明                                             |
| -------------------- | ------------------------------------------------ |
| r.status_code        | HTTP请求的返回状态，200表示连接成功，404表示失败 |
| r.text               | HTTP响应内容的字符串形式，即，url对应的页面内容  |
| r.encoding           | 从HTTP header中猜测的响应内容编码方式            |
| r.apparent_enconding | 从内容中分析出的响应内容编码方式（备选编码方式） |
| r.content            | HTTP响应内容的二进制形式                         |

爬虫流程

- 检测`r.status_code==200`
- 利用上面的属性去解析网络页面

若header中不存在charset字段，默认r.encoding=ISO-8859-1

r.apparent_enconding更加靠谱  

## Requests库的异常

| 异常                     | 说明                                      |
| ------------------------ | ----------------------------------------- |
| request.ConnectionError  | 网络连接错误异常，如DNS查询失败、拒绝连接 |
| request.HTTPError        | HTTP错误异常                              |
| request.URLRequired      | URL缺失异常                               |
| request.TooManyRedirects | 超过最大重定向次数，产生重定向异常        |
| request.ConnectTimeout   | 连接远程服务器超时异常                    |
| request.Timeout          | 请求URL超时，产生超时异常                 |

r.raise_for_staturs(): r.status_code如果不是200，产生异常request.HTTPError

## HTTP协议及Requests库方法

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

## requests库主要方法解析

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

## 小结

通用代码框架

requests的主要方法

## robots协议

/robots.txt

