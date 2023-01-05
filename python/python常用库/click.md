# click

https://github.com/pallets/click

https://click.palletsprojects.com/en/8.1.x/quickstart/

### 基础用法

创建一个`helper.py`文件，输入：

```python
import click

@click.command()
def hello():
    click.echo('Hello World!')

if __name__ == '__main__':
    hello()
```

在命令行中

```
python helper.py
```

```
Hello World!
```

### 创建命令组

```python
import click

@click.group()
def cli():
    pass

@click.command()
def initdb():
    click.echo('Initialized the database')

@click.command()
def dropdb():
    click.echo('Dropped the database')

cli.add_command(initdb)
cli.add_command(dropdb)

if __name__ == '__main__':
    cli()
```

```
python helper initdb
```

```
Initialized the database
```

