# MapReduce

## 概述

案例：假设你有一100个文档，想知道文档里的每个单词出现了多少次。

#### Map（映射）阶段

**任务**：首先，你需要读取文档并对每个单词进行计数。
**操作**：在 Map 阶段，每个文档会被分成小块，然后每块会被送到一个不同的计算机（或者说节点）上。
**输出**：每个节点会输出一个键值对列表，键是单词，值是这个单词出现的次数（通常是 1）。

比如，文本 "Hello, World! Hello" 会被转换为：

```
(Hello, 1)
(World, 1)
(Hello, 1)
```

#### Reduce（归约）阶段

**任务**：现在，你需要把所有相同的单词的计数加起来。
**操作**：在 Reduce 阶段，所有相同的键（也就是单词）会被聚集在一起，并送到同一个节点上。
**输出**：这个节点会把所有相同单词的值（也就是计数）加起来。

例如，上面的键值对列表会被归约为：

```
(Hello, 2)
(World, 1)
```

总结

**Map**：把大任务分成小任务，然后在多个节点上并行处理。

**Reduce**：把多个节点的处理结果聚集在一起，得到最终结果。



Hadoop Map/Reduce是一个使用简易的软件框架，基于它写出来的应用程序能够运行在由上千个商用机器组成的大型集群上，并以一种可靠容错的方式并行处理上T级别的数据集。

一个Map/Reduce *作业（job）* 通常会把输入的数据集切分为若干独立的数据块，由 *map任务（task）*以完全并行的方式处理它们。框架会对map的输出先进行排序， 然后把结果输入给*reduce任务*。通常作业的输入和输出都会被存储在文件系统中。 整个框架负责任务的调度和监控，以及重新执行已经失败的任务。

通常，Map/Reduce框架和[分布式文件系统](https://hadoop.apache.org/docs/r1.0.4/cn/hdfs_design.html)是运行在一组相同的节点上的，也就是说，计算节点和存储节点通常在一起。这种配置允许框架在那些已经存好数据的节点上高效地调度任务，这可以使整个集群的网络带宽被非常高效地利用。

Map/Reduce框架由一个单独的master JobTracker 和每个集群节点一个slave TaskTracker共同组成。master负责调度构成一个作业的所有任务，这些任务分布在不同的slave上，master监控它们的执行，重新执行已经失败的任务。而slave仅负责执行由master指派的任务。

应用程序至少应该指明输入/输出的位置（路径），并通过实现合适的接口或抽象类提供map和reduce函数。再加上其他作业的参数，就构成了*作业配置（job configuration）*。然后，Hadoop的 *job client*提交作业（jar包/可执行程序等）和配置信息给JobTracker，后者负责分发这些软件和配置信息给slave、调度任务并监控它们的执行，同时提供状态和诊断信息给job-client。

虽然Hadoop框架是用JavaTM实现的，但Map/Reduce应用程序则不一定要用 Java来写 。

- [Hadoop Streaming](https://hadoop.apache.org/core/docs/r0.18.2/api/org/apache/hadoop/streaming/package-summary.html)是一种运行作业的实用工具，它允许用户创建和运行任何可执行程序 （例如：Shell工具）来做为mapper和reducer。
- [Hadoop Pipes](https://hadoop.apache.org/core/docs/r0.18.2/api/org/apache/hadoop/mapred/pipes/package-summary.html)是一个与[SWIG](http://www.swig.org/)兼容的C++ API （没有基于JNITM技术），它也可用于实现Map/Reduce应用程序。

## 输入与输出

Map/Reduce框架运转在<key, value> 键值对上，也就是说， 框架把作业的输入看为是一组<key, value> 键值对，同样也产出一组 <key, value> 键值对做为作业的输出，这两组键值对的类型可能不同。

框架需要对key和value的类(classes)进行序列化操作， 因此，这些类需要实现 [Writable](https://hadoop.apache.org/core/docs/r0.18.2/api/org/apache/hadoop/io/Writable.html)接口。 另外，为了方便框架执行排序操作，key类必须实现 [WritableComparable](https://hadoop.apache.org/core/docs/r0.18.2/api/org/apache/hadoop/io/WritableComparable.html)接口。

一个Map/Reduce 作业的输入和输出类型如下所示：

(input) <k1, v1> -> **map** -> <k2, v2> -> **combine** -> <k2, v2> -> **reduce** -> <k3, v3> (output)