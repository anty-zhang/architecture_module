[TOC]

# 环境搭建

```bash
# 下载解压
tar -xzf kafka_2.9.2-0.8.1.1.tgz
cd kafka_2.9.2-0.8.1.1

# 启动服务
bin/zookeeper-server-start.sh config/zookeeper.properties &  # 启动zookeeper
bin/kafka-server-start.sh config/server.properties   # 启动kafka

# 创建topic
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test

# 查看topic
bin/kafka-topics.sh --list --zookeeper localhost:2181

# 发送消息
bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test 

# 启动consumer
bin/kafka-console-consumer.sh --bootstrap-server localhost:2181 --topic test --from-beginning


ukafka-4rieyu-1-bj03.service.ucloud.cn:9092, ukafka-4rieyu-2-bj03.service.ucloud.cn:9092, ukafka-4rieyu-3-bj03.service.ucloud.cn:9092, ukafka-4rieyu-4-bj03.service.ucloud.cn:9092 


bin/kafka-console-consumer.sh --zookeeper 10.10.148.197:2181 --topic analytics-user-profile --from-beginning > all_kafka.txt

参考网址 http://www.aboutyun.com/thread-12882-1-1.html

```

# 单机环境搭建
```bash
# config file
cat ./config/zookeeper.properties
# the directory where the snapshot is stored.
dataDir=/tmp/zookeeper
# the port at which the clients will connect
clientPort=2181

cat ./config/server.properties
log.dirs=/tmp/kafka-logs
zookeeper.connect=localhost:2181

nohup bin/zookeeper-server-start.sh config/zookeeper.properties > zookeeper-run.log 2>&1 &

nohup bin/kafka-server-start.sh config/server.properties > kafka-run.log 2>&1 &

# 创建kafka主题：

bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic HOTEL_gnhotel_elong_orderdetail

# 显示kafka所有主题：
bin/kafka-topics.sh -list -zookeeper localhost:2181

# 创建kafka生产者：

bin/kafka-console-producer.sh --broker-list localhost:9092 --topic HOTEL_gnhotel_elong_orderdetail

# 创建kafka消费者：

bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic HOTEL_gnhotel_elong_orderdetail --from-beginning

```

# 原理与特性
## 介绍

> Kafka是一个 "分布式的"/"可分区的(partitioned)"/"基于备份的(replicated)"/"基于commit-log存储"的服务. 它提供了类似于JMS的特性,但是在设计实现上完全不同,此外它并不是JMS规范的实现.

> kafka消息是根据 Topic进行归类,发送消息者成为Producer,消息接收者成为Consumer;此外kafka集群有多个kafka实例组成,每个实例(server)称为broker.

> 无论是kafka集群,还是producer和consumer都依赖于zookeeper来保证系统可用性以及保存一些meta信息.

## topic/logs

> 一个Topic可以认为是一类消息,每个topic将被分成多个partition(区),每个partition在存储层面是append log文件.任何发布到此partition的消息都会直接追加到log文件的尾部,每条消息在文件中的位置称为offset(偏移量),offset为一个long型数字,它唯一的标记一条消息.kafka并没有提供其他额外的索引机制来存储offset,因为在kafka中几乎不允许对消息进行"随机读-写",一旦消息写入log日志之后,将不能被修改.

> producer: kafka和JMS实现(activeMQ)不同的是: 即使消息被消费,消息仍然不会被立即删除 .日志文件将会根据broker中的配置要求,保留一定的时间之后删除;比如log文件保留2天,那么两天后,文件会被清除,无论其中的消息是否被消费.kafka通过这种简单的手段,来释放磁盘空间.此外,kafka的性能并不会因为日志文件的太多而低下,所以即使保留较多的log文件,也不不会有问题.

> consumer: 它需要保存消费消息的offset,对于offset的保存和使用,有consumer来控制;当consumer正常消费消息时,offset将会"线性"的向前驱动,即消息将依次顺序被消费.事实上consumer可以使用任意顺序消费消息,它只需要将offset重置为任意值..(offset将会保存在zookeeper中)

> kafka集群: 几乎不需要维护任何consumer和producer状态信息,这些信息有zookeeper保存;因此producer和consumer的客户端实现非常轻量级,它们可以随意离开,而不会对集群造成额外的影响

> partitions: 设计目的有多个.最根本原因是kafka基于文件存储.通过分区,可以将日志内容分散到多个server上,来避免文件尺寸达到单机磁盘的上限,每个partiton都会被当前server(kafka实例)保存;可以将一个topic切分多任意多个partitions(备注:基于sharding),来消息保存/消费的效率.此外越多的partitions意味着可以容纳更多的consumer,有效提升并发消费的能力


## tips
Messaging 和一些常规的消息系统相比,kafka仍然是个不错的选择;它具备partitons/replication和容错,可以使kafka具有良好的扩展性和性能优势.不过到目前为止,我们应该很清楚认识到,kafka并没有提供JMS中的"事务性""消息传输担保(消息确认机制)""消息分组"等企业级特性;kafka只能使用作为"常规"的消息系统,在一定程度上,尚未确保消息的发送与接收绝对可靠(比如,消息重发,消息发送丢失等)

Websit activity tracking kafka可以作为"网站活性跟踪"的最佳工具;可以将网页/用户操作等信息发送到kafka中.并实时监控,或者离线统计分析等.

Log Aggregation kafka的特性决定它非常适合作为"日志收集中心";application可以将操作日志"批量""异步"的发送到kafka集群中,而不是保存在本地或者DB中;kafka可以批量提交消息/压缩消息等,这对producer端而言,几乎感觉不到性能的开支.此时consumer端可以使hadoop等其他系统化的存储和分析系统.

# 参考网址:

http://shift-alt-ctrl.iteye.com/blog/1930345

