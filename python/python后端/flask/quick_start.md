参考来自：https://github.com/greyli/flask-tutorial

# 3.模板

https://jinja.palletsprojects.com/en/3.0.x/templates/

在模板里，你需要添加特定的定界符将 Jinja2 语句和变量标记出来，下面是三种常用的定界符：

- `{{ ... }}` 用来标记变量。
- `{% ... %}` 用来标记语句，比如 if 语句，for 语句等。
- `{# ... #}` 用来写注释。

过滤器

例如，创建了一个python对象如下

```python
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
]
```

采用如下语句遍历`movies`

```jinja2
<p>{{ movies|length }} Titles</p>
<ul>
    {% for movie in movies %}  {# 迭代 movies 变量 #}
    <li>{{ movie.title }} - {{ movie.year }}</li> 
    {% endfor %}  {# 使用 endfor 标签结束 for 语句 #}
</ul>
```

`{{ movies|length }} `就相当于`len(movies)`

`{{ movie.title }}`相当于`movie['title']`

> 提示
>
> * 使用 [Faker](https://github.com/joke2k/faker) 可以实现自动生成虚拟数据，它支持丰富的数据类型，比如时间、人名、地名、随机字符等。
> * 除了过滤器，Jinja2 还在模板中提供了一些测试器、全局函数可以使用；除此之外，还有更丰富的控制结构支持，有一些我们会在后面学习到，更多的内容则可以访问 [Jinja2 文档](http://jinja.pocoo.org/docs/2.10/templates/)学习。

# 4.静态文件

静态文件（static files）指的是内容不需要动态生成的文件。比如图片、CSS 文件和 JavaScript 脚本等。

在项目根目录创建静态文件夹：

```bash
mkdir static
```

## 生成静态文件URL

通过Flask提供的`url_for()`来引入静态文件

假如我们在 static 文件夹的根目录下面放了一个 foo.jpg 文件，下面的调用可以获取它的 URL：

```jinja2
<img src="{{ url_for('static', filename='foo.jpg') }}">
```

花括号部分的调用会返回 `/static/foo.jpg`。

> **提示** 在 Python 脚本里，`url_for()` 函数需要从 `flask` 包中导入，而在模板中则可以直接使用，因为 Flask 把一些常用的函数和对象添加到了模板上下文（环境）里。

通常会在`/static`文件夹下创建一个`images`目录

然后图片放到`/static/images`里

## 引入Favicon

Favicon（favourite icon） 是显示在标签页和书签栏的网站头像。你需要准备一个 ICO、PNG 或 GIF 格式的图片，大小一般为 16×16、32×32、48×48 或 64×64 像素。

```html
<head>
    ...
    <link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}">
</head>
```



## 引入CSS

格式如下

```html
<head>
    ...
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}" type="text/css">
</head>
```

# 5.数据库

使用 [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/) 

```bash
pip install flask-sqlalchemy
```

导入扩展类，实例化并传入 Flask 程序实例：

```python
# 导入扩展类
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# 初始化扩展，传入程序实例 app
db = SQLAlchemy(app)
```

## 设置数据库 URI

为了设置 Flask、扩展或是我们程序本身的一些行为，我们需要设置和定义一些配置变量。Flask 提供了一个统一的接口来写入和获取这些配置变量：`Flask.config` 字典。配置变量的名称必须使用大写，写入配置的语句一般会放到扩展类实例化语句之前。

下面写入了一个 `SQLALCHEMY_DATABASE_URI` 变量来告诉 SQLAlchemy 数据库连接地址：

```python
import os

prefix = 'sqlite:///'  # windows 3斜线 linux 4斜线
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)
```

## 创建数据库模型

```python
# 表名将会是 user（自动生成，小写处理）
class User(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    
# 表名将会是 movie
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))
```

模型编写

- 模型类要声明继承 `db.Model`。
- 每一个类属性（字段）要实例化 `db.Column`，传入的参数为字段的类型，下面的表格列出了常用的字段类。
- 在 `db.Column()` 中添加额外的选项（参数）可以对字段进行设置。比如，`primary_key` 设置当前字段是否为主键。除此之外，常用的选项还有 `nullable`（布尔值，是否允许为空值）、`index`（布尔值，是否设置索引）、`unique`（布尔值，是否允许重复值）、`default`（设置默认值）等。

常用的字段类型如下表所示：

| 字段类           | 说明                                          |
| ---------------- | --------------------------------------------- |
| db.Integer       | 整型                                          |
| db.String (size) | 字符串，size 为最大长度，比如 `db.String(20)` |
| db.Text          | 长文本                                        |
| db.DateTime      | 时间日期，Python `datetime` 对象              |
| db.Float         | 浮点数                                        |
| db.Boolean       | 布尔值                                        |

## 创建数据库表

模型类创建后，还不能对数据库进行操作，因为我们还没有创建表和数据库文件。下面在 Python Shell 中创建了它们：

```
(env) $ flask shell
>>> from app import db
>>> db.create_all()
```

打开文件管理器，你会发现项目根目录下出现了新创建的数据库文件 data.db。

如果你改动了模型类，想重新生成表模式，那么需要先使用 `db.drop_all()` 删除表，然后重新创建：

```
>>> db.drop_all()
>>> db.create_all()
```

注意这会一并删除所有数据，如果你想在不破坏数据库内的数据的前提下变更表的结构，需要使用数据库迁移工具，比如集成了 [Alembic](https://alembic.sqlalchemy.org/en/latest/) 的 [Flask-Migrate](https://github.com/miguelgrinberg/Flask-Migrate) 扩展。

> **提示** 上面打开 Python Shell 使用的是 `flask shell`命令，而不是 `python`。使用这个命令启动的 Python Shell 激活了“程序上下文”，它包含一些特殊变量，这对于某些操作是必须的（比如上面的 `db.create_all()`调用）。请记住，后续的 Python Shell 都会使用这个命令打开。

和 `flask shell`类似，我们可以编写一个自定义命令来自动执行创建数据库表操作：

*app.py：自定义命令 initdb*

```python
import click

@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息
```

默认情况下，函数名称就是命令的名字，现在执行 `flask initdb` 命令就可以创建数据库表：

```bash
flask initdb
```

使用 `--drop` 选项可以删除表后重新创建：

```bash
flask initdb --drop
```

## 创建、读取、更新、删除

在前面打开的 Python Shell 里，我们来测试一下常见的数据库操作。你可以跟着示例代码来操作，也可以自由练习。

### 创建

下面的操作演示了如何向数据库中添加记录：

```python
from app import User, Movie  # 导入模型类
user = User(name='Grey Li')  # 创建一个 User 记录
m1 = Movie(title='Leon', year='1994')  # 创建一个 Movie 记录
m2 = Movie(title='Mahjong', year='1996')  # 再创建一个 Movie 记录
db.session.add(user)  # 把新创建的记录添加到数据库会话
db.session.add(m1)
db.session.add(m2)
db.session.commit()  # 提交数据库会话，只需要在最后调用一次即可
```

> **提示** 在实例化模型类的时候，我们并没有传入 `id` 字段（主键），因为 SQLAlchemy 会自动处理这个字段。

最后一行 `db.session.commit()` 很重要，只有调用了这一行才会真正把记录提交进数据库，前面的 `db.session.add()` 调用是将改动添加进数据库会话（一个临时区域）中。

### 读取

通过对模型类的 `query` 属性调用可选的过滤方法和查询方法，我们就可以获取到对应的单个或多个记录（记录以模型类实例的形式表示）。查询语句的格式如下：

```python
<模型类>.query.<过滤方法（可选）>.<查询方法>
```

下面是一些常用的过滤方法：

| 过滤方法    | 说明                                                         |
| ----------- | ------------------------------------------------------------ |
| filter()    | 使用指定的规则过滤记录，返回新产生的查询对象                 |
| filter_by() | 使用指定规则过滤记录（以关键字表达式的形式），返回新产生的查询对象 |
| order_by()  | 根据指定条件对记录进行排序，返回新产生的查询对象             |
| group_by()  | 根据指定条件对记录进行分组，返回新产生的查询对象             |

下面是一些常用的查询方法：

| 查询方法       | 说明                                                         |
| -------------- | ------------------------------------------------------------ |
| all()          | 返回包含所有查询记录的列表                                   |
| first()        | 返回查询的第一条记录，如果未找到，则返回 None                |
| get(id)        | 传入主键值作为参数，返回指定主键值的记录，如果未找到，则返回 None |
| count()        | 返回查询结果的数量                                           |
| first_or_404() | 返回查询的第一条记录，如果未找到，则返回 404 错误响应        |
| get_or_404(id) | 传入主键值作为参数，返回指定主键值的记录，如果未找到，则返回 404 错误响应 |
| paginate()     | 返回一个 Pagination 对象，可以对记录进行分页处理             |

下面的操作演示了如何从数据库中读取记录，并进行简单的查询：

```python
from app import Movie  # 导入模型类
movie = Movie.query.first()  # 获取 Movie 模型的第一个记录（返回模型类实例）
movie.title  # 对返回的模型类实例调用属性即可获取记录的各字段数据
# 'Leon'
movie.year
# '1994'
Movie.query.all()  # 获取 Movie 模型的所有记录，返回包含多个模型类实例的列表
# [<Movie 1>, <Movie 2>]
Movie.query.count()  # 获取 Movie 模型所有记录的数量
# 2
Movie.query.get(1)  # 获取主键值为 1 的记录
# <Movie 1>
Movie.query.filter_by(title='Mahjong').first()  # 获取 title 字段值为 Mahjong 的记录
# <Movie 2>
Movie.query.filter(Movie.title=='Mahjong').first()  # 等同于上面的查询，但使用不同的过滤方法
# <Movie 2>
```

> **提示** 我们在说 Movie 模型的时候，实际指的是数据库中的 movie 表。表的实际名称是模型类的小写形式（自动生成），如果你想自己指定表名，可以定义 `__tablename__` 属性。

对于最基础的 `filter()` 过滤方法，SQLAlchemy 支持丰富的查询操作符，具体可以访问[文档相关页面](http://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.operators.ColumnOperators)查看。除此之外，还有更多的查询方法、过滤方法和数据库函数可以使用，具体可以访问文档的 [Query API](https://docs.sqlalchemy.org/en/latest/orm/query.html) 部分查看。

### 更新

下面的操作更新了 `Movie` 模型中主键为 `2` 的记录：

```python
movie = Movie.query.get(2)
movie.title = 'WALL-E'  # 直接对实例属性赋予新的值即可
movie.year = '2008'
db.session.commit()  # 注意仍然需要调用这一行来提交改动
```

### 删除

下面的操作删除了 `Movie` 模型中主键为 `1` 的记录：

```python
movie = Movie.query.get(1)
db.session.delete(movie)  # 使用 db.session.delete() 方法删除记录，传入模型实例
db.session.commit()  # 提交改动
```

## 在程序里操作数据库

经过上面的一番练习，我们可以在 Watchlist 里进行实际的数据库操作了。

### 在主页视图读取数据库记录

因为设置了数据库，负责显示主页的 `index` 可以从数据库里读取真实的数据：

```python
@app.route('/')
def index():
    user = User.query.first()  # 读取用户记录
    movies = Movie.query.all()  # 读取所有电影记录
    return render_template('index.html', user=user, movies=movies)
```

在 `index` 视图中，原来传入模板的 `name` 变量被 `user` 实例取代，模板 index.html 中的两处 `name` 变量也要相应的更新为 `user.name` 属性：

```jinja2
{{ user.name }}'s Watchlist
```

### 生成虚拟数据

因为有了数据库，我们可以编写一个命令函数把虚拟数据添加到数据库里。下面是用来生成虚拟数据的命令函数：

*app.py：创建自定义命令 forge*

```python
import click

@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()
    
    # 全局的两个变量移动到这个函数内
    name = 'Grey Li'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]
    
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    
    db.session.commit()
    click.echo('Done.')
```

现在执行 `flask forge` 命令就会把所有虚拟数据添加到数据库里：

```bash
(env) $ flask forge
```

## 本章小结

本章我们学习了使用 SQLAlchemy 操作数据库，后面你会慢慢熟悉相关的操作。结束前，让我们提交代码：

```bash
$ git add .
$ git commit -m "Add database support with Flask-SQLAlchemy"
$ git push
```

> **提示** 你可以在 GitHub 上查看本书示例程序的对应 commit：[4d2442a](https://github.com/greyli/watchlist/commit/4d2442a41e55fb454e092864206af08e4e3eeddf)。

## 进阶提示

* 在生产环境，你可以更换更合适的 DBMS，因为 SQLAlchemy 支持多种 SQL 数据库引擎，通常只需要改动非常少的代码。
* 我们的程序只有一个用户，所以没有将 User 表和 Movie 表建立关联。访问 Flask-SQLAlchemy 文档的“[声明模型](http://flask-sqlalchemy.pocoo.org/2.3/models/#one-to-many-relationships)”章节可以看到相关内容。 
* 阅读 [SQLAlchemy 官方文档和教程](https://docs.sqlalchemy.org/en/latest/)详细了解它的用法。注意我们在这里使用 Flask-SQLAlchemy 来集成它，所以用法和单独使用 SQLAlchemy 有一些不同。作为参考，你可以同时阅读 [Flask-SQLAlchemy 官方文档](http://flask-sqlalchemy.pocoo.org/2.3/)。
* 如果你是[《Flask Web 开发实战》](http://helloflask.com/book/)的读者，第 5 章详细介绍了 SQLAlchemy 和 Flask-Migrate 的使用，第 8 章和第 9 章引入了更复杂的模型关系和查询方法。

# 6.模板优化

## 自定义错误页面

为了引出相关知识点，我们首先要为 Watchlist 编写一个错误页面。目前的程序中，如果你访问一个不存在的 URL，比如 /hello，Flask 会自动返回一个 404 错误响应。默认的错误页面非常简陋，如下图所示：

![默认的 404 错误页面](images/6-1.png)

在 Flask 程序中自定义错误页面非常简单，我们先编写一个 404 错误页面模板，如下所示：

*templates/404.html：404 错误页面模板*

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{{ user.name }}'s Watchlist</title>
    <link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}" type="text/css">
</head>
<body>
    <h2>
        <img alt="Avatar" class="avatar" src="{{ url_for('static', filename='images/avatar.png') }}">
        {{ user.name }}'s Watchlist
    </h2>
    <ul class="movie-list">
        <li>
            Page Not Found - 404
            <span class="float-right">
                <a href="{{ url_for('index') }}">Go Back</a>
            </span>
        </li>
    </ul>
    <footer>
        <small>&copy; 2018 <a href="http://helloflask.com/tutorial">HelloFlask</a></small>
	</footer>
</body>
</html>
```

接着使用 `app.errorhandler()` 装饰器注册一个错误处理函数，它的作用和视图函数类似，当 404 错误发生时，这个函数会被触发，返回值会作为响应主体返回给客户端：

*app.py：404 错误处理函数*

```python
@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    user = User.query.first()
    return render_template('404.html', user=user), 404  # 返回模板和状态码
```

> **提示** 和我们前面编写的视图函数相比，这个函数返回了状态码作为第二个参数，普通的视图函数之所以不用写出状态码，是因为默认会使用 200 状态码，表示成功。

这个视图返回渲染好的错误模板，因为模板中使用了 user 变量，这里也要一并传入。现在访问一个不存在的 URL，会显示我们自定义的错误页面：

![自定义 404 错误页面](images/6-2.png)

编写完这部分代码后，你会发现两个问题：

* 错误页面和主页都需要使用 user 变量，所以在对应的处理函数里都要查询数据库并传入 user 变量。因为每一个页面都需要获取用户名显示在页面顶部，如果有更多的页面，那么每一个对应的视图函数都要重复传入这个变量。
* 错误页面模板和主页模板有大量重复的代码，比如 `<head>` 标签的内容，页首的标题，页脚信息等。这种重复不仅带来不必要的工作量，而且会让修改变得更加麻烦。举例来说，如果页脚信息需要更新，那么每个页面都要一一进行修改。

显而易见，这两个问题有更优雅的处理方法，下面我们来一一了解。

## 模板上下文处理函数

对于多个模板内都需要使用的变量，我们可以使用 `app.context_processor` 装饰器注册一个模板上下文处理函数，如下所示：

*app.py：模板上下文处理函数*

```python
@app.context_processor
def inject_user():  # 函数名可以随意修改
    user = User.query.first()
    return dict(user=user)  # 需要返回字典，等同于 return {'user': user}
```

这个函数返回的变量（以字典键值对的形式）将会统一注入到每一个模板的上下文环境中，因此可以直接在模板中使用。

现在我们可以删除 404 错误处理函数和主页视图函数中的 `user` 变量定义，并删除在 `render_template()` 函数里传入的关键字参数：

```python
@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)
```

同样的，后面我们创建的任意一个模板，都可以在模板中直接使用 `user` 变量。

## 使用模板继承组织模板

对于模板内容重复的问题，Jinja2 提供了模板继承的支持。这个机制和 Python 类继承非常类似：我们可以定义一个父模板，一般会称之为基模板（base template）。基模板中包含完整的 HTML 结构和导航栏、页首、页脚等通用部分。在子模板里，我们可以使用 `extends` 标签来声明继承自某个基模板。

基模板中需要在实际的子模板中追加或重写的部分则可以定义成块（block）。块使用 `block` 标签创建， `{% block 块名称 %}` 作为开始标记，`{% endblock %}` 或 `{% endblock 块名称 %}` 作为结束标记。通过在子模板里定义一个同样名称的块，你可以向基模板的对应块位置追加或重写内容。

### 编写基础模板

下面是新编写的基模板 base.html：

*templates/base.html：基模板*

```html
<!DOCTYPE html>
<html lang="en">
<head>
    {% block head %}
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ user.name }}'s Watchlist</title>
    <link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}" type="text/css">
    {% endblock %}
</head>
<body>
    <h2>
        <img alt="Avatar" class="avatar" src="{{ url_for('static', filename='images/avatar.png') }}">
        {{ user.name }}'s Watchlist
    </h2>
    <nav>
        <ul>
            <li><a href="{{ url_for('index') }}">Home</a></li>
        </ul>
    </nav>
    {% block content %}{% endblock %}
    <footer>
        <small>&copy; 2018 <a href="http://helloflask.com/tutorial">HelloFlask</a></small>
	</footer>
</body>
</html>
```

在基模板里，我们添加了两个块，一个是包含 `<head></head>` 内容的 `head` 块，另一个是用来在子模板中插入页面主体内容的 `content` 块。在复杂的项目里，你可以定义更多的块，方便在子模板中对基模板的各个部分插入内容。另外，块的名字没有特定要求，你可以自由修改。

在编写子模板之前，我们先来看一下基模板中的两处新变化。

第一处，我们添加了一个新的 `<meta>` 元素，这个元素会设置页面的视口，让页面根据设备的宽度来自动缩放页面，让移动设备拥有更好的浏览体验：

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

第二处，新的页面添加了一个导航栏：

```html
<nav>
    <ul>
        <li><a href="{{ url_for('index') }}">Home</a></li>
    </ul>
</nav>
```

导航栏对应的 CSS 代码如下所示：

```css
nav ul {
    list-style-type: none;
    margin: 0;
    padding: 0;
    overflow: hidden;
    background-color: #333;
}

nav li {
    float: left;
}

nav li a {
    display: block;
    color: white;
    text-align: center;
    padding: 8px 12px;
    text-decoration: none;
}

nav li a:hover {
    background-color: #111;
}
```

### 编写子模板

创建了基模板后，子模板的编写会变得非常简单。下面是新的主页模板（index.html）：

*templates/index.html：继承基模板的主页模板*

```html
{% extends 'base.html' %}

{% block content %}
<p>{{ movies|length }} Titles</p>
<ul class="movie-list">
    {% for movie in movies %}
    <li>{{ movie.title }} - {{ movie.year }}
        <span class="float-right">
            <a class="imdb" href="https://www.imdb.com/find?q={{ movie.title }}" target="_blank" title="Find this movie on IMDb">IMDb</a>
        </span>
    </li>
    {% endfor %}
</ul>
<img alt="Walking Totoro" class="totoro" src="{{ url_for('static', filename='images/totoro.gif') }}" title="to~to~ro~">
{% endblock %}
```

第一行使用 `extends` 标签声明扩展自模板 base.html，可以理解成“这个模板继承自 base.html“。接着我们定义了 `content` 块，这里的内容会插入到基模板中 `content` 块的位置。

> **提示** 默认的块重写行为是覆盖，如果你想向父块里追加内容，可以在子块中使用 `super()` 声明，即 `{{ super() }}`。

404 错误页面的模板类似，如下所示：

*templates/404.html：继承基模板的 404 错误页面模板*

```html
{% extends 'base.html' %}

{% block content %}
<ul class="movie-list">
    <li>
        Page Not Found - 404
        <span class="float-right">
            <a href="{{ url_for('index') }}">Go Back</a>
        </span>
    </li>
</ul>
{% endblock %}
```

## 添加 IMDb 链接

在主页模板里，我们还为每一个电影条目右侧添加了一个 IMDb 链接：

```html
<span class="float-right">
    <a class="imdb" href="https://www.imdb.com/find?q={{ movie.title }}" target="_blank" title="Find this movie on IMDb">IMDb</a>
</span>
```

这个链接的 `href` 属性的值为 IMDb 搜索页面的 URL，搜索关键词通过查询参数 `q` 传入，这里传入了电影的标题。

对应的 CSS 定义如下所示：

```css
.float-right {
    float: right;
}

.imdb {
    font-size: 12px;
    font-weight: bold;
    color: black;
    text-decoration: none;
    background: #F5C518;
    border-radius: 5px;
    padding: 3px 5px;
}
```

现在，我们的程序主页如下所示：

![添加导航栏和 IMDb 链接](images/6-3.png)

## 本章小结

本章我们主要学习了 Jinja2 的模板继承机制，去掉了大量的重复代码，这让后续的模板编写工作变得更加轻松。结束前，让我们提交代码：

```bash
git add .
git commit -m "Add base template and error template"
git push
```

> **提示** 你可以在 GitHub 上查看本书示例程序的对应 commit：[3bca489](https://github.com/greyli/watchlist/commit/3bca489421cc498289734cfef9d6ff90232df8be)。

## 进阶提示

* 本章介绍的自定义错误页面是为了引出两个重要的知识点，因此并没有着重介绍错误页面本身。这里只为 404 错误编写了自定义错误页面，对于另外两个常见的错误 400 错误和 500 错误，你可以自己试着为它们编写错误处理函数和对应的模板。
* 因为示例程序的语言和电影标题使用了英文，所以电影网站的搜索链接使用了 IMDb，对于中文，你可以使用豆瓣电影或时光网。以豆瓣电影为例，它的搜索链接为 <https://movie.douban.com/subject_search?search_text=关键词>，对应的 `href` 属性即 `https://movie.douban.com/subject_search?search_text={{ movie.title }}`。
* 因为基模板会被所有其他页面模板继承，如果你在基模板中使用了某个变量，那么这个变量也需要使用模板上下文处理函数注入到模板里。

# 7.表单

在 HTML 页面里，我们需要编写表单来获取用户输入。一个典型的表单如下所示：

```html
<form method="post">  <!-- 指定提交方法为 POST -->
    <label for="name">名字</label>
    <input type="text" name="name" id="name"><br>  <!-- 文本输入框 -->
    <label for="occupation">职业</label>
    <input type="text" name="occupation" id="occupation"><br>  <!-- 文本输入框 -->
    <input type="submit" name="submit" value="登录">  <!-- 提交按钮 -->
</form>
```

编写表单的 HTML 代码有下面几点需要注意：

* 在 `<form>` 标签里使用 `method` 属性将提交表单数据的 HTTP 请求方法指定为 POST。如果不指定，则会默认使用 GET 方法，这会将表单数据通过 URL 提交，容易导致数据泄露，而且不适用于包含大量数据的情况。
* `<input>` 元素必须要指定 `name`  属性，否则无法提交数据，在服务器端，我们也需要通过这个 `name` 属性值来获取对应字段的数据。

> **提示** 填写输入框标签文字的 `<label>` 元素不是必须的，只是为了辅助鼠标用户。当使用鼠标点击标签文字时，会自动激活对应的输入框，这对复选框来说比较有用。`for` 属性填入要绑定的 `<input>` 元素的 `id` 属性值。

## 创建新条目

创建新条目可以放到一个新的页面来实现，也可以直接在主页实现。这里我们采用后者，首先在主页模板里添加一个表单：

*templates/index.html：添加创建新条目表单*

```html
<p>{{ movies|length }} Titles</p>
<form method="post">
    Name <input type="text" name="title" autocomplete="off" required>
    Year <input type="text" name="year" autocomplete="off" required>
    <input class="btn" type="submit" name="submit" value="Add">
</form>
```

在这两个输入字段中，`autocomplete` 属性设为 `off` 来关闭自动完成（按下输入框不显示历史输入记录）；另外还添加了 `required` 标志属性，如果用户没有输入内容就按下了提交按钮，浏览器会显示错误提示。

两个输入框和提交按钮相关的 CSS 定义如下：

```css
/* 覆盖某些浏览器对 input 元素定义的字体 */
input[type=submit] {
    font-family: inherit;
}

input[type=text] {
    border: 1px solid #ddd;
}

input[name=year] {
    width: 50px;
}

.btn {
    font-size: 12px;
    padding: 3px 5px;
    text-decoration: none;
    cursor: pointer;
    background-color: white;
    color: black;
    border: 1px solid #555555;
    border-radius: 5px;
}

.btn:hover {
    text-decoration: none;
    background-color: black;
    color: white;
    border: 1px solid black;
}
```

接下来，我们需要考虑如何获取提交的表单数据。

## 处理表单数据

默认情况下，当表单中的提交按钮被按下，浏览器会创建一个新的请求，默认发往当前 URL（在 `<form>` 元素使用 `action` 属性可以自定义目标 URL）。

因为我们在模板里为表单定义了 POST 方法，当你输入数据，按下提交按钮，一个携带输入信息的 POST 请求会发往根地址。接着，你会看到一个 405 Method Not Allowed 错误提示。这是因为处理根地址请求的 `index` 视图默认只接受 GET 请求。

> **提示** 在 HTTP 中，GET 和 POST 是两种最常见的请求方法，其中 GET 请求用来获取资源，而 POST 则用来创建 / 更新资源。我们访问一个链接时会发送 GET 请求，而提交表单通常会发送 POST 请求。

为了能够处理 POST 请求，我们需要修改一下视图函数：

```python
@app.route('/', methods=['GET', 'POST'])
```

在 `app.route()` 装饰器里，我们可以用 `methods` 关键字传递一个包含 HTTP 方法字符串的列表，表示这个视图函数处理哪种方法类型的请求。默认只接受 GET 请求，上面的写法表示同时接受 GET 和 POST 请求。

两种方法的请求有不同的处理逻辑：对于 GET 请求，返回渲染后的页面；对于 POST 请求，则获取提交的表单数据并保存。为了在函数内加以区分，我们添加一个 if 判断：

*app.py：创建电影条目*

```python
from flask import request, url_for, redirect, flash

# ...

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # 判断是否是 POST 请求
        # 获取表单数据
        title = request.form.get('title')  # 传入表单对应输入字段的 name 值
        year = request.form.get('year')
        # 验证数据
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页
        # 保存表单数据到数据库
        movie = Movie(title=title, year=year)  # 创建记录
        db.session.add(movie)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash('Item created.')  # 显示成功创建的提示
        return redirect(url_for('index'))  # 重定向回主页

    movies = Movie.query.all()
    return render_template('index.html', movies=movies)
```

在 `if` 语句内，我们编写了处理表单数据的代码，其中涉及 3 个新的知识点，下面来一一了解。

### 请求对象

Flask 会在请求触发后把请求信息放到 `request` 对象里，你可以从 `flask` 包导入它：

```python
from flask import request
```

因为它在请求触发时才会包含数据，所以你只能在视图函数内部调用它。它包含请求相关的所有信息，比如请求的路径（`request.path`）、请求的方法（`request.method`）、表单数据（`request.form`）、查询字符串（`request.args`）等等。

在上面的 `if` 语句中，我们首先通过 `request.method` 的值来判断请求方法。在 `if` 语句内，我们通过 `request.form` 来获取表单数据。`request.form` 是一个特殊的字典，用表单字段的 `name` 属性值可以获取用户填入的对应数据：

```python
if request.method == 'POST':
    title = request.form.get('title')
    year = request.form.get('year')
```

### flash 消息

在用户执行某些动作后，我们通常在页面上显示一个提示消息。最简单的实现就是在视图函数里定义一个包含消息内容的变量，传入模板，然后在模板里渲染显示它。因为这个需求很常用，Flask 内置了相关的函数。其中 `flash()` 函数用来在视图函数里向模板传递提示消息，`get_flashed_messages()` 函数则用来在模板中获取提示消息。

`flash()` 的用法很简单，首先从 `flask` 包导入 `flash` 函数：

```python
from flask import flash
```

然后在视图函数里调用，传入要显示的消息内容：

```python
flash('Item Created.')
```

`flash()` 函数在内部会把消息存储到 Flask 提供的 `session` 对象里。`session` 用来在请求间存储数据，它会把数据签名后存储到浏览器的 Cookie 中，所以我们需要设置签名所需的密钥：

```python
app.config['SECRET_KEY'] = 'dev'  # 等同于 app.secret_key = 'dev'
```

> **提示** 这个密钥的值在开发时可以随便设置。基于安全的考虑，在部署时应该设置为随机字符，且不应该明文写在代码里， 在部署章节会详细介绍。

下面在基模板（base.html）里使用 `get_flashed_messages()` 函数获取提示消息并显示：

```python
<!-- 插入到页面标题上方 -->
{% for message in get_flashed_messages() %}
	<div class="alert">{{ message }}</div>
{% endfor %}
<h2>...</h2>
```

`alert` 类为提示消息增加样式：

```css
.alert {
    position: relative;
    padding: 7px;
    margin: 7px 0;
    border: 1px solid transparent;
    color: #004085;
    background-color: #cce5ff;
    border-color: #b8daff;
    border-radius: 5px;
}
```

通过在 `<input>` 元素内添加 `required` 属性实现的验证（客户端验证）并不完全可靠，我们还要在服务器端追加验证：

```python
if not title or not year or len(year) != 4 or len(title) > 60:
    flash('Invalid input.')  # 显示错误提示
    return redirect(url_for('index'))
# ...
flash('Item created.')  # 显示成功创建的提示
```

> **提示** 在真实世界里，你会进行更严苛的验证，比如对数据去除首尾的空格。一般情况下，我们会使用第三方库（比如 [WTForms](https://github.com/wtforms/wtforms)）来实现表单数据的验证工作。

如果输入的某个数据为空，或是长度不符合要求，就显示错误提示“Invalid input.”，否则显示成功创建的提示“Item Created.”。

### 重定向响应

重定向响应是一类特殊的响应，它会返回一个新的 URL，浏览器在接受到这样的响应后会向这个新 URL 再次发起一个新的请求。Flask 提供了 `redirect()` 函数来快捷生成这种响应，传入重定向的目标 URL 作为参数，比如 `redirect('http://helloflask.com')`。

根据验证情况，我们发送不同的提示消息，最后都把页面重定向到主页，这里的主页 URL 均使用 `url_for()` 函数生成：

```python
if not title or not year or len(year) != 4 or len(title) > 60:
    flash('Invalid title or year!')  
    return redirect(url_for('index'))  # 重定向回主页
flash('Item created.')
return redirect(url_for('index'))  # 重定向回主页
```

## 编辑条目

编辑的实现和创建类似，我们先创建一个用于显示编辑页面和处理编辑表单提交请求的视图函数：

*app.py：编辑电影条目*

```python
@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':  # 处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']
        
        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回对应的编辑页面
        
        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        db.session.commit()  # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('index'))  # 重定向回主页
    
    return render_template('edit.html', movie=movie)  # 传入被编辑的电影记录
```

这个视图函数的 URL 规则有一些特殊，如果你还有印象的话，我们在第 2 章的《实验时间》部分曾介绍过这种 URL 规则，其中的 `<int:movie_id>` 部分表示 URL 变量，而 `int` 则是将变量转换成整型的 URL 变量转换器。在生成这个视图的 URL 时，我们也需要传入对应的变量，比如 `url_for('edit', movie_id=2)` 会生成 /movie/edit/2。

`movie_id` 变量是电影条目记录在数据库中的主键值，这个值用来在视图函数里查询到对应的电影记录。查询的时候，我们使用了 `get_or_404()` 方法，它会返回对应主键的记录，如果没有找到，则返回 404 错误响应。

为什么要在最后把电影记录传入模板？既然我们要编辑某个条目，那么必然要在输入框里提前把对应的数据放进去，以便于进行更新。在模板里，通过表单 `<input>` 元素的 `value` 属性即可将它们提前写到输入框里。完整的编辑页面模板如下所示：

*templates/edit.html：编辑页面模板*

```html
{% extends 'base.html' %}

{% block content %}
<h3>Edit item</h3>
<form method="post">
    Name <input type="text" name="title" autocomplete="off" required value="{{ movie.title }}">
    Year <input type="text" name="year" autocomplete="off" required value="{{ movie.year }}">
    <input class="btn" type="submit" name="submit" value="Update">
</form>
{% endblock %}
```

最后在主页每一个电影条目右侧都添加一个指向该条目编辑页面的链接：

*index.html：编辑电影条目的链接*

```html
<span class="float-right">
    <a class="btn" href="{{ url_for('edit', movie_id=movie.id) }}">Edit</a>
    ...
</span>
```

点击某一个电影条目的编辑按钮打开的编辑页面如下图所示：

![编辑电影条目](images/7-1.png)

## 删除条目

因为不涉及数据的传递，删除条目的实现更加简单。首先创建一个视图函数执行删除操作，如下所示：

*app.py：删除电影条目*

```python
@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index'))  # 重定向回主页
```

为了安全的考虑，我们一般会使用 POST 请求来提交删除请求，也就是使用表单来实现（而不是创建删除链接）：

*index.html：删除电影条目表单*

```html
<span class="float-right">
    ...
    <form class="inline-form" method="post" action="{{ url_for('delete', movie_id=movie.id) }}">
        <input class="btn" type="submit" name="delete" value="Delete" onclick="return confirm('Are you sure?')">
    </form>
    ...
</span>
```

为了让表单中的删除按钮和旁边的编辑链接排成一行，我们为表单元素添加了下面的 CSS 定义：

```css
.inline-form {
    display: inline;
}
```

最终的程序主页如下图所示：

![添加表单和操作按钮后的主页](images/7-2.png)

## 本章小结

本章我们完成了程序的主要功能：添加、编辑和删除电影条目。结束前，让我们提交代码：

```bash
$ git add .
$ git commit -m "Create, edit and delete item by form"
$ git push
```

> **提示** 你可以在 GitHub 上查看本书示例程序的对应 commit：[84e766f](https://github.com/greyli/watchlist/commit/84e766f276a25cb2b37ab43a468b2b707ed3489c)。在后续的 [commit](https://github.com/greyli/watchlist/commit/bb892c5f4721208619e656ccda7827c821fb301a) 里，我们为另外两个常见的 HTTP 错误：400（Bad Request） 和 500（Internal Server Error） 错误编写了错误处理函数和对应的模板，前者会在请求格式不符要求时返回，后者则会在程序内部出现任意错误时返回（关闭调试模式的情况下）。

## 进阶提示

- 从上面的代码可以看出，手动验证表单数据既麻烦又不可靠。对于复杂的程序，我们一般会使用集成了 WTForms 的扩展 [Flask-WTF](https://github.com/lepture/flask-wtf) 来简化表单处理。通过编写表单类，定义表单字段和验证器，它可以自动生成表单对应的 HTML 代码，并在表单提交时验证表单数据，返回对应的错误消息。更重要的，它还内置了 CSRF（跨站请求伪造） 保护功能。你可以阅读 [Flask-WTF 文档](https://flask-wtf.readthedocs.io/en/stable/)和 Hello, Flask! 专栏上的[表单系列文章](https://zhuanlan.zhihu.com/p/23577026)了解具体用法。
- CSRF 是一种常见的攻击手段。以我们的删除表单为例，某恶意网站的页面中内嵌了一段代码，访问时会自动发送一个删除某个电影条目的 POST 请求到我们的程序。如果我们访问了这个恶意网站，就会导致电影条目被删除，因为我们的程序没法分辨请求发自哪里。解决方法通常是在表单里添加一个包含随机字符串的隐藏字段，同时在 Cookie 中也创建一个同样的随机字符串，在提交时通过对比两个值是否一致来判断是否是用户自己发送的请求。在我们的程序中没有实现 CSRF 保护。
- 使用 Flask-WTF 时，表单类在模板中的渲染代码基本相同，你可以编写宏来渲染表单字段。如果你使用 Bootstap，那么扩展 [Bootstrap-Flask](https://github.com/greyli/bootstrap-flask) 内置了多个表单相关的宏，可以简化渲染工作。
- 你可以把删除按钮的行内 JavaScript  代码改为事件监听函数，写到单独的 JavaScript 文件里。再进一步，你也可以使用 JavaScript 来监听点击删除按钮的动作，并发送删除条目的 POST 请求，这样删除按钮就可以使用普通 `<a>` 标签（CSRF 令牌存储在元素属性里），而不用创建表单元素。
- 如果你是[《Flask Web 开发实战》](http://helloflask.com/book/)的读者，第 4 章介绍了表单处理的各个方面，包括表单类的编写和渲染、错误消息显示、自定义错误消息语言、文件和多文件上传、富文本编辑器等等。