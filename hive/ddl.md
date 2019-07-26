
[TOC]

# Alter Table/Partition/Column

## Alter Table

```bash
ALTER TABLE table_name RENAME TO new_table_name;


# 查看表的属性
desc formatted tablename;

# 将表table_name中的字段分割符修改成'\t',注意，这是在表没有分区的情况下
alter table table_name set serdepropertyes('field.delim'='\t');

alter table t9 partition(dt='20140901') set serdepropertyes('field.delim=\t');

alter table table_name[partition] set location 'path'
alter table table_name set TBLPROPERTIES('EXTERNAL'='TRUE');//内部表转化成外部表
alter table table_name set TBLPROPERTIES('EXTERNAL'='FALSE');//外部表转成内部表
```

## Alter Partition
```bash
ALTER TABLE table_name ADD [IF NOT EXISTS] PARTITION partition_spec 
  [LOCATION 'location1'] partition_spec [LOCATION 'location2'] ...;


ALTER TABLE table_name DROP [IF EXISTS] PARTITION partition_spec[, PARTITION partition_spec, ...]

ALTER TABLE table_name [PARTITION partition_spec] SET LOCATION "new location";

alter table table_name set location 'hdfs://cluster/home/table_name';
```

## alter columns
```bash

alter table tablename change column column_orign column_new int(修改后列的属性) comment 'column_name'
alter table tablename add columns(column1 string comment 'xxxx',column2 long comment 'yyyy')

参考手册
https://cwiki.apache.org/confluence/display/Hive/LanguageManual

http://www.cnblogs.com/sunfie/p/4375795.html

```

# 查看信息

```bash
hive> desc formatted tbName;

# 模糊查询表
hive> show tables like '*name*';


# 查询显示列名 及 行转列显示
set hive.cli.print.header=true; // 打印列名
set hive.cli.print.row.to.vertical=true; // 开启行转列功能, 前提必须开启打印列名功能
set hive.cli.print.row.to.vertical.num=1; // 设置每行显示的列数

# hive开启简单模式不启用mr
set hive.fetch.task.conversion=more;

# 以json格式输出执行语句会读取的input table和input partition信息
Explain dependency query  

```

# 常用函数

```sql
-- unix_timestamp() 当前系统时间
-- to_date(string timestamp) 将时间戳转换成日期型字符串
-- datediff(string enddate, string startdate) 返回int 的两个日期差
-- date_add(string startdate, int days) 日期加减
-- current_timestamp 返回当前时间戳
-- current_date 返回当前日期
-- date_format(date/timestamp/string ts, string fmt) 按照格式返回字符串
-- last_day(string date) 返回 当前时间的月末日期

-- trim(string A) 删除字符串两边的空格，中间的会保留
-- if(boolean testCondition, T valueTrue, T valueFalseOrNull) ，根据条件返回不同的值
-- nvl(T value, T default_value) 如果T is null ，返回默认值
-- length(string A) 返回字符串A的长度
-- greatest(T v1, T v2, ...) 返回最大值，会过滤null
-- least(T v1, T v2, ...) 返回最小值，会过滤null
-- rand(), 返回0-1的随机值。rand(INT seed) 返回固定的随机值
-- split(str, regex) ,安装规则截取字符串,返回数组

-- rpad(string str, int len, string pad) 将字符串str 用pad进行右补足 到len位(如果位数不足的话)
-- lpad(string str, int len, string pad) 将字符串str 用pad进行左补足 到len位(如果位数不足的话)
-- repeat(string str, int n) 重复N次字符串

-- regexp_replace(string A, string B, string C) 字符串替换函数，将字符串A 中的B 用 C 替换


```

# 常用DDL

## 三种建表方法
```sql
CREATE [TEMPORARY] [EXTERNAL] TABLE [IF NOT EXISTS] [db_name.]table_name    -- (Note: TEMPORARY available in Hive 0.14.0 and later)
  [(col_name data_type [COMMENT col_comment], ... [constraint_specification])]
  [COMMENT table_comment]
  [PARTITIONED BY (col_name data_type [COMMENT col_comment], ...)]
  [CLUSTERED BY (col_name, col_name, ...) [SORTED BY (col_name [ASC|DESC], ...)] INTO num_buckets BUCKETS]
  [SKEWED BY (col_name, col_name, ...)  -- (Note: Available in Hive 0.10.0 and later)]
     ON ((col_value, col_value, ...), (col_value, col_value, ...), ...)
     [STORED AS DIRECTORIES]
  [
   [ROW FORMAT row_format] 
   [STORED AS file_format]
     | STORED BY 'storage.handler.class.name' [WITH SERDEPROPERTIES (...)]  -- (Note: Available in Hive 0.6.0 and later)
  ]
  [LOCATION hdfs_path]
  [TBLPROPERTIES (property_name=property_value, ...)]   -- (Note: Available in Hive 0.6.0 and later)

[AS select_statement];   -- (Note: Available in Hive 0.5.0 and later; not supported for external tables)

CREATE [TEMPORARY] [EXTERNAL] TABLE [IF NOT EXISTS] [db_name.]table_name
  LIKE existing_table_or_view_name
  [LOCATION hdfs_path];
 
data_type
  : primitive_type
  | array_type
  | map_type
  | struct_type
  | union_type  -- (Note: Available in Hive 0.7.0 and later)
 
primitive_type
  : TINYINT
  | SMALLINT
  | INT
  | BIGINT
  | BOOLEAN
  | FLOAT
  | DOUBLE
  | DOUBLE PRECISION -- (Note: Available in Hive 2.2.0 and later)
  | STRING
  | BINARY      -- (Note: Available in Hive 0.8.0 and later)
  | TIMESTAMP   -- (Note: Available in Hive 0.8.0 and later)
  | DECIMAL     -- (Note: Available in Hive 0.11.0 and later)
  | DECIMAL(precision, scale)  -- (Note: Available in Hive 0.13.0 and later)
  | DATE        -- (Note: Available in Hive 0.12.0 and later)
  | VARCHAR     -- (Note: Available in Hive 0.12.0 and later)
  | CHAR        -- (Note: Available in Hive 0.13.0 and later)
 
array_type
  : ARRAY < data_type >
 
map_type
  : MAP < primitive_type, data_type >
 
struct_type
  : STRUCT < col_name : data_type [COMMENT col_comment], ...>
 
union_type
   : UNIONTYPE < data_type, data_type, ... >  -- (Note: Available in Hive 0.7.0 and later)
 
row_format
  : DELIMITED [FIELDS TERMINATED BY char [ESCAPED BY char]] [COLLECTION ITEMS TERMINATED BY char]
        [MAP KEYS TERMINATED BY char] [LINES TERMINATED BY char]
        [NULL DEFINED AS char]   -- (Note: Available in Hive 0.13 and later)
  | SERDE serde_name [WITH SERDEPROPERTIES (property_name=property_value, property_name=property_value, ...)]
 
file_format:
  : SEQUENCEFILE
  | TEXTFILE    -- (Default, depending on hive.default.fileformat configuration)
  | RCFILE      -- (Note: Available in Hive 0.6.0 and later)
  | ORC         -- (Note: Available in Hive 0.11.0 and later)
  | PARQUET     -- (Note: Available in Hive 0.13.0 and later)
  | AVRO        -- (Note: Available in Hive 0.14.0 and later)
  | INPUTFORMAT input_format_classname OUTPUTFORMAT output_format_classname
 
constraint_specification:
  : [, PRIMARY KEY (col_name, ...) DISABLE NOVALIDATE ]
    [, CONSTRAINT constraint_name FOREIGN KEY (col_name, ...) REFERENCES table_name(col_name, ...) DISABLE NOVALIDATE

-- 直接建表

-- 查询建表
CREATE TABLE new_key_value_store
   ROW FORMAT SERDE "org.apache.hadoop.hive.serde2.columnar.ColumnarSerDe"
   STORED AS RCFile
   AS
SELECT col1, col2
FROM key_value_store

-- like建表法，表结构相同，但是没有数据
CREATE TABLE empty_key_value_store
LIKE key_value_store;


```

## 列转行
```sql
-- collect_list 不去重，collect_set 去重
select user_id,
concat_ws(',',collect_list(order_id)) as order_value 
from tbl
group by user_id
limit 10;

```

## 行转列
```sql
-- explode(array): 每个元素生成一行; explode(map): key-value生成一行; explode不能增加其他字段
-- lateral view: 结合explode可以查询其他字段

select col1, col2
from tbl
lateral view explode(split(col, ',')) lateral_view_tbl as col2

-- 多个lateral view
SELECT myCol1, myCol2 FROM baseTable
LATERAL VIEW explode(col1) myTable1 AS myCol1
LATERAL VIEW explode(col2) myTable2 AS myCol2;

-- Outer Lateral Views
-- 如果array类型的字段为空，但依然需返回记录，可使用outer关键词。
-- 这条语句中的array字段是个空列表，这条语句不管src表中是否有记录，结果都是空的
select * from src LATERAL VIEW explode(array()) C AS a limit 5;

-- 结果中的记录数为src表的记录数，只是a字段为NULL
select * from src LATERAL VIEW OUTER explode(array()) C AS a limit 5;

```

## group_concat,concat, concat_ws
```sql
-- concat(str1, str2, ..., strn)
-- 返回结果为连接参数产生的字符串。如有任何一个参数为NULL ，则返回值为 NULL。可以有一个或多个参数

-- concat_ws(sep, str1, str2, ...)
-- 分隔符可以是一个字符串，也可以是其它参数。如果分隔符为 NULL，则结果为 NULL
-- CONCAT_WS()不会忽略任何空字符串,然而会忽略所有的 NULL

-- group_concat
GROUP_CONCAT([DISTINCT] expr [,expr ...]
[ORDER BY {unsigned_integer | col_name | formula} [ASC | DESC] [,col ...]]
[SEPARATOR str_val])

-- example
SELECT locus,GROUP_CONCAT(distinct id ORDER BY id DESC SEPARATOR '_') FROM info WHERE locus IN('AB086827','AF040764') GROUP BY locus

```


## 压缩
```sql

set hive.exec.compress.intermediate=true --启用中间数据压缩
SET hive.exec.compress.output=true; -- 启用最终数据输出压缩
set mapreduce.output.fileoutputformat.compress=true; --启用reduce输出压缩
-- set mapred.output.compression.codec=org.apache.hadoop.io.compress.GzipCodec
set mapreduce.output.fileoutputformat.compress.codec=org.apache.hadoop.io.compress.SnappyCodec --设置reduce输出压缩格式
set mapreduce.map.output.compress=true; --启用map输入压缩
set mapreduce.map.output.compress.codec=org.apache.hadoop.io.compress.SnappyCodec；-- 设置map输出压缩格式

-- 文本表
create table if not exists test1
(
unionid string,
label_name_en string,
label_val string
)
row format delimited
fields terminated by '\001'
location '/data/test1';

-- 压缩表ORC创建
create table if not exists test2
(
unionid string,
label_name_en string,
label_val string
)
row format delimited
fields terminated by '\001'
STORED AS ORC
location '/data/test2';

-- 插入数据
insert overwrite table test2
select unionid, label_name_en, label_val from test1

```


## 开窗分析函数

### 开窗规范
```sql
over (order by salary range between 5 preceding and 5 following)  -- 窗口范围为当前行数据幅度减5加5后的范围内的。
over (order by salary rows between 5 preceding and 5 following)   -- 窗口范围为当前行前后各移动5行。
over (order by salary range between unbounded preceding and unbounded following) -- 窗口不做限制
over (order by salary rows between unbounded preceding and unbounded following) -- 窗口不做限制


-- example range
--sum(s)over(order by s range between 2 preceding and 2 following) 表示加2或2的范围内的求和
select name,class,s, sum(s)over(order by s range between 2 preceding and 2 following) mm 
from t2
adf   3  45  45  --45加2减2即43到47，但是s在这个范围内只有45
asdf  3  55  55
cfe   2  74  74
3dd   3  78  158 --78在76到80范围内有78，80，求和得158
fda   1  80  158
gds   2  92  92
ffd   1  95  190
dss   1  95  190
ddd   3  99  198
gf    3  99  198

-- Example rows
--sum(s)over(order by s rows between 2 preceding and 2 following)表示在上下两行之间的范围内
select name,class,s, sum(s)over(order by s rows between 2 preceding and 2 following) mm 
from t2
adf   3  45  174  -- (45+55+74=174)
asdf  3  55  252  -- (45+55+74+78=252)
cfe   2  74  332  -- (74+55+45+78+80=332)
3dd   3  78  379  -- (78+74+55+80+92=379)
fda   1  80  419
gds   2  92  440
ffd   1  95  461
dss   1  95  480
ddd   3  99  388
gf    3  99  293

```

### 开窗函数
```sql
-- lead(expresstion,<offset>,<default>) over() 取出后N行
-- lag(expresstion,<offset>,<default>) over()  取出前N行

-- FIRST_VALUE() over()  -- 第一条记录
-- LAST_VALUE()  over()  -- 最后一条记录
```


### OVER与标准的聚合
```sql
-- COUNT
-- SUM
-- MIN
-- MAX
-- AVG
```

### 分析函数
```sql
-- ROW_NUMBER  		-- 生成唯一的编号，比如取第一名成绩的用户，如果是并列的用户只能取出一条
-- RANK 			-- rank可以将并列的第一名取出来；跳跃编号
-- DENSE_RANK 		-- 连续编号
-- ratio_to_report(a)函数用法 Ratio_to_report() 括号中就是分子，over() 括号中就是分母
-- CUME_DIST 		-- 所在组排名序号除以该组所有的行数，但是如果存在并列情况，则需加上并列的个数-1
-- PERCENT_RANK 	-- 所在组排名序号-1除以该组所有的行数-1
-- percentile_cont  -- 输入一个百分比（该百分比就是按照percent_rank函数计算的值），返回该百分比位置的平均值
-- PERCENTILE_DISC  -- 返回一个与输入的分布百分比值相对应的数据值，分布百分比的计算方法见函数CUME_DIST，如果没有正好对应的数据值，就取大于该分布值的下一个值。
-- NTILE
```
