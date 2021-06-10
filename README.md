# dbinterface

[![Build Status](https://travis-ci.com/somenzz/dbinterface.svg?branch=master)](https://travis-ci.com/somenzz/dbinterface)
[![Coverage Status](https://coveralls.io/repos/github/somenzz/dbinterface/badge.svg)](https://coveralls.io/github/somenzz/dbinterface)


Python 连接数据库，执行读写操作的通用接口，采用简单工厂模式，基于接口和组合进行编程。

## 安装

```sh
git clone  https://github.com/somenzz/dbinterface.git 
pip install -r requirements.txt
pip install dbinterface
```

## 使用方法


### 读取数据

```python

from dbinterface.database_client import DataBaseClientFactory

client1 = DataBaseClientFactory.create(
            dbtype="postgres",
            host="localhost",
            port=5432,
            user="postgres",
            pwd="121113",
            database="postgres",
        )
result1 = client1.read("select current_date")
for row in result1:
    #do something
    pass


client = DataBaseClientFactory.create(
            dbtype="mysql",
            host="localhost",
            port=3306,
            user="aaron",
            pwd="aaron",
            database="information_schema",
        )
result2 = client.read("select current_date()")

for row in result2:
    #do something
    pass

```


### 更新数据

```python

from dbinterface.database_client import DataBaseClientFactory

client1 = DataBaseClientFactory.create(
            dbtype="postgres",
            host="localhost",
            port=5432,
            user="postgres",
            pwd="121113",
            database="postgres",
        )

rows_affeted = client1.write(
    "insert into tmp_test_table values(%s, %s)", ("1", "aaron")
)
assert rows_affeted == 1
```


### 导出数据


```python

from dbinterface.database_client import DataBaseClientFactory

client = DataBaseClientFactory.create(
            dbtype="postgres",
            host="localhost",
            port=5432,
            user="postgres",
            pwd="121113",
            database="postgres",
        )

rows_export = client.export(
            "select * from information_schema.TABLES",
            params=(),
            file_path="/Users/aaron/tmp/mysql_tables.txt",
            delimeter="0x02",
            quote="0x03",
            all_col_as_str=False,
        )

assert rows_export > 0

```



### 获取表名列表


```python

from dbinterface.database_client import DataBaseClientFactory

client = DataBaseClientFactory.create(
            dbtype="postgres",
            host="localhost",
            port=5432,
            user="postgres",
            pwd="121113",
            database="postgres",
        )

table_list = client.get_tables()
for table in table_list:
    print(table['name'])
    print(table['type'])
    print(table['schema'])
    print(table['remarks'])

```


## 扩展

- 修改 database_interface.py 文件，添加新的函数

- 添加新的数据库，以 oracle 为例，在 dbinterface 目录下，新增 oracle_client.py 文件，参考其他 client 编写即可。

- 然后修改 dbinterface 目录下 database_client.py 文件，修改 DataBaseClientFactory 类，添加对应的数据库类型。
  
- tests 目录内添加单元测试，执行 pytess 测试


## 联系我

微信号 somenzz
公众号 「Python七号」