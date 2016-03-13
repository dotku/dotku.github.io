#big-data


## 概念

1. 可视化分析。
2. 数据挖掘算法。
3. 预测性分析。
4. 语义引擎。
5. 数据质量和数据管理。

## 技术设计

数据采集：ETL [http://bbs.csdn.net/topics/390349305](http://bbs.csdn.net/topics/390349305)
数据存取：关系数据库、NOSQL、SQL
基础架构：云存储、分布式文件存储等。
数据处理：自然语言处理(NLP，Natural Language Processing)是研究人与计算机交互的语言问题的一门学科。处理自然语言的关键是要让计算机”理解”自然语言，所以自然语言处理又叫做自然语言理解(NLU，Natural Language Understanding)，也称为计算语言学(Computational Linguistics。一方面它是语言信息处理的一个分支，另一方面它是人工智能(AI, Artificial Intelligence)的核心课题之一。
统计分析：假设检验、显著性检验、差异分析、相关分析、T检验、方差分析、卡方分析、偏相关分析、距离分析、回归分析、简单回归分析、多元回归分析、逐步回归、回归预测与残差分析、岭回归、logistic回归分析、曲线估计、因子分析、聚类分析、主成分分析、因子分析、快速聚类法与聚类法、判别分析、对应分析、多元对应分析（最优尺度分析）、bootstrap技术等等。
数据挖掘：分类 （Classification）、估计（Estimation）、预测（Prediction）、相关性分组或关联规则（Affinity grouping or association rules）、聚类（Clustering）、描述和可视化、Description and Visualization）、复杂数据类型挖掘(Text, Web ,图形图像，视频，音频等)
模型预测：预测模型、机器学习、建模仿真。
结果呈现：云计算、标签云、关系图等。

## 技术架构

![big-data-architecture-diagram](https://pic1.zhimg.com/1e5e4619d13115ec24dbe84a431647c0_b.jpg)

1. 分析层: 元数据, 语义层, OLAP引擎
2. 数据访问: SQL(GBase, MonetDB), NoSQL(HBase, Cassandra, MongoDB), 缓存(Redis, Memcached)
3. 计算层: 内存计算(Spark+Shark), IMDG(Drill, Impala), Hive, 
数据挖掘(R, Mahout), 分布式计算(YARN)，文件系统(ceph, HDFS), 流计算(Storm)
4. 数据源: 结构化数据， 非结构化数据，实时数据

> 数据源：其实这种分类法是一种，还可以分为离线数据、近似实时数据和实时数据。按照图中的分类其实就是说明了数据存储的结构，而特别要说的是流数据，它的核心就是数据的连续性和快速分析性；

> 计算层：内存计算中的Spark是UC Berkeley的最新作品，思路是利用集群中的所有内存将要处理的数据加载其中，省掉很多I/O开销和硬盘拖累，从而加快计算。而Impala思想来源于Google Dremel，充分利用分布式的集群和高效存储方式来加快大数据集上的查询速度，这也就是我上面说到的近似实时查询；底层的文件系统当然是HDFS独大，也就是Hadoop的底层存储，现在大数据的技术除了微软系的意外，基本都是HDFS作为底层的存储技术。上层的YARN就是MapReduce的第二版，和在一起就是Hadoop最新版本。基于之上的应用有Hive，Pig Latin，这两个是利用了SQL的思想来查询Hadoop上的数据。

> 现在说到你问题中的关键了，想利用大数据做决策支持，那么好，R可以帮你在大数据上做统计分析，利用R语言和框架可以实现很专业的统计分析功能，并且能利用图形的方式展现；而Mahout就是一个集数据挖掘、决策支持等算法于一身的工具，其中包含的都是基于Hadoop来实现的经典算法，拿这个作为数据分析的核心算法集来参考还是很好的。  数据层和分析层就不过多的说了，主要的在计算层中已经说了。至于你问题的后半部分，这样一个决策支持系统要怎么展现呢？其实这个和数据挖掘过程中的展现一样，无非就是通过表格和图标图形来进行展示，其实一份分类详细、颜色艳丽、数据权威的数据图标报告就是呈现给客户的最好方式！至于用什么工具来实现，有两个是最好的数据展现工具，Tableau和Pentaho，利用他们最为数据展现层绝对是最好的选择。

## 大数据的处理

## 相关新闻
1. 存储系统: Cassandra 问题, 处理高 IO，HBase，MengoDB 更合适[https://www.zhihu.com/question/19593207](https://www.zhihu.com/question/19593207)

2. 存储技术比较: HDFS 是主流， MooseFS 也不差[https://www.zhihu.com/question/22171041](https://www.zhihu.com/question/22171041)

3. BigTable 实践成本高，HBase 是可代替方案[https://www.zhihu.com/question/19867181](https://www.zhihu.com/question/19867181)

4. Hadoop主要分三部分构成：HDFS、MapReduce、ZooKeeper

5. 数据监控技术: Nagios

6. ceph是统一存储架构，支持文件、块、对象三种方式。

7. Hadoop的子项目Hive和Pig 都不错[http://www.infoq.com/cn/news/2013/12/facebook-hadoop](http://www.infoq.com/cn/news/2013/12/facebook-hadoop)