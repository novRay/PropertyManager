# PropertyManager

- 安装：
  - Python 3.8
  - MySQL 8.0
  - PyCharm
- 创建虚拟环境

```shell
pip install virtualenv
virtualenv venv
```

- 激活虚拟环境

```shell
./venv/Scripts/activate
```

- 安装依赖

```shell
pip install -r requirements.txt
```

- 数据库创建

```sql
create database property;
use property;
```

- 修改config.py里的配置信息，把用户名密码改成你自己电脑上的。

```python
DB_USER = 'root'
DB_PASSWORD = 'your_db_password'
DB_NAME = 'property'
```


- 启动程序（或者直接pycharm启动）

```shell
flask run
```

- 打开http://127.0.0.1:5000

