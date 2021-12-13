# ElasticSearch

## ES介绍

我理解的es就是类似后端+数据库，也就是说数据存储在数据库里，但是它还给你提供了CRUD的接口，可以很方便地增删改查。

es 基本介绍https://www.cnblogs.com/dreamroute/p/8484457.html

## docker安装

拉取镜像

```
docker pull elasticsearch
```

运行ES镜像

```
docker run -dit --name es0 -p 80:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:6.7.0
```

- `-d`后台运行容器，并返回容器id
- `-i`以交互模式运行容器，与`-t`同时使用
- `-t`为容器重新非配一个伪输入终端，与`-i`同时使用
- `--name`为容器指定一个名称
- `-p`指定端口映射，格式为：`主机端口:容器端口`
- `-e`设置环境变量

**可能会遇到启动后内存不足的情况**：默认启动es镜像要2个G的内存，我的小服务器根本支撑不起。

https://blog.csdn.net/weixin_40660221/article/details/107656626

如果成功启动

访问服务器ip地址：http://119.45.58.134，即可看到如下信息

```json
{
  "name" : "rZmqp9e",
  "cluster_name" : "docker-cluster",
  "cluster_uuid" : "QDEjIE-qSHue8M_pgvqIWw",
  "version" : {
    "number" : "6.7.0",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "8453f77",
    "build_date" : "2019-03-21T15:32:29.844721Z",
    "build_snapshot" : false,
    "lucene_version" : "7.7.0",
    "minimum_wire_compatibility_version" : "5.6.0",
    "minimum_index_compatibility_version" : "5.0.0"
  },
  "tagline" : "You Know, for Search"
}
```

# 索引API

https://www.elastic.co/guide/en/elasticsearch/reference/6.7/indices.html

索引api用于管理单个索引、索引设置、别名、映射和索引模板。

文档是属于索引下的

## 索引管理

### [创建索引](https://www.elastic.co/guide/en/elasticsearch/reference/6.7/indices-create-index.html)

最常用的语法就是`PUT http://*/_index`

比如创建一个名为twitter的索引，所有选项都是默认值

```
PUT twitter
```

如果需要参数

```json
{
    "settings" : {
        "number_of_shards" : 5,
        "number_of_replicas" : 1
    }
}
```

### [删除索引](https://www.elastic.co/guide/en/elasticsearch/reference/6.7/indices-delete-index.html)

了解这个最简单的方法即可

```
DELETE twitter
```

### [查看索引](https://www.elastic.co/guide/en/elasticsearch/reference/6.7/indices-get-index.html)

```
GET /twitter
```

### [判断索引是否存在]()

```
HEAD /twitter
```

返回200说明这个索引存在，返回404说明不存在



# 文档API

https://www.elastic.co/guide/en/elasticsearch/reference/6.7/docs.html

是RESTful格式的api

**Single document APIs**

- [*Index API*](https://www.elastic.co/guide/en/elasticsearch/reference/6.7/docs-index_.html)
- [*Get API*](https://www.elastic.co/guide/en/elasticsearch/reference/6.7/docs-get.html)
- [*Delete API*](https://www.elastic.co/guide/en/elasticsearch/reference/6.7/docs-delete.html)
- [*Update API*](https://www.elastic.co/guide/en/elasticsearch/reference/6.7/docs-update.html)

**Multi-document APIs**

- [*Multi Get API*](https://www.elastic.co/guide/en/elasticsearch/reference/6.7/docs-multi-get.html)
- [*Bulk API*](https://www.elastic.co/guide/en/elasticsearch/reference/6.7/docs-bulk.html)
- [*Delete By Query API*](https://www.elastic.co/guide/en/elasticsearch/reference/6.7/docs-delete-by-query.html)
- [*Update By Query API*](https://www.elastic.co/guide/en/elasticsearch/reference/6.7/docs-update-by-query.html)
- [*Reindex API*](https://www.elastic.co/guide/en/elasticsearch/reference/6.7/docs-reindex.html)

## Single documents APIs

查找一篇文档（一条数据的json）

### Index API

用于增加或更新一篇JSON文档，如下例往索引为twitter的文档为`_doc`插入一条数据。

```json
PUT twitter/_doc/1
{
    "user" : "kimchy",
    "post_date" : "2009-11-15T14:12:12",
    "message" : "trying out Elasticsearch"
}
```

返回值

```json
{
    "_shards" : {
        "total" : 2,
        "failed" : 0,
        "successful" : 2
    },
    "_index" : "twitter",
    "_type" : "_doc",
    "_id" : "1",
    "_version" : 1,
    "_seq_no" : 0,
    "_primary_term" : 1,
    "result" : "created"
}
```



