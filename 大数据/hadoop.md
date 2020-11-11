大数据

- 数据量大
- 高速增长
- 种类多样（图片、视频）
- 价值密度低
- 真实性

### Hadoop

Apache的Hadoop是一个开源的、可靠的、可扩展的系统架构，可利用分布式架构来存储海量数据，以及实现分布式的计算

- reliable，可靠性，可以确保数据存储在Hadoop之后，即使服务器坏掉，数据也可以恢复
- scalable，可扩展性
- distributed，分布式

### Nutch

全文检索和爬虫

把数据存到数据库必须将非结构化数据转为结构化数据，以行列形式的二维表存储，

但是这种处理不可取，因为是通用爬虫数据，不能只能针对一个网站。

Hadoop的诞生最初是为了解决Nutch海量数据的存储问题，在Nutch0.8版本之后，就将模块独立出来，

并改名：**HDFS Hadoop Distributed File System**

在2004年，Google又公开发表了阐述其另一核心技术MapReduce的论文
之后Cutting又根据其设计了基于Hadoop的MapReduce

- HDFS 存取数据
- MapReduce 处理数据

**Hadoop2.0** 比第一代多了**YARN**和**others**

YARN计算需要多少内存多少CPU，做好资源管理

还可以跑MapReduce还有Others

第一代只能跑一种框架，第二代还可以跑spark等计算框架

Yarn 资源调度框架à实现对资源的细粒度封装（cpu，内存，带宽）此外，还可以通过yarn协调多种不同计算框架（MR，Spark）

**Hadoop3.0**

17年9月发布



Hadoop安装

- 单机模式：不能使用HDFS，只能使用MapReduce，所以单机模式主要是用于在本地调试MapReduce代码
- 伪分布式模式：用多个线程来模拟多台真实机器，即模拟分布式状态
- 完全分布式模式：用多台机器（或启动多个虚拟机）来完成部署集群。

```
wget http://bj-yzjd.ufile.cn-north-02.ucloud.cn/sqoop-1.4.4.bin__hadoop-2.0.4-alpha.tar.gz
```

