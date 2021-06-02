# dbinterface

[![Build Status](https://travis-ci.com/somenzz/dbinterface.svg?branch=master)](https://travis-ci.com/somenzz/dbinterface)
[![Coverage Status](https://coveralls.io/repos/github/somenzz/dbinterface/badge.svg)](https://coveralls.io/github/somenzz/dbinterface)


Python 连接数据库，执行读写操作的通用接口。

## 安装

```sh
pip install dbinterface
```

## 使用方法

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

client = DataBaseClientFactory.create(
            dbtype="mysql",
            host="localhost",
            port=3306,
            user="aaron",
            pwd="aaron",
            database="information_schema",
        )
result2 = client.read("select current_date()")

```

## 扩展

以 oracle 为例，在 dbinterface 目录下，新增 oracle_client.py 文件，参考其他 client 编写即可。

然后修改 dbinterface 目录下 database_client.py 文件，修改 DataBaseClientFactory 类，添加对应的数据库类型。

