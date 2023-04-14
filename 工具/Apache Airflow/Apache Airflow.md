[What is Airflow? — Airflow Documentation --- 什么是气流？ — 气流文档 (apache.org)](https://airflow.apache.org/docs/apache-airflow/stable/index.html)

目前的直观理解是，Airflow是一个工作流可视化平台，可以：

- 在平台上显示工作任务
- 设定工作的执行顺序，比如有的工作需要先后顺序，就需要先完成任务A再去完成任务B
- 设定工作的执行周期等
- 设定工作流需要通过代码进行，而不是在平台上点击。就是说这玩意主要为程序员服务的，不会代码还不好操作这东西，因为你要按照Airflow的要求写代码来安排工作流。

然后我觉得下一步就是部署Airflow，实现一个最简单的应用看看效果。

> 尝试了在windows部署Airflow，遇到一些错误

下面尝试在Linux部署Airflow



## Airflow安装

首先用conda创建一个虚拟环境

```
conda create -n py39 python=3.9
```

> 然后根据chatgpt4 教的来安装airflow

以下是在您的Linux服务器上安装Airflow的逐步指南。我们将遵循官方文档并使用pip作为安装工具。在开始之前，请确保您已经安装了Python 3.9。

首先，我们需要为Python和Airflow创建一个新的虚拟环境。这样可以确保我们的安装不会干扰其他Python项目。打开终端并运行以下命令：

```
python3.9 -m venv airflow_venv
```

接下来，激活刚刚创建的虚拟环境：

```
source airflow_venv/bin/activate
```

使用以下命令安装Airflow（这个例子使用了Celery执行器，根据您的需求选择适当的执行器）：

```
AIRFLOW_VERSION=2.5.3
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
pip install "apache-airflow[celery]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

现在，Airflow应该已经安装完成。接下来，我们需要初始化Airflow的元数据库。运行以下命令：

```
airflow db init
```

创建一个Airflow用户并设置用户名和密码：

```
airflow users create --username <your_username> --password <your_password> --firstname <your_firstname> --lastname <your_lastname> --role Admin --email <your_email>

```

例如

```
airflow users create --username light --password 123456 --firstname L --lastname L --role Admin --email 435786117@qq.com

```



将 `<your_username>`，`<your_password>`，`<your_firstname>`，`<your_lastname>` 和 `<your_email>` 替换为您的个人信息。

最后，启动Airflow Web服务器：

```
airflow webserver --port 8080
```

在另一个终端中（不启动scheduler则无法显示dag）

```
airflow scheduler
```



打开浏览器并访问 [http://localhost:8080](http://localhost:8080/)

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
with DAG(dag_id="demo", start_date=datetime(2022, 1, 1), schedule="0 0 * * *") as dag:
    # Tasks are represented as operators
    hello = BashOperator(task_id="hello", bash_command="echo hello")

    @task()
    def airflow():
        print("airflow")

    # Set dependencies between tasks
    hello >> airflow()
```

这样就得到了一个dag。
