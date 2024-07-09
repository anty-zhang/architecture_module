
[TOC]

# hive本地模式

```bash
hive > set mapred.job.tracker=local;
hive > set hive.exec.mode.local.auto=true;

# 为何要使用本地模式: 查询速度很快,默认是关闭的,  但是要保证你查询的数据要在你执行hive所在的机器上，如果查询的数据文件不在本地，那么报file does not exists, 感觉还是没必要使用

```

# hive参数配置使用

```bash
# 在hql语句中，通过${}引用变量的值  通过${env:}引用java system的数据 
# 通过${system:}来引用shell环境变量的值) 

# 方式1：  范围hivevar定义局部变量  
#hive -d columeage=age  
hive>create table t(name string, ${columeage} string)  
# 方式2：  范围hiveconf定义全局     
#hive --hiveconf hive.cli.print.current.db=true;  
#hive --hiveconf hive.cli.print.header=true;  
# 方式3：  获取java system系统参数   
hive>create table t(name string, ${system:user.name} string)  
# 方式4：  获取shell参数    通过命令env查看shell下的所有环境变量的数据    
hive>create table t(name string, ${env:HOSTNAME} string)  

[root@chinadaas109 ~]# env  
HOSTNAME=chinadaas109  
TERM=vt100  
SHELL=/bin/bash  
HISTSIZE=1000  
.....  

hive (default)> create table ttttt(id string,${env:HOSTNAME});  
FAILED: Parse Error: line 1:41 cannot recognize input near ')' '<EOF>' '<EOF>' in column type  

hive (default)> create table ttttt(id string,${env:HOSTNAME} string);  
OK  
Time taken: 0.256 seconds  
hive (default)> desc ttttt;  
OK  
col_name        data_type       comment  
id      string  
chinadaas109    string  
Time taken: 0.254 seconds  
hive (default)>   

```


# 数据类型

## 基本数据类型：
- 整型

- 布尔

- 浮点

- 字符


- 复合数据类型：

Struct

Array

Map

- Array 实例
```bash
create table test1 (name string, student_id_list array<INT>) 
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
COLLECTION ITEMS TERMINATED BY ':';

cat array.txt
class1,1001:1002
class2,1001:1002

load data local inpath '/data/project/data/tmp/now/array.txt' into table test1;
```

- Struct 实例

```bash
structs内部的数据可以通过DOT（.）来存取，例如，表中一列c的类型为STRUCT{a INT; b INT}，我们可以通过c.a来访问域a  
create table test2(id INT, info struct<name:STRING, age:INT>)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
COLLECTION ITEMS TERMINATED BY ':';    

cat struct.txt 
1,f1:1002
2,f2:1003

load data local inpath '/data/project/data/tmp/now/struct.txt' into table test1;
```

- Map 实例

```bash
访问指定域可以通过["指定域名称"]进行，例如，一个Map M包含了一个group-》gid的kv对，gid的值可以通过M['group']来获取  
create table test3(id string, perf map<string, int>)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
COLLECTION ITEMS TERMINATED BY ','
MAP KEYS TERMINATED BY ':';

```

# 数据库定义

默认数据库"default"  

使用#hive命令后，不使用hive>use <数据库名>，系统默认的数据库。可以显式使用hive> use default;  

```bash
创建一个新库  
hive>CREATE DATABASE    
[IF NOT EXISTS] mydb    
[COMMENT] '....';  
[LOCATION] '/.......'    

hive>SHOW DATABASES;  

hive>DESCRIBE DATABASE [extended] mydb;  

hive>DROP DATABASE [IF EXISTS] mydb [CASCADE];  删除库的时候 级联删除库下对应的表  
```

# hive 索引

```bash
创建索引  
create index t1_index on table t1(name)as 'org.apache.hadoop.hive.ql.index.compact.CompactIndexHandler' with deferred rebuild in table t1_index_table;  
as指定索引器，   in table t1_index_table 可以不写,即简写成：  
create index t1_index on table t1(name)as 'org.apache.hadoop.hive.ql.index.compact.CompactIndexHandler' with deferred rebuild;  
全写下多出一张表t1_index_table；  
简写下多出一张表default__stu_stu_index__  
格式都为：  
hive (default)> desc default__stu_stu_index__;  
OK  
col_name        data_type       comment  
name                    string                                        
_bucketname             string                                        
_offsets                array<bigint>    

再次创建索引时,全写下需要指定别的表名, in table othertablename;   


重建索引   创建后还需要重建索引才能生效  创建仅仅是建立了关联 重建类似于初始化   
 alter index t1_index on t1 rebuild;  
显示索引  
show formatted index on t1;  
删除索引  
drop index  if exists t1_index on t1;  关键词 if exists可以不加  
```

# hive 执行计划

```bash
explain extended select id, info.name from test2;
```

# 查看文件块大小
```bash
hive查看默认文件块大小:
hive>set dfs.block.size;
```

# hive使用正则

