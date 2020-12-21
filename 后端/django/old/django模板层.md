# Django模板语言详解

本节将介绍Django模版系统的语法。Django模版语言致力于在性能和简单性上取得平衡。

如果你有过其它编程背景，或者使用过一些在HTML中直接混入程序代码的语言，那么你需要记住，Django的模版系统并不是简单的将Python嵌入到HTML中。

## 一、模板

模版是纯文本文件，可以生成任何基于文本的文件格式，比如HTML，XML，CSV等。

下面是一个小模版，它展示了一些基本的元素。 

```html
{% extends "base_generic.html" %}

{% block title %}{{ section.title }}{% endblock %}

{% block content %}
<h1>{{ section.title }}</h1>

{% for story in story_list %}
<h2>
  <a href="{{ story.get_absolute_url }}">
    {{ story.headline|upper }}
  </a>
</h2>
<p>{{ story.tease|truncatewords:"100" }}</p>
{% endfor %}
{% endblock %}
```

## 二、变量

变量看起来就像是这样： `{{ variable }}。` 

当模版系统渲染变量的时候遇到点(".")，它将以这样的顺序查询这个圆点具体代表的功能：

- 字典查询（Dictionary lookup）
- 属性或方法查询（Attribute or method lookup）
- 数字索引查询（Numeric index lookup）

如果你使用的变量不存在，模版系统将插入`string_if_invalid`选项的值，默认设置为''(空字符串)。

注意，像`{{ foo.bar }}`这种模版表达式中的“bar”，如果在模版上下文中存在，将解释为一个字面意义的字符串而不是使用变量bar的值 。

## 三、过滤器

过滤器看起来是这样的：`{{ name | lower }}`。使用管道符号(`|`)来应用过滤器。该过滤器将文本转换成小写。

过滤器特性：

- 链接：`{{ text|escape|linebreaks }}`就是一个常用的过滤器链，它首先转移文本内容，然后把文本行转成`<p>`标签。
- 参数： `{{ bio|truncatewords:30 }}`。 这将显示bio变量的前30个词。**过滤器参数包含空格的话，必须用引号包起来。**例如，使用逗号和空格去连接一个列表中的元素，你需要使用`{{ list|join:", " }}`。

Django提供了大约六十个内置的模版过滤器，很多时候你想要的功能，它都已经提供了，经常查看这些过滤器，发现新大陆吧。下面是一些常用的模版过滤器：

| 常用模板过滤器 | 说明                                                         | 例子                           |
| -------------- | ------------------------------------------------------------ | ------------------------------ |
| default        | 为false或者空变量提供默认值                                  | `{{ value|defatul:"nothing"}}` |
| length         | 返回字符串或列表等的长度                                     | `{{ value|length}}`            |
| filesizeformat | 格式化为“人类可读”文件大小单位<br />（即'13 KB'，4.1 MB'，'102 bytes'等）。 | `{{ value|filesizeoformat }}`  |



## 四、标签

标签看起来像是这样的： `{% tag %}`。 

标签比变量复杂得多，有些用于在输出中创建文本，有些用于控制循环或判断逻辑，有些用于加载外部信息到模板中供以后的变量使用。

一些标签需要开始和结束标签（即 `{％ 标签 ％} ... 标签 内容 ... {％ ENDTAG ％}`）。

Django自带了大约24个内置的模版标签。下面是一些常用的标签：

### 1. for循环标签

循环对象中每个元素。需要结束标签`{% endfor %}` 。例如，显示`athlete_list`中提供的运动员列表：

```html
<ul>
{% for athlete in athlete_list %}
    <li>{{ athlete.name }}</li>
{% endfor %}
</ul>
```

### 2. if，elif和else标签

计算一个表达式，并且当表达式的值是“True”时，显示块中的内容。需要`{% endif %}`结束标签。整体逻辑非常类似Python的if、elif和else，如下所示。：

```jinja2
{% if athlete_list %}
    Number of athletes: {{ athlete_list|length }}
{% elif athlete_in_locker_room_list %}
    Athletes should be out of the locker room soon!
{% else %}
    No athletes.
{% endif %}
```

在上面的例子中，如果`athlete_list`不是空的，运动员的数量将显示为`{{ athlete_list|length }}`。否则，如果`athlete_in_locker_room_list`不为空，将显示“Athletes should be out…”。如果两个列表都是空的，将显示“No athletes.” 。

还可以在if标签中使用过滤器和多种运算符：

```jinja2
{% if athlete_list|length > 1 %}
   Team: {% for athlete in athlete_list %} ... {% endfor %}
{% else %}
   Athlete: {{ athlete_list.0.name }}
{% endif %}
```

需要注意，大多数模版过滤器都返回字符串类型，所以使用过滤器做整数类型的比较通常是错误的，但length是一个例外。

### 3. block和extends标签

继承和复写模版。类似Python的类继承和重写机制。

## 五、注释

要注释模版中一行的部分内容，使用注释语法:`{# #}`。

例如，下面的模版将被渲染为'hello'：

```jinja2
{# greeting #}hello
```

注释可以包含任何模版内的代码，有效的或者无效的都可以。 像这样：

```jinja2
{# {% if foo %}bar{% else %} #}
```

以上是单行注释（在`{# .... #}`中，不允许有新行）。 

如果需要注释掉模版中的多行内容，请使用comment标签。

## 六、模板继承

Django模版引擎中最强大也是最复杂的部分就是模版继承了。模版继承允许你创建一个包含基本“骨架”的父亲模版，它包含站点中的共有元素，并且可以定义能够被子模版覆盖的blocks。

通过下面这个例子，理解模版继承的概念：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="style.css" />
    <title>{% block title %}My amazing site{% endblock %}</title>
</head>

<body>
    <div id="sidebar">
        {% block sidebar %}
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/blog/">Blog</a></li>
        </ul>
        {% endblock %}
    </div>

    <div id="content">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

这个模版，通常被命名为`base.html`，它定义了一个可以用于两列排版页面的简单HTML骨架。 

“子模版”需要做的是先继承父模板`base.html`，然后复写、填充，或者说实现其中的blocks。

block是在子模版中可能会被覆盖掉的位置。在上面的例子中，block标签定义了三个可以被子模版内容填充的block，分别是title、content和siderbar。

再看下面的例子，子模版可能看起来是这样的：

```jinja2
{% extends "base.html" %}

{% block title %}My amazing blog{% endblock %}

{% block content %}
{% for entry in blog_entries %}
    <h2>{{ entry.title }}</h2>
    <p>{{ entry.body }}</p>
{% endfor %}
{% endblock %}
```

extends标签是这里的关键。它告诉模版引擎，这个模版“继承”了另一个模版。当模版系统处理这个模版时，首先会去加载父模版，也就是“base.html”。

加载过程中，模版引擎将注意到`base.html`中的三个block标签，并用子模版中的内容来替换这些block。 根据`blog_entries`的值，最终输出可能看起来是这样的：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="style.css" />
    <title>My amazing blog</title>
</head>

<body>
    <div id="sidebar">
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/blog/">Blog</a></li>
        </ul>
    </div>

    <div id="content">
        <h2>Entry one</h2>
        <p>This is my first entry.</p>

        <h2>Entry two</h2>
        <p>This is my second entry.</p>
    </div>
</body>
</html>
```

请注意，上面例子中的子模版并没有定义`sidebar block`，这种情况下，将使用父模版中的内容。父模版的`{% block %}`标签中的内容总是被用作默认内容。

Django还支持多级继承！常用方式是类似下面的三级结构：

- 创建一个`base.html`模版，用来控制整个站点的主要视觉和体验。
- 为站点的每一个app，创建一个`base_SECTIONNAME.html`模版。 例如`base_news.html`,`base_sports.html`。这些模版都继承`base.html`，并且包含了各自特有的样式和设计。
- 为每一个页面类型，创建独立的模版，例如新闻内容或者博客文章。 这些模版继承对应app的模版。

上面的方式可以使代码得到最大程度的复用，并且使得添加内容到共享的内容区域更加简单，例如app范围内的导航条。

下面是使用继承的一些相关说明：

- 如果在模版中使用`{% extends %}`标签，它必须是模版中的第一个标签，必须放在文件首行！ 
- 在base模版中设置越多的`{% block %}`标签越好。子模版不必定义全部父模版中的blocks，所以可以在大多数blocks中填充合理的默认内容，然后，只定义你需要的那一个。多一点钩子总比少一点好。
- 如果发现你自己在复制大量重复的模版内容，那意味着你应该把重复的内容移动到父模版中的一个`{% block %}`中。
- 如果需要获取父模板中的block的内容，可以使用`{{ block.super }}`变量。如果想要在父block中新增内容而不是完全覆盖它，这将非常有用。使用`{{ block.super }}` 插入的数据不会被自动转义，因为父模板中的内容已经被转义。
- 在`{% block %}`之外创建的变量使用模板标签的`as`语法，不能在块内使用。 

例如，下面的模板不会显示任何内容：

```
{% trans "Title" as title %}
{% block content %}{{ title }}{% endblock %}
```

- 为了更好的可读性，可以给`{% endblock %}`标签一个取名字，像这样：

  {% block content %} ...

在大型模版中，这有助于你清楚的看到哪一个`{% block %}`标签被关闭了。

- 最后，请注意不能在一个模版中定义多个相同名字的block标签。 

## 七、自动转义HTML

当从模版中生成HTML文件时，总会存在各种风险，比如xss代码注入等恶意攻击。比如下面的模版片段：

```
Hello, {{ name }}
```

首先，它看起来像是无害的，用来显示用户的名字，但是设想一下，如果用户像下面这样输入他的名字，会发生什么：

```
<script>alert('hello')</script>
```

使用这个名字的值，模版将会被渲染成这样：

```
Hello, <script>alert('hello')</script>
```

这意味着浏览器会弹出一个JavaScript警报框！

类似的，如果名字包含一个 '<' 符号（比如下面这样），会发生什么呢？

```
<b>username
```

这将会导致模版被渲染成这样：

```
Hello, <b>username
```

这会导致网页的其余部分被粗体化！

显然，**用户提交的数据都被不应该被盲目的信任**，并且被直接插入到网页中，因为一个怀有恶意的用户可能会使用这样的漏洞来做一些坏事。 这种类型的安全问题被叫做跨站脚本攻击(Cross Site Scripting）(XSS)。

为避免这个问题，有两个选择：

- 第一，对每个不被信任的值运行escape过滤器，这将把潜在的有害的HTML字符转换成无害的字符串。在Django最初的几年里，这是默认的解决方案，但问题是它将责任放在开发人员/模板作者身上，以确保转义了所有内容，而且很容易忘记转义数据。
- 第二，利用Django的自动HTML转义功能。默认情况下，Django中的每个模板会自动转义每个变量。也就是说，下面五个字符将被转义：
- `<`会转换为`<`
- `>`会转换为`>`
- `'`（单引号）转换为`'`
- `"`(双引号)会转换为`"`
- `&`会转换为`&`

**强烈建议：将第二种功能做为默认打开的设置，不要关闭它！**

但是，凡事都有正反两面。有时，模板变量含有一些你打算渲染成原始HTML的数据，你并不想转义这些内容。  例如，你可能会在数据库中储存一些HTML代码，并且直接在模板中嵌入它们。或者，你可能使用Django的模板系统来生成不是HTML的文本 --  比如邮件信息。要怎么办呢？

**对于单个变量**：

使用safe过滤器来关闭变量上的自动转义：

```
This will be escaped: {{ data }}
This will not be escaped: {{ data|safe }}
```

safe是`safe from further escaping`或者`can be safely interpreted as HTML`的缩写。请确保你知道自己在用safe过滤器干什么！在上面的例子中，如果data含有`<b>`，输出会是：

```
This will be escaped: &lt;b&gt;
This will not be escaped: <b>
```

**对于模板块:**

要控制模板上的自动转义，将模板（或者模板中的特定区域）包裹在`autoescape`标签中，像这样：

```
{% autoescape off %}
    Hello {{ name }}
{% endautoescape %}
```

autoescape标签接受on或者off作为它的参数。下面是一个模板的示例：

```
Auto-escaping is on by default. Hello {{ name }}

{% autoescape off %}
    This will not be auto-escaped: {{ data }}.

    Nor this: {{ other_data }}
    {% autoescape on %}
        Auto-escaping applies again: {{ name }}
    {% endautoescape %}
{% endautoescape %}
```

自动转义标签autoescape还会作用于扩展（extend）了当前模板的模板，以及通过include标签包含的模板，就像所有block标签那样。 看下面的例子：

```
# base.html文件

{% autoescape off %}
<h1>{% block title %}{% endblock %}</h1>
{% block content %}
{% endblock %}
{% endautoescape %}

# child.html文件

{% extends "base.html" %}
{% block title %}This &amp; that{% endblock %}
{% block content %}{{ greeting }}{% endblock %}
```

由于自动转义标签在base模板中关闭，它也会在child模板中关闭，导致当greeting变量含有`<b>Hello!</b>`字符串时，会渲染HTML。

```
<h1>This &amp; that</h1>
<b>Hello!</b>
```

**过滤器的字符串参数：**

之前我们展示过，过滤器的参数可以是字符串：

```
{{ data|default:"This is a string literal." }}
```

要注意，所有这种字符串参数在插入模板时都不会进行任何自动转义。原因是，模板的作者可以控制字符串字面值的内容，所以可以确保在模板编写时文本经过正确转义。白话讲，就是，你个程序员对自己传递的参数心里要有数！

也即是说你应该这样编写：

```
{{ data|default:"3 &lt; 2" }}
```

而不是：

```
{{ data|default:"3 < 2" }}  {# 错误的做法#}
```

## 八、方法调用

这部分内容，如果你掌握的极大提高你的模版语言能力。

大多数对象上的方法调用同样可用于模板中。这意味着模板能够访问到的不仅仅是对象的属性（比如字段名称）和视图中传入的变量，还可以执行对象的方法。 例如，Django ORM提供了“entry_set”语法用于查找关联到外键的对象集合。  所以，如果模型“comment”有一个外键关联到模型“task”，可以根据task遍历其所有的comments，像这样：

```
{% for comment in task.comment_set.all %}
    {{ comment }}
{% endfor %}
```

与之类似，QuerySets提供了count()方法来计算含有对象的总数。因此，你可以像这样获取所有关于当前任务的评论总数：

```
{{ task.comment_set.all.count }}
```

当然，还可以访问已经显式定义在模型上的方法：

```
# models.py
class Task(models.Model):
    def foo(self):
        return "bar"
template.html
{{ task.foo }}
```

由于Django有意限制了模板语言中的处理逻辑，不能够在模板中传递参数来调用方法。数据应该在视图中处理，然后传递给模板用于展示。这点不同于Django的ORM操作。

## 九、多对多调用

对于如下的模型：

```
from django.db import models

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=128)

class Course(models.Model):
    name = models.CharField(max_length=128)
    students = models.ManyToManyField('Student')
```

模型Course有一个多对多字段指向Student模型。

### 正向查询

假设编写了一个如下的视图：

```
def test(request):
    course = models.Course.objects.get(pk=1)
    return render(request, 'course.html', locals())
```

获取了id为1的course对象，并将它传递给course.html模版，模版代码如下：

```
{% for student in course.students.all %}

<p>{{ student.name }}</p>

{% endfor %}
```

首先通过`course.students.all`，查寻到course对象关联的students对象集，然后用for标签循环它，获取每个student对象，再用student模型的定义，访问其各个字段的属性。

### 反向查询

对于反向查询，从student往course查，假设有如下的视图：

```
def test2(request):
    student = models.Student.objects.get(pk=1)
    return render(request, 'student.html', locals())
```

获取了id为1的student对象，并将它传递给student.html模版，模版代码如下：

```
{% for course in  student.course_set.all %}
{{ course.name }}
{% endfor %}
```

通过`student.course_set.all`，反向获取到student实例对应的所有course对象，然后再for标签循环每个course，调用course的各种字段属性。

对于外键ForeignKey，其用法基本类似。只不过正向是`obj.fk`，且只有1个对像，不是集合。反向则是`obj.fk_set`，类似多对多。

## 十、使用自定义标签和过滤器

某些应用提供了自定义的标签和过滤器。想要在模板中使用它们，首先要确保该应用已经在`INSTALLED_APPS` 中（比如在下面的例子中，我们添加了'django.contrib.humanize'），之后在模板中使用load标签：

```
{% load humanize %}
{{ 45000|intcomma }}
```

上面的例子中， load标签加载了`humanize`app的标签库，之后我们可以使用它的intcomma过滤器。 

如果你开启了`django.contrib.admindocs`，可以查询admin站点中的文档，查看你安装的自定义库列表。

load标签可以同时接受多个库名称，由空格分隔。 例如：

```
{% load humanize i18n %}
```

**自定义库和模板继承：**

当你加载一个自定义标签或过滤器库时，标签或过滤器只在当前模板中有效--并不是带有模板继承关系的任何父模板或者子模版中都有效。白话说就是，你在父模板中可能加载了自定义标签，然并卵，你在子模版中还要再加载一次！

例如，如果一个模板`foo.html`带有`{% load humanize %}`，子模版（例如，带有`{% extends "foo.html" %}`）中不能访问humanize模板标签和过滤器。 子模版需要再添加自己的`{% load humanize %}`。

这个特性是出于保持可维护性和逻辑性的目的。

# Django内置模板标签

阅读: 33730                  [评论](https://www.liujiangblog.com/course/django/146#comments)：14            

------

## Django内置标签总览

可以查询下表来总览Django的内置标签：

| 标签        | 说明                      |
| ----------- | ------------------------- |
| autoescape  | 自动转义开关              |
| block       | 块引用                    |
| comment     | 注释                      |
| csrf_token  | CSRF令牌                  |
| cycle       | 循环对象的值              |
| debug       | 调试模式                  |
| extends     | 继承模版                  |
| filter      | 过滤功能                  |
| firstof     | 输出第一个不为False的参数 |
| for         | 循环对象                  |
| for … empty | 带empty说明的循环         |
| if          | 条件判断                  |
| ifchanged   | 如果有变化，则..          |
| include     | 导入子模版的内容          |
| load        | 加载标签和过滤器          |
| lorem       | 生成无用的废话            |
| now         | 当前时间                  |
| regroup     | 根据对象重组集合          |
| resetcycle  | 重置循环                  |
| spaceless   | 去除空白                  |
| templatetag | 转义模版标签符号          |
| url         | 获取url字符串             |
| verbatim    | 禁用模版引擎              |
| widthratio  | 宽度比例                  |
| with        | 上下文变量管理器          |

# Django内置过滤器

阅读: 27764                  [评论](https://www.liujiangblog.com/course/django/147#comments)：3            

------

## Django内置过滤器总览

可以查询下表来总览Django的内置过滤器：

| 过滤器             | 说明                                                  |
| ------------------ | ----------------------------------------------------- |
| add                | 加法                                                  |
| addslashes         | 添加斜杠                                              |
| capfirst           | 首字母大写                                            |
| center             | 文本居中                                              |
| cut                | 切除字符                                              |
| date               | 日期格式化                                            |
| default            | 设置默认值                                            |
| default_if_none    | 为None设置默认值                                      |
| dictsort           | 字典排序                                              |
| dictsortreversed   | 字典反向排序                                          |
| divisibleby        | 整除判断                                              |
| escape             | 转义                                                  |
| escapejs           | 转义js代码                                            |
| filesizeformat     | 文件尺寸人性化显示                                    |
| first              | 第一个元素                                            |
| floatformat        | 浮点数格式化                                          |
| force_escape       | 强制立刻转义                                          |
| get_digit          | 获取数字                                              |
| iriencode          | 转换IRI                                               |
| join               | 字符列表链接                                          |
| json_script        | 生成script标签，带json数据                            |
| last               | 最后一个                                              |
| length             | 长度                                                  |
| length_is          | 长度等于                                              |
| linebreaks         | 行转换                                                |
| linebreaksbr       | 行转换                                                |
| linenumbers        | 行号                                                  |
| ljust              | 左对齐                                                |
| lower              | 小写                                                  |
| make_list          | 分割成字符列表                                        |
| phone2numeric      | 电话号码                                              |
| pluralize          | 复数形式                                              |
| pprint             | 调试                                                  |
| random             | 随机获取                                              |
| rjust              | 右对齐                                                |
| safe               | 安全确认                                              |
| safeseq            | 列表安全确认                                          |
| slice              | 切片                                                  |
| slugify            | 转换成ASCII                                           |
| stringformat       | 字符串格式化                                          |
| striptags          | 去除HTML中的标签                                      |
| time               | 时间格式化                                            |
| timesince          | 从何时开始                                            |
| timeuntil          | 到何时多久                                            |
| title              | 所有单词首字母大写                                    |
| truncatechars      | 截断字符                                              |
| truncatechars_html | 截断字符                                              |
| truncatewords      | 截断单词                                              |
| truncatewords_html | 截断单词                                              |
| unordered_list     | 无序列表                                              |
| upper              | 大写                                                  |
| urlencode          | 转义url                                               |
| urlize             | url转成可点击的链接                                   |
| urlizetrunc        | urlize的截断方式                                      |
| wordcount          | 单词计数                                              |
| wordwrap           | 单词包裹                                              |
| yesno              | 将True，False和None，映射成字符串‘yes’，‘no’，‘maybe’ |

**为模版过滤器提供参数的方式是：过滤器后加个冒号，再紧跟参数，中间不能有空格！**

**目前只能为过滤器最多提供一个参数！**