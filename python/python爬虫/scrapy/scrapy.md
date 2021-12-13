## scrapy框架

https://scrapy.org/

什么是框架？

>集成了很多功能，具有很强通用性的一个项目模板。

如何学习框架？

>专门学习框架封装的各种功能的详细用法

什么是scrapy？

>爬虫中封装好的一个明星框架。

scrapy功能：

- 高性能的持久化存储
- 异步数据下载
- 高性能数据解析
- 分布式

安装

```
pip install scrapy
```

## scrapy基本使用

通过终端指令创建一个工程

```
scrapy startproject my_spider
```

```
You can start your first spider with:
    cd my_spider
    scrapy genspider example example.com
```

目录如下

```
|-my_spider
  |-my_spider
    |-spiders
      |- __init__.py
    |-items.py
    |-middlewares.py
    |-pipelines.py
    |-settings.py
  |-scrapy.cfg
```

spiders文件夹放爬虫文件。在子目录中创建一个爬虫文件



```
cd my_spider
scrapy genspider baidu_spider www.baidu.com
```



