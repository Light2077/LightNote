# Hadoop学习文档

| 版本号 | 时间           | 编辑人 | 更新说明                                       |
| ------ | -------------- | ------ | ---------------------------------------------- |
| v1.0   | 2020年11月12日 | 李一繁 | 初步撰写文档，包含Hadoop存储和Python调用的方法 |
|        |                |        |                                                |

 ## 1 Hadoop简介

### 1.1 Hadoop的诞生背景

![](pics/hadoop.png)

Hadoop的诞生与大数据时代的发展密切相关。在互联网刚兴起的时代，搜索引擎类公司如Google通过网络爬虫获取了大量的网页内容，但是这些海量的的内容如何稳定存储和高效查询确实一个难点问题。

因为网页数据是多源异构的非结构数据，不经处理无法落入数据库，就算处理得当，但是每多一个网站就要人为分析并建一张新表，工作了过于庞大。所以最早Google内部开发了属于自己的分布式存储系统，并于2003年发布了论文《Google File System》，该论文介绍了如何存储Google的海量数据，之后于2005年发布了《MapReduce:  Simplified Data Processing on Large Clusters》，该论文介绍了如何计算GFS存储的海量数据。

Google虽然发表了论文介绍了核心原理，但是这些系统仅限于内部使用并未开源。

Doug Cutting是Lucene和Nutch的创立者，他于1985年毕业于美国斯坦福大学，专门从事网页检索方面的工作。

![](pics/cutting.png)

Cutting根据《Google File System》设计了NDFS（Nutch Distributed File System），之后将存储部分的模块独立出来，并改名为HDFS（Hadoop Distributed File System），之后又根据《MapReduce:  Simplified Data Processing on Large Clusters》设计了基于Hadoop的MapReduce。并于2006年贡献给Apache基金会。



### 1.2 Hadoop与大数据

#### 1.2.1 大数据的存储

到了2006年，各大2C的互联网公司都出现了存储的瓶颈问题。以eBay为例，当时eBay每天新增的数据量达到50TB，1年累计的数据量即达到18PB。与之相对地，根据IDC的研究报告，自人类开始记录历史以来，到2006年为止全人类全部的印刷书本文字加起来大约50PB。也就是说，仅eBay平台3年的新增数据，就超过了全人类全部书本的数据量。同时，在社交网站Facebook的计算机集群的磁盘空间中，目前已存储了超过100PB的数据，也就是说，仅Facebook一个网站存储的数据，就已经是人类书本数据量的2倍之多。  

#### 1.2.2 大数据的价值

此外，越来越多的企业认识到了大数据的价值。

**第一、计算机科学在大数据出现之前，非常依赖模型以及算法。**

人们如果想要得到精准的结论，需要建立模型来描述问题，同时，需要理顺逻辑，理解因果，设计精妙的算法来得出接近现实的结论。因此，一个问题，能否得到最好的解决，取决于建模是否合理，各种算法的比拼成为决定成败的关键。然而，大数据的出现彻底改变了人们对于建模和算法的依赖。举例来说，假设解决某一问题有算法A 和算法B。在小量数据中运行时，算法A的结果明显优于算法B。也就是说，就算法本身而言，算法A能够带来更好的结果；然而，人们发现，当数据量不断增大时，算法B在大量数据中运行的结果优于算法A在小量数据中运行的结果。这一发现给计算机学科及计算机衍生学科都带来了里程碑式的启示：当数据越来越大时，数据本身（而不是研究数据所使用的算法和模型）保证了数据分析结果的有效性。即便缺乏精准的算法，只要拥有足够多的数据，也能得到接近事实的结论。数据因此而被誉为新的生产力。.

**当数据达到一定程度时，数据本身就可以说话了。**

**第二、当数据足够多的时候，不需要了解具体的因果关系就能够得出结论。**

例如，Google 在帮助用户翻译时，并不是设定各种语法和翻译规则。而是利用Google数据库中收集的所有用户用词习惯进行比较推荐。Google检查所有用户的写作习惯，将最常用、出现频率最高的翻译方式推荐给用户。在这一过程中，计算机可以并不了解问题的逻辑，但是当用户行为的记录数据越来越多时，计算机就可以在不了解问题逻辑的情况之下，提供最为可靠的结果。可见，海量数据和处理这些数据的分析工具，为理解世界提供了一条完整的新途径。

**第三、由于能够处理多种数据结构，大数据能够在最大程度上利用互联网上记录的人类行为数据进行分析。**

大数据出现之前，计算机所能够处理的数据都需要前期进行结构化处理，并记录在相应的数据库中。但大数据技术对于数据的结构的要求大大降低，互联网上人们留下的社交信息、地理位置信息、行为习惯信息、偏好信息等各种维度的信息都可以实时处理，立体完整地勾勒出每一个个体的各种特征。

**第四、从政府或社会角度，大数据时代到来，会催生很多新的就业岗位**



人们对大数据存储需求和对数据价值的认识使得Hadoop成为了Apache最火热的开源项目。	

### 1.3 Hadoop和商业

Cutting于2006编写了Hadoop之后，在雅虎公司一直从事Hadoop相应工作的开发。

2008年，由Christophe Bisciglia, Amr Awadallah 以及 Jeff Hammerbacher创建的**Cloudera **开始涉足大数据领域，并成为Hadoop的供应商。

![](pics/cloudera.png)

2009年Cloudera发行了它的第一个Hadoop集成版本。现在业界通常也把Cloudera发行的Hadoop版本叫做CDH。CDH里面包括的是100%开源的东西。但是Cloudera的企业版里面也会包括一个叫做Cloudera Manager的管理组件。这个组件是闭源的，闭源的管理软件给用户提供了很多Haoop的易用性。

2009年9月，由于Cutting和雅虎的管理人员Eric不和，被Cloudera成功挖走，之后Cloudera也一直被认为是Hadoop的正宗，Cutting也得到了更好的发展，之后荣升了Apache基金会的主席。 

也是2009年，多次创业的老选手 John Schroeder和在谷歌做谷歌文件系统的工程师老印M.C.Srivas联合成立了**MapR**。 MapR也是一家Hadoop的发行商，但是它家的套路有点不太一样。MapR用C++重新写了整个Hadoop文件系统，所以它的版本只是保持了和Hadoop的接口兼容，实际的实现是自己做的。印度的CTO有资深的文件系统背景，而且印度又码农价廉物美。MapR结合硅谷印度人的经验和资金，以及印度的文件系统开发团队，正式杀入了Hadoop发行商的市场。 

![](pics/mapr.png)

2011年，雅虎将整个Hadoop团队全体的拆分出去，正式成立一家名字叫做**Hortonworks**的公司。而Hortonworks由Eric主导，Eric最初是CEO，后来又做了CTO。 后于2013年离开。

![](pics/hortonworks.png)

2013年，英特尔投资7.4亿美金入股Cloudera18% ，并结束了英特尔Hadoop版本的100多人团队的开发。同年，该团队的主要负责人孙元浩离职，并创立了星环科技。

![](pics/星环科技.png)

 ## 2 Hadoop原理

### 2.1 Hadoop主要特性



 ## 3 Hadoop部署使用

### 3.1 Hadoop部署

### 3.2 原生API使用

#### 3.3.1 测试环境

```shell
测试：主机为172.16.2.114，Hadoop版本为2.7，请用shell操作
开发：能访问到172.16.2.114，保证开发机器的/etc/hosts做了如下的IP配置

172.16.2.114 automlgpu1
172.16.2.115 automlgpu2
172.16.2.116 automlgpu3
```

#### 3.3.2 测试代码

##### 3.3.2.1 创建目录

貌似只能一层一层创建

```shell
hadoop fs -mkdir /NewHand
hadoop fs -mkdir /NewHand/liyifan
```

##### 3.3.2.2 上传文件

自己新建一个1.txt

上传如果无法覆盖，可以先删除

```shell
hadoop fs –put 1.txt /NewHand/liyifan
```

##### 3.3.2.3 查看文件

```shell
hadoop fs –ls /NewHand/liyifan
```

##### 3.3.2.4 下载文件

```shell
hadoop fs –get /NewHand/liyifan/1.txt 
```

##### 3.3.2.5 删除文件目录

```shell
hadoop fs –rm /NewHand/liyifan/1.txt 
hadoop fs –rmdir /NewHand/liyifan/
```

##### 

### 3.3 Python API使用

#### 3.3.1 测试环境

##### 3.3.1.1 Python环境

详细API可以参考：https://hdfscli.readthedocs.io/en/latest/

```shell
python = 3.x
hdfs == 2.5.8
```

##### 3.3.1.2 Hadoop环境

```shell
测试：主机为172.16.2.114，版本为2.7，请访问172.16.2.114:8888的jupyter操作，jupyter右上角内核要选automl
开发：能访问到172.16.2.114，保证开发机器的/etc/hosts做了如下的IP配置

172.16.2.114 automlgpu1
172.16.2.115 automlgpu2
172.16.2.116 automlgpu3
```

#### 3.3.2 测试代码

##### 3.3.2.1 建立连接

```python
import hdfs
client = hdfs.Client("http://172.16.2.114:50070", root='/')
```

##### 3.3.2.2 创建目录

```python
client.makedirs('/NewHand/liyifan')
```

##### 3.3.2.3 上传文件

自己新建一个1.txt

上传如果无法覆盖，可以先删除

```python
client.upload('/NewHand/liyifan', '1.txt')
```

##### 3.3.2.4 查看目录文件

```python
client.list('/NewHand/liyifan')
```

##### 3.3.2.5 查看文件状态

```python
client.status('/NewHand/liyifan')
```

##### 3.3.2.6 下载文件

```python
client.download('/NewHand/liyifan/1.txt', '1.txt', overwrite=True)
```

##### 3.3.2.7 删除文件

可以选择递归

```python
client.delete('/NewHand/liyifan/1.txt', recursive=False)
```

##### 3.3.2.8 字节流操作

前面都是操作整个文件，可以打开HDFS文件去读取字节，这样本地就不会下载这个文件，比如读取csv：

```python
with client.read('/NewHand/liyifan/1.txt') as fs:
    stat_hdfs = pd.read_csv(fs)
```

##### 3.3.2.9 判断文件或文件夹是否存在

```python
if client.content('/NewHand/liyifan/1.txt'):
    print('文件存在')
    
if client.status('/NewHand/liyifan'):
    print('文件夹存在')
```

##### 3.3.2.10 直接读取pandas dataframe

#### 3.3.3 封装示例

熟悉API之后可以将HDFS做一个封装

```python
import os, json
import hdfs
import shutil
import pickle
# 使用pickle而不用joblib，是因为考虑到不仅仅sklearn模型保存以及pickle可以直接保存到内存中
import pandas as pd
import numpy as np
from util.BaseFS import BaseFS
from conf import localInputPathTemp, localOutputPathTemp, WebHDFSAddr, NginxAddr, AlluxioAddr

class HDFSFS(BaseFS):
    def __init__(self):
        # 对于WebHDFS的读写，在不考虑Kuberos的情况下，需要将/etc/hosts文件配置和Hadoop集群一样的IP
        self.HDFSClient = hdfs.Client(WebHDFSAddr, root='/')
        self.localInputPathTemp = localInputPathTemp
        self.localOutputPathTemp = localOutputPathTemp
        self.NginxAddr = NginxAddr

    def load_dataframe(self, inputPath):
        # 现在读取文件的形式都是统一存入内存当中，多用户可能会内存溢出
        # 但是对于spark文件要拼合的，目前也只能在内存中拼合，所以没有更好的办法
        # 强哥建议可以先读一个文件，然后计算总的内存大小，如果超过一定比例就报错返回
        # 或者如果是csv文件就先读取几行，然后估算总体内存大小，但是parquet文件就无法计算了
        #  "hdfs:/user/experiment/tmp/{graph_id}-{node_id}{port_id}" 要去掉前面的hdfs
        inputPath = inputPath.split(':')[1]
        total = None
        if self.HDFSClient.status(inputPath)['type'] == 'FILE':  # 是sklearn生成的
            try:
                with self.HDFSClient.read(inputPath) as fs:
                    total = pd.read_csv(fs, encoding='utf-8')# 加engine = 'python'会报错
            except:
                print('不符合utf-8编码，采用GBK')
                with self.HDFSClient.read(inputPath) as fs:
                    total = pd.read_csv(fs, encoding='gbk')# 加engine = 'python'会报错
        elif self.HDFSClient.status(inputPath)['type'] == 'DIRECTORY':  # 是spark生成的
            first = True
            for i in self.HDFSClient.list(inputPath):
                if i.startswith('part'):
                    try:
                        with self.HDFSClient.read(os.path.join(inputPath, i)) as fs:
                            tmp = pd.read_csv(fs, encoding='utf-8', engine='python')
                            if first:
                                total = tmp
                                first = False
                            else:
                                total = pd.concat([total, tmp], axis=0)
                    except:
                        print('不符合utf-8编码，采用GBK')
                        with self.HDFSClient.read(os.path.join(inputPath, i)) as fs:
                            tmp = pd.read_csv(fs, encoding='gbk', engine='python')
                            if first:
                                total = tmp
                                first = False
                            else:
                                total = pd.concat([total, tmp], axis=0)
        total.index = range(total.shape[0])
        return total

    def load_supervised_ml_dataframe(self, inputPath):
        data = self.load_dataframe(inputPath)
        feature = data.iloc[:, :-1]
        label = data.iloc[:, -1]
        return feature, label

    def load_unsupervised_ml_dataframe(self, inputPath):
        data = self.load_dataframe(inputPath)
        return data

    # 权限： 创建者是	dr.who	supergroup
    def save_dataframe(self, data, outputPath):
        # 目前的outputPath ： "hdfs:/user/experiment/tmp/{graph_id}-{node_id}{port_id}"
        graphNodePort = outputPath.split('/')[-1]
        localOutputPath= os.path.join(self.localOutputPathTemp, graphNodePort)
        #  "hdfs:/user/experiment/tmp/{graph_id}-{node_id}{port_id}" 要去掉前面的hdfs
        outputPath = outputPath.split(':')[1]
        # 一定要注意不能加index！否则下次读取会多一列Unnamed的index列
        self.clean_file_from_local(localOutputPath)
        data.to_csv(localOutputPath, index=None)
        self.HDFSClient.upload(outputPath, localOutputPath, overwrite=True)

    def load_ml_model(self, inputPath):
        # 目前的inputPath ： "hdfs:/user/experiment/tmp/{graph_id}-{node_id}{port_id}"
        graphNodePort = inputPath.split('/')[-1]
        inputPath = inputPath.split(':')[1]
        localInputPath= os.path.join(self.localInputPathTemp, graphNodePort)
        self.clean_file_from_local(localInputPath)
        self.HDFSClient.download(hdfs_path=inputPath, local_path=localInputPath, overwrite=True)
        with open(localInputPath, 'rb') as f:
            model = pickle.load(f)
        return model

    def save_ml_model(self, model, outputPath, saveModel=False):
        # 目前的outputPath ： "hdfs:/user/experiment/tmp/{graph_id}-{node_id}{port_id}"
        graphNodePort = outputPath.split('/')[-1]
        localOutputPath= os.path.join(self.localOutputPathTemp, graphNodePort)
        #  "hdfs:/user/experiment/tmp/{graph_id}-{node_id}{port_id}" 要去掉前面的hdfs
        outputPath = outputPath.split(':')[1]
        with open(localOutputPath, 'wb') as f:
            pickle.dump(model, f)
        if not saveModel:
            self.HDFSClient.upload(outputPath, localOutputPath, overwrite=True)
        else:
            self.HDFSClient.upload(outputPath+'_model', localOutputPath, overwrite=True)
            
    def save_npz(self, data, outputPath):
         #data = {'text': text, 'tag2id': tag2id, 'token2id': token2id, 'sub_length': sub_length}
        # 目前的outputPath ： "hdfs:/user/experiment/tmp/{graph_id}-{node_id}{port_id}"
        graphNodePort = outputPath.split('/')[-1]
        localOutputPath= os.path.join(self.localOutputPathTemp, graphNodePort) + '.npz'
        #  "hdfs:/user/experiment/tmp/{graph_id}-{node_id}{port_id}" 要去掉前面的hdfs
        outputPath = outputPath.split(':')[1]
        # data = {'text': text, 'tag2id': tag2id, 'token2id': token2id}
        self.clean_file_from_local(localOutputPath)
        np.savez(localOutputPath, **data)
        self.HDFSClient.upload(outputPath, localOutputPath, overwrite=True)

    def load_npz(self, inputPath):
        # 目前的inputPath ： "hdfs:/user/experiment/tmp/{graph_id}-{node_id}{port_id}"
        graphNodePort = inputPath.split('/')[-1]
        inputPath = inputPath.split(':')[1]
        localInputPath= os.path.join(self.localInputPathTemp, graphNodePort)
        self.clean_file_from_local(localInputPath)
        self.HDFSClient.download(hdfs_path=inputPath, local_path=localInputPath, overwrite=True)
        data = np.load(localInputPath, allow_pickle=True)
        return data

    # 读取json文件
    def load_json(self, inputPath):
        # 目前的inputPath ： "hdfs:/user/experiment/tmp/{graph_id}-{node_id}{port_id}"
        inputPath = inputPath.split(':')[1]
        with self.HDFSClient.read(inputPath) as fs:
            print(inputPath)
            print(type(fs))
            # 加engine = 'python'会报错
            data = json.loads(fs.data)
        return data

    # 读取json文件
    def save_json(self, data, outputPath):
        # 目前的inputPath ： "hdfs:/user/experiment/tmp/{graph_id}-{node_id}{port_id}"
        graphNodePort = outputPath.split('/')[-1]
        outputPath = outputPath.split(':')[1]
        localOutputPath = os.path.join(self.localOutputPathTemp, graphNodePort)
        self.clean_file_from_local(localOutputPath)
        with open(localOutputPath, 'w') as f:
            json.dump(data, f)
        self.HDFSClient.upload(outputPath, localOutputPath, overwrite=True)

    # 清理目录
    def clean_file_from_local(self, filePath):
        if os.path.exists(filePath) and os.path.isdir(filePath):
            shutil.rmtree(filePath)
        elif os.path.exists(filePath) and os.path.isfile(filePath):
            os.remove(filePath)

```



## 参考资料

### 论文

[1]《Google File System》https://storage.googleapis.com/pub-tools-public-publication-data/pdf/035fc972c796d33122033a0614bc94cff1527999.pdf

[2]《MapReduce:  Simplified Data Processing on Large Clusters》https://www.usenix.org/legacy/event/osdi04/tech/full_papers/dean/dean.pdf

### 网页

[1] 血淋淋的Cloudera上市路  https://www.sohu.com/a/134406998_160850

[2] 2.5亿，星环往事：从Intel走出的孙元浩和他的Hadoop征程 https://zhuanlan.zhihu.com/p/22343807

[3] 长文：Cloudera难卖身！回顾Hadoop黑历史！https://3g.163.com/dy/article/FFIV6NUJ05315PUD.html

