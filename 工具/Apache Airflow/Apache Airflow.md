[What is Airflow? — Airflow Documentation --- 什么是气流？ — 气流文档 (apache.org)](https://airflow.apache.org/docs/apache-airflow/stable/index.html)

https://help.aliyun.com/document_detail/301707.html?spm=a2c4g.337789.0.0.3b3a798cHR7wcI

目前的直观理解是，Airflow是一个工作流可视化平台，可以：

- 在平台上显示工作任务
- 设定工作的执行顺序，比如有的工作需要先后顺序，就需要先完成任务A再去完成任务B
- 设定工作的执行周期等
- 设定工作流需要通过代码进行，而不是在平台上点击。就是说这玩意主要为程序员服务的，不会代码还不好操作这东西，因为你要按照Airflow的要求写代码来安排工作流。

然后我觉得下一步就是部署Airflow，实现一个最简单的应用看看效果。

> 尝试了在windows部署Airflow，遇到一些错误

下面尝试在Linux部署Airflow



## Airflow安装

创建新用户：可以在系统中创建一个Airflow用户用于管理

```
sudo useradd airflow -m -s /bin/bash
```

设置密码

```
sudo passwd airflow
```

如果python版本跟需要的版本不一致，可以用conda创建一个虚拟环境

```
conda create -n airflow python=3.9
conda activate airflow
```

创建文件夹便于管理

```
cd ~
mkdir airflow
cd airflow
```

当前路径应该是

```
pwd
> /home/airflow/airflow
```

创建虚拟环境

```
python -m venv venv
```

激活虚拟环境：

```
source venv/bin/activate
```

设置Airflow目录

```
export AIRFLOW_HOME=~/airflow
```



使用以下命令安装Airflow（这个例子使用了Celery执行器，根据您的需求选择适当的执行器）：

```
AIRFLOW_VERSION=2.6.3
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
pip install "apache-airflow[celery]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

Run Airflow Standalone

The `airflow standalone` command initializes the database, creates a user, and starts all components.

这条命令会初始化所有数据库、创建一个用户并开启所有组件

```
airflow standalone
```



根据经验，一般要手动安装pandas

```
pip install pandas
```

现在，Airflow应该已经安装完成。

初始化Airflow的元数据库。

```
airflow db init
```

如果报错（SQLite C library的版本太低）

```
airflow.exceptions.AirflowConfigException: error: sqlite C library version too old (< 3.15.0). See https://airflow.apache.org/docs/apache-airflow/2.5.3/howto/set-up-database.html#setting-up-a-sqlite-database
```

先检查 SQLite C 库版本

```
sqlite3 --version
```

更新

```
wget https://www.sqlite.org/src/tarball/sqlite.tar.gz
tar xzf sqlite.tar.gz
cd sqlite/
export CFLAGS="-DSQLITE_ENABLE_FTS3 \
    -DSQLITE_ENABLE_FTS3_PARENTHESIS \
    -DSQLITE_ENABLE_FTS4 \
    -DSQLITE_ENABLE_FTS5 \
    -DSQLITE_ENABLE_JSON1 \
    -DSQLITE_ENABLE_LOAD_EXTENSION \
    -DSQLITE_ENABLE_RTREE \
    -DSQLITE_ENABLE_STAT4 \
    -DSQLITE_ENABLE_UPDATE_DELETE_LIMIT \
    -DSQLITE_SOUNDEX \
    -DSQLITE_TEMP_STORE=3 \
    -DSQLITE_USE_URI \
    -O2 \
    -fPIC"
export PREFIX="/usr/local"
LIBS="-lm" ./configure --disable-tcl --enable-shared --enable-tempstore=always --prefix="$PREFIX"
make
make install
```

然后要设置环境变量

```
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
```



最后再启动

```
airflow db init
```



创建一个Airflow用户并设置用户名和密码：

```
airflow users create \
  --username <your_username> \
  --password <your_password> \
  --firstname <your_firstname> \
  --lastname <your_lastname> \
  --role Admin \
  --email <your_email>
```

例如

```
airflow users create \
  --username admin \
  --password 2zhlmcy \
  --firstname admin \
  --lastname admin \
  --role Admin \
  --email admin@admin.com

```

将 `<your_username>`，`<your_password>`，`<your_firstname>`，`<your_lastname>` 和 `<your_email>` 替换为您的个人信息。

最后，启动Airflow Web服务器：

```
airflow webserver --port 7070
```

在另一个终端中（不启动scheduler则无法显示dag）

```
airflow scheduler
```

后台启动这两个

```
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
nohup airflow webserver --port 7070 >/dev/null &
nohup airflow scheduler >/dev/null &
```



打开浏览器并访问 [http://localhost:7070](http://localhost:7070/)

现在，您已经在Linux服务器上成功安装了Airflow。如有需要，您可以按照官方文档进一步配置和定制Airflow。

## 第一个DAG

找到Airflow主目录的dags文件夹，不存在就创建，默认情况下在`~/airflow/dags`

在该目录下创建`my_first_dag.py`

```python
from datetime import datetime

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator

# A DAG represents a workflow, a collection of tasks
with DAG(dag_id="demo", start_date=datetime(2022, 1, 1), schedule="*/1 * * * *") as dag:
    # Tasks are represented as operators
    hello = BashOperator(task_id="hello", bash_command="echo hello")

    @task()
    def airflow():
        print("airflow")

    # Set dependencies between tasks
    hello >> airflow()
```

这样就得到了一个dag。
