https://apscheduler.readthedocs.io/

APScheduler 是一个 Python 的定时任务框架，使用起来简单方便，功能也非常强大。使用 APScheduler 做到以下这些事情：

- 程序启动后，可以在任何时间点在后台线程运行作业。
- 在一段固定的时间间隔内运行作业，例如每隔5分钟或者每隔一小时。
- 在每天、每周或者每月的特定时间运行作业。
- 在特定的日期或者日期间隔运行作业。

安装

```
pip install apscheduler
```



基本用法

```python
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

def job_function():
    print("Hello World", datetime.now())

sched = BlockingScheduler()

# Schedule job_function to be called every two seconds
sched.add_job(job_function, 'interval', seconds=2)

sched.start()

```

`BlockingScheduler`，这意味着调度器会阻塞当前线程执行，直到调度器被关闭。

### 调度器类型

在 APScheduler 中，有三种类型的调度器，分别是：

- BlockingScheduler：这种调度器会阻塞当前线程执行，直到调度器被关闭。这对于脚本和命令行应用程序非常有用。
- BackgroundScheduler：这种调度器在后台线程运行，这对于GUI应用程序非常有用，因为你不希望GUI线程被阻塞。
- AsyncIOScheduler：这种调度器适用于使用 asyncio 库的应用程序。

如果你想要在 APScheduler 中并发执行任务，你可以创建多个 `BackgroundScheduler` 对象，每个对象在各自的后台线程中运行任务。但是，请注意，这可能会增加程序的复杂性，因为你需要管理多个调度器和它们各自的后台线程



### 任务添加

在 APScheduler 中，你可以添加多种类型的任务，包括：

- interval：间隔一定时间执行任务
- date：在某个日期/时间执行任务
- cron：在符合某种模式的日期/时间执行任务

例如

```python
# 在 2023 年 8 月 1 日 15:30 执行 job_function
sched.add_job(job_function, 'date', run_date=datetime(2023, 8, 1, 15, 30))

# 每隔 5 分钟执行一次 job_function
sched.add_job(job_function, 'interval', minutes=5)

# 每天早上 6:30 执行 job_function
sched.add_job(job_function, 'cron', hour='6', minute='30')

```

### 管理和控制作业

```python
# 添加一个作业并获取它的作业 id
job = sched.add_job(job_function, 'interval', minutes=5)
job_id = job.id

# 使用作业 id 来删除一个作业
sched.remove_job(job_id)

# 暂停一个作业
sched.pause_job(job_id)

# 恢复一个被暂停的作业
sched.resume_job(job_id)

# 列出所有的作业
jobs = sched.get_jobs()

```

### 常见使用场景

**1. Web 应用程序**

在 Web 应用程序中，你可能需要定期执行一些后台任务，例如清理旧数据、发送电子邮件通知或者更新缓存。这种情况下，你可以使用 APScheduler 来调度这些任务。

例如，如果你在使用 Flask，你可以这样做：

```python
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

def my_job():
    print("Job running...")

scheduler = BackgroundScheduler()
scheduler.add_job(my_job, 'interval', minutes=1)
scheduler.start()
```

**2. 数据分析和报告**

你可能需要定期收集和分析数据，然后生成报告。这种情况下，你可以使用 APScheduler 来调度收集和分析数据的任务。

```python
from apscheduler.schedulers.background import BackgroundScheduler

def collect_data():
    # Code to collect data...

def analyze_data():
    # Code to analyze data...

scheduler = BackgroundScheduler()
scheduler.add_job(collect_data, 'interval', hours=6)
scheduler.add_job(analyze_data, 'cron', hour='0')
scheduler.start()
```

**3. 自动化测试**

如果你正在进行软件测试，你可能需要定期运行一些测试任务，例如性能测试或者回归测试。这种情况下，你可以使用 APScheduler 来调度这些测试任务。

```python
from apscheduler.schedulers.background import BackgroundScheduler

def run_tests():
    # Code to run tests...

scheduler = BackgroundScheduler()
scheduler.add_job(run_tests, 'cron', day_of_week='mon-fri', hour='1')
scheduler.start()
```

**4. IoT（物联网）设备**

如果你正在开发 IoT 设备，你可能需要定期检查传感器的状态或者控制设备。这种情况下，你可以使用 APScheduler 来调度这些任务。

```python
from apscheduler.schedulers.background import BackgroundScheduler

def check_sensor():
    # Code to check sensor...

def control_device():
    # Code to control device...

scheduler = BackgroundScheduler()
scheduler.add_job(check_sensor, 'interval', seconds=10)
scheduler.add_job(control_device, 'cron', hour='0-23/2')
scheduler.start()
```

以上就是 APScheduler 的一些常见使用场景。当然，这只是一些基本的例子，你可以根据你自己的需求，使用 APScheduler 去调度任何你需要定期执行的任务。