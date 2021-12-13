Django的视图层包含下面一些主要内容：

- URL路由
- 视图函数
- 快捷方式
- 装饰器
- 请求与响应
- 类视图
- 文件上传
- CSV/PDF生成
- 内置中间件

# URL路由基础

Django奉行DRY（Don't Repeat Yourself ）主义，提倡使用简洁、优雅的URL

## 一、概述

Django提倡项目有个根`urls.py`，各app下分别有自己的一个`urls.py`，既集中又分治，是一种解耦的模式。

随便新建一个Django项目，默认会自动为我们创建一个`/<project_name>/urls.py`文件，并且自动包含下面的内容，这就是项目的根URL：

```python
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
```

默认导入了path方法和admin模块，然后有一条指向admin后台的url路径。

## 二、Django如何处理请求

当用户请求一个页面时，Django根据下面的逻辑执行操作：

1. **决定要使用的根URLconf模块。**通常，这是`ROOT_URLCONF`(在settings.py里查看)设置的值

   ```python
   ROOT_URLCONF = 'django_study.urls'
   ```

   

2. **加载该模块(`urls.py`)并寻找可用的urlpatterns。** 它是`django.urls.path()`或者`django.urls.re_path()`实例的一个列表。

   ```python
   from django.contrib import admin
   from django.urls import path
   
   urlpatterns = [
       path('admin/', admin.site.urls),
   ]
   ```

   

3. **依次匹配每个URL模式，在与请求的URL相匹配的第一个模式停下来**。也就是说，url匹配是从上往下的短路操作，所以url在列表中的位置非常关键。

4. 导入并调用匹配行中给定的视图，该视图是一个简单的Python函数（被称为视图函数）,或基于类的视图。 视图将获得如下参数:

   - 一个HttpRequest 实例。

   - 如果匹配的表达式返回了未命名的组，那么匹配的内容将作为位置参数提供给视图。

   - 关键字参数由表达式匹配的命名组组成，但是可以被`django.urls.path()`的可选参数kwargs覆盖。

   - 如果没有匹配到任何表达式，或者过程中抛出异常，将调用一个适当的错误处理视图。（比如403，比如无任何反应） 

## 三、简单示例

先看一个例子：

```python
from django.urls import path

from . import views

urlpatterns = [
    path('articles/2003/', views.special_case_2003),
    path('articles/<int:year>/', views.year_archive),
    path('articles/<int:year>/<int:month>/', views.month_archive),
    path('articles/<int:year>/<int:month>/<slug:slug>/', views.article_detail),
]
```

注意：

1. urlpatterns是个列表，每个元素都是`path()` 或 `re_path()` 的实例
2. 要**捕获一段url中的值**，需要使用尖括号，而不是之前的圆括号；
3. 可以转换捕获到的值为指定类型，比如例子中的int。默认情况下，捕获到的结果保存为字符串类型，不包含`/`这个特殊字符；
4. 匹配模式的最开头不需要添加`/`，因为默认情况下，每个url都带一个最前面的`/`，既然大家都有的部分，就不用浪费时间特别写一个了。
5. 每个匹配模式**都建议以斜杠结尾**

匹配例子：

- /articles/2005/03/ 将匹配第三条，并调用`views.month_archive(request, year=2005, month=3)`；
- /articles/2003/匹配第一条，并调用`views.special_case_2003(request)`；
- /articles/2003将一条都匹配不上，因为它最后少了一个斜杠，而列表中的所有模式中都以斜杠结尾；
- /articles/2003/03/building-a-django-site/ 将匹配最后一个，并调用`views.article_detail(request, year=2003, month=3, slug="building-a-django-site"`

**请思考：**

第一问：/articles/2005/March/会匹配那一条？第三条？它那一条都不匹配！因为月份有个int转换器，March无法被转换为整数，所以无法匹配。

第二问：那么如果我去掉第三条的int转换器呢，让它变成`path('articles/<year>/<month>/', views.month_archive),`呢？/articles/2005/March/会成功匹配！

第三问：如果只保留第三条path，其它的都删除，那么/articles/2003/会匹配上吗？不会！因为默认的匹配方式是exact完全相同，而不是include子串包含。

第四问：如果我将第一条和第二条换个位置，那么/articles/2003/会匹配哪个？它会匹配`'articles/<int:year>/'`，因为短路机制。

第五问：我能不能写一个`path('articles/year<int:year>/month<int:month>/', views.another_month_archive),`这样的path？当然可以！但是这么不优雅！

第六问：path最后的斜杠和我们在浏览器中最后是否输入斜杠之间是什么关系？记住，path最后有斜杠，则url输入最后可以有也可以没有斜杠，但是path最后没有斜杠，则url输入最后也不能有斜杠。

提示：每当urls.py文件被第一次加载的时候，urlpatterns里的表达式们都将被预先编译，这会大大提高系统处理路由的速度。

## 四、path转换器

默认情况下，Django内置下面的路径转换器：

- `str`：匹配任何非空字符串，但不含斜杠`/`，如果你没有专门指定转换器，默认使用该转换器
- `int`：匹配0和正整数，返回一个int类型
- `slug`：可理解为注释、后缀、附属等概念，是url拖在最后的一部分解释性字符。该转换器匹配任何ASCII字符以及连接符和下划线，比如`building-your-1st-django-site`；
- `uuid`：匹配一个uuid格式的对象。为了防止冲突，规定必须使用破折号，所有字母必须小写，例如`075194d3-6885-417e-a8a8-6c931e272f00`。返回一个UUID对象；
- `path`：匹配任何非空字符串，重点是可以包含路径分隔符’/‘。这个转换器可以帮助你匹配整个url而不是一段一段的url字符串。**要区分path转换器和path()方法**。

## 五、自定义path转换器

对于更复杂的匹配需求，你可能需要自定义你自己的path转换器。

path转换器其实就是一个类，包含下面的成员和属性：

- 类属性`regex`：一个字符串形式的正则表达式属性；
- `to_python(self, value)` 方法：一个用来将匹配到的字符串转换为你想要的那个数据类型，并传递给视图函数。如果转换失败，它必须弹出ValueError异常；
- `to_url(self, value)`方法：将Python数据类型转换为一段url的方法，上面方法的反向操作。如果转换失败，也会弹出`ValueError`异常。

例如，新建一个converters.py文件，与urlconf同目录，写个下面的类：

```python
class FourDigitYearConverter:
    regex = '[0-9]{4}'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%04d' % value
```

写完类后，在URLconf 中使用`register_converter`注册它，如下所示，注册了一个yyyy：

```python
from django.urls import register_converter, path

from . import converters, views

register_converter(converters.FourDigitYearConverter, 'yyyy')

urlpatterns = [
    path('articles/2003/', views.special_case_2003),
    path('articles/<yyyy:year>/', views.year_archive),
    ...
]
```

## 六、使用正则表达式

Django2.0的urlconf虽然改‘配置方式’了，但它依然向老版本兼容。而这个兼容的办法，就是用`re_path()`方法。`re_path()`方法在骨子里，根本就是以前的`url()`方法，只不过导入的位置变了。下面是一个例子，对比一下Django1.11时代的语法，有什么太大的差别？

```
from django.urls import path, re_path

from . import views

urlpatterns = [
    path('articles/2003/', views.special_case_2003),
    re_path(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive),
    re_path(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive),
    re_path(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<slug>[\w-]+)/$', views.article_detail),
]
```

与`path()`方法不同的在于三点：

- 捕获URL中的参数使用的是正则捕获，语法是 `(?P<name>pattern)` ，其中 `name` 是组名，`pattern` 是要匹配的模式。
- year中匹配不到10000等非四位数字，这是正则表达式决定的
- **传递给视图的所有参数都是字符串类型**。而不像`path()`方法中可以指定转换成某种类型。在视图中接收参数时一定要小心。

## 七、匹配部分

请求的URL被看做是一个普通的Python字符串，URLconf在其上查找并匹配。**进行匹配时将不包括GET或POST请求方式的参数以及域名。**

例如，在`https://www.example.com/myapp/`的请求中，URLconf将查找`myapp/`。

在`https://www.example.com/myapp/?page=3`的请求中，URLconf也将查找`myapp/`。

**URLconf不检查使用何种HTTP请求方法**，所有请求方法POST、GET、HEAD等都将路由到同一个URL的同一个视图。在视图中，才根据具体请求方法的不同，进行不同的处理。

## 八、指定视图参数的默认值

有一个小技巧，我们可以指定视图参数的默认值。 下面是一个URLconf和视图的示例：

```python
# URLconf
from django.urls import path

from . import views

urlpatterns = [
    path('blog/', views.page),
    path('blog/page<int:num>/', views.page),
]

# 视图 (blog/views.py)
def page(request, num=1):
    # Output the appropriate page of blog entries, according to num.
    ...
```

在上面的例子中，两个URL模式指向同一个视图`views.page`。但是第一个模式不会从URL中捕获任何值。 如果第一个模式匹配，page()函数将使用num参数的默认值"1"。 如果第二个模式匹配，page()将使用捕获的num值。

# [路由转发](https://www.liujiangblog.com/course/django/135)

## 一、路由转发

通常，我们会在每个app里，各自创建一个urls.py路由模块，然后从根路由出发，将app所属的url请求，全部转发到相应的urls.py模块中。

例如，下面是Django网站本身的URLconf节选。 它包含许多其它URLconf：

```python
from django.urls import include, path   

urlpatterns = [
    # ... 省略...
    path('community/', include('aggregator.urls')),
    path('contact/', include('contact.urls')),
    # ... 省略 ...
]
```



## 二、捕获参数

目的地URLconf会收到来自父URLconf捕获的所有参数，看下面的例子：

```python
# In settings/urls/main.py
from django.urls import include, path

urlpatterns = [
    path('<username>/blog/', include('foo.urls.blog')),
]

# In foo/urls/blog.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog.index),
    path('archive/', views.blog.archive),
]
```

在上面的例子中，捕获的"username"变量将被传递给include()指向的URLconf，再进一步传递给对应的视图。

## 三、向视图传递额外的参数

URLconfs具有一个钩子（hook），允许你传递一个Python字典作为额外的关键字参数给视图函数，像下面这样：

```python
from django.urls import path
from . import views

urlpatterns = [
    path('blog/<int:year>/', views.year_archive, {'foo': 'bar'}),
]
```

在上面的例子中，对于`/blog/2005/`请求，Django将调`用views.year_archive(request, year='2005', foo='bar')`。理论上，你可以在这个字典里传递任何你想要的传递的东西。但是要注意，URL模式捕获的命名关键字参数和在字典中传递的额外参数有可能具有相同的名称，这会发生冲突，将使用字典里的参数来替代捕捉的参数。

## 四、传递额外的参数给include()

类似上面，也可以传递额外的参数给include()。参数会传递给include指向的urlconf中的每一行。

```python
# main.py
from django.urls import include, path

urlpatterns = [
    path('blog/', include('inner'), {'blog_id': 3}),
]

# inner.py
from django.urls import path
from mysite import views

urlpatterns = [
    path('archive/', views.archive),
    path('about/', views.about),
]
```

# [反向解析和命名空间](https://www.liujiangblog.com/course/django/136)

## 一、反向解析URL

假设我这里建了个名叫study的app

在`study/urls.py`文件中：

```python
from django.urls import path
from . import views
app_name = 'study'

urlpatterns = [
    path('', views.index, name='index'),
    path('articles/<int:year>/', views.year_archive, name='news-year-archive'),
]
```



在`study/views.py`文件中：

```python
from django.shortcuts import render


def index(request):
    context = {'many_year': [2017, 2018, 2019, 2020]}
    return render(request, 'study/index.html', context)


def year_archive(request, year):
    context = {'year': year}
    return render(request, 'study/archive.html', context)
```

在study目录下的`templates/study/index.html`

```html
<h1>hello</h1>
<ul>
    {% for year in many_year %}
        <li><a href="{% url 'study:news-year-archive' year %}">{{ year }} Archive</a></li>
    {% endfor %}
</ul>
```

`templates/study/archive.html`

```html
<h1>{{ year }}</h1>
<a href="{% url 'study:news-year-archive' year %}">next year</a>
```

这样，在想更改url时，就只用修改urls.py里path的第一个参数，其他文件都不用碰。比如只用这么改一下就ok了。

```python
urlpatterns = [
    path('', views.index, name='index'),
    # path('articles/<int:year>/', views.year_archive, name='news-year-archive'),
    path('texts/<int:year>/', views.year_archive, name='news-year-archive'),
]
```



## 二、应用命名空间app_name

由于一个项目有多个app，可能取的name一样，这就要用app_name来区分了

```python
from django.urls import path
from . import views

app_name = 'your_app_name'   # 重点是这行！

urlpatterns = [
    ...
]
```



使用的方式很简单：

```python
# 视图中
reverse('your_app_name:index',args=(...))

# 模板中
{% url 'your_app_name:index' ... %}
```

注意your_app_name和index之间是冒号分隔。

## 三、实例命名空间namespace

首先我们要知道，Django是可以对app进行实例化的。也就是说：

- 一个app在运行的时候，可以同时生成多个实例
- 每个实例运行同样的代码
- 但是不同的实例，可能会有不同的状态

以上不好理解，甚至很多人都不知道这个知识点。

假设我们有个app，实现一个index页面展示功能：

- 假设访问Django服务器的人分两类，author和publisher，作者和出版社
- 他们都需要访问app
- 业务需求：为两类人实现不同的权限或者页面内容
- 尽可能重用代码

为此，我们可以这么实现：

- 根据不同的url来区分两类人，author访问`author/...`，publisher访问`publisher/...`。
- 两个url都指向同一个app的url：`include('app.urls')`
- 在视图中，根据来访人员的不同，if/else判断，实现不同的业务逻辑。
- 这样，我们就相当于共用了urls和views实现了两套app

而这，就是所谓的app的多个实例！

但这种做法有个明显的问题，就是对于每条URL，如何区分两种人员？

使用应用命名？像`reverse('your_app_name:index',args=(...))`这样？

显然是不行的，因为多个应用的实例共享应用空间名，通过`app_name`是区分不了的！

针对这种情况，Django提供了一个`namespace`属性，用于标记不同的应用实例，如下所示：

```python
# 根urls.py
from django.urls import include, path

# 在include里定义namespace，更好的名字应该是 app_author 与 app_publisher
urlpatterns = [
    path('author/', include('app.urls', namespace='author')),
    path('publisher/', include('app.urls', namespace='publisher')),
]
app/urls.py
from django.urls import path

from . import views

app_name = 'app'          # 这行不能少

urlpatterns = [
    path('index/', views.index, name='index'),
    path('detail/', views.detail, name='detail'),
]
app/views.py
from django.shortcuts import render,HttpResponse


def index(request):

    return HttpResponse('当前的命名空间是%s'% request.resolver_match.namespace)

def detail(request):
    if request.resolver_match.namespace == 'author':
        return HttpResponse('这里是作者的页面')
    elif request.resolver_match.namespace == 'publisher':
        return HttpResponse('这里是出版商的页面')
    else:
        return HttpResponse('去liujiangblog.com学习Django吧')
```

启动服务器，分别访问`author/index/`和`publisher/index`，你应该能看到不同的结果。

要注意：

- namespace定义在include中
- **整个项目的所有app中的所有namespace不能重名，也就是全局唯一！**所以我们一般设计成`appname_spacename`。（文中为了简洁，偷了个懒）
- **使用namespace功能的前提是设置`app_name`，如果不设置，会弹出异常**
- 要在视图中获取namespace属性值，通过`request.resolver_match.namespace`

这样，我们实现了URL的正向解析。那么反向解析怎么做呢？

为根`urls.py`添加一条路由：

```python
from app import views

path('goto/', views.goto)
```

为`app/views.py`添加一个视图：

```python
def goto(request):
    return HttpResponseRedirect(reverse('app:index', current_app='author' ))
```

注意`reverse`方法提供的`current_app`参数!

然后我们访问`goto/`，可以看到页面跳转到了author的index。

是直接指定字符串形式的namespace名称，还是使用`request.resolver_match.namespace`，取决于你当前视图是从哪个URL路由过来的，该URL是否携带了namespace属性。

> 在基于类的视图的方法中，我们也可以这样使用：
>
> ```python
> reverse('app:index', current_app=self.request.resolver_match.namespace)
> ```

再拓展一下，实际上我们再reverse的时候完全可以直接指定使用哪个命名空间：

```python
reverse('author:index')

# 或者

reverse('publisher:index')
```

那么在HTML模板中怎么使用呢？

可以这么用：

```python
{% url 'app:index' %}
```

但是要注意，这会有两种情况：

- 视图携带了namespace，那么访问对应的namespace
- 视图未携带namespace，app应用上一次使用的是author还是pushliser中的哪个，就访问哪个

所以为了彻底区分每个实例，你也可以这么用：

```python
{% url 'author:index' %}

或者

{% url 'publisher:index' %}
```

其实，从这里也能看出，Django为什么要求namespace全局唯一。

# 视图函数及快捷方式

阅读: 26026                  [评论](https://www.liujiangblog.com/course/django/137#comments)：7            

------

视图函数，简称视图，本质上是一个简单的Python函数，它接受Web请求并且返回Web响应。

响应的内容可以是HTML网页、重定向、404错误，XML文档或图像等任何东西。但是，无论视图本身是个什么处理逻辑，最好都返回某种响应。

视图函数的代码写在哪里也无所谓，只要它在你的Python目录下面。但是通常我们约定将视图放置在项目或应用程序目录中的名为`views.py`的文件中。

## 一、简单的视图

下面是一个返回当前日期和时间作为HTML文档的视图：

```python
from django.http import HttpResponse
import datetime

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)
```

让我们逐行分析一下上面的代码：

- 首先，从`django.http`模块导入了`HttpResponse`类，以及Python的datetime库。
- 接着，我们定义了`current_datetime`视图函数。
- 每个视图函数都接收一个`HttpRequest`对象作为第一位置参数，一般取名为`request`，你可以取别的名字，但这不符合潜规则，最好不要那么做。
- 视图函数的名称没有强制规则，但尽量不要和Python及Django内置的各种名称重名，并且尽量精确地反映出它的功能，比如这里的`current_datetime`。
- 该视图返回一个`HttpResponse`对象，其中包含生成的HTML页面。 

## 二、返回错误

在Django中返回HTTP错误代码是非常简单的。

HttpResponse的许多子类对应着除了200（代表“OK”）以外的一些常用的HTTP状态码。

为了标示一个错误，可以直接返回那些子类中的一个实例，而不是普通的HttpResponse。像下面这样：

```python
from django.http import HttpResponse, HttpResponseNotFound

def my_view(request):
    # ...
    if foo:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    else:
        return HttpResponse('<h1>Page was found</h1>')
```

Django为404错误提供了一个特化的子类HttpResponseNotFound。由于一些状态码不太常用，所以不是每个状态码都有一个特化的子类。

也可以向HttpResponse的构造器传递HTTP状态码，来创建你想要的任何状态码的返回类。 像下面这样：

```python
from django.http import HttpResponse

def my_view(request):
    # ...

    # Return a "created" (201) response code.
    return HttpResponse(status=201)
```

关键是在返回中提供`status=201`参数。别的什么303之类的错误都可以参照上面的例子。

## 三、Http404异常

> class django.http.Http404

当你返回错误，例如 `HttpResponseNotFound` ，你需要定义错误页面的 HTML 。

```python
return HttpResponseNotFound('<h1>Page not found</h1>')
```

为了方便，Django 内置了 Http404 异常。（没有Http400、Http403等，只有这一个）

如果你在视图的任何地方引发了 Http404 ，Django 会捕捉到它并且返回标准的错误页面，连同 HTTP 错误代码 404 。

```python
from django.http import Http404
from django.shortcuts import render
from polls.models import Poll

def detail(request, poll_id):
    try:
        p = Poll.objects.get(pk=poll_id)
    except Poll.DoesNotExist:
        raise Http404("Poll does not exist")  # 注意是raise，不是return
    return render(request, 'polls/detail.html', {'poll': p})
```

为了在Django返回404时显示自定义的HTML，可以创建一个名为`404.html`的HTML模板，并将其放置在模板树的顶层。

只有当DEBUG设置为False时，此模板才会被自动使用。DEBUG为True表示开发模式，Django会展示详细的错误信息页面，而不是针对性的404页面。

实际上，当你raise了Http404后：

1. Django会首先读取`django.conf.urls.handler404`的值，默认为`django.views.defaults.page_not_found()`视图
2. 执行`page_not_found()`视图
3. 判断是否自定义了404.html，如果有，输出该HTML文件
4. 如果没有，输出默认的404提示信息

上面的流程就给我们留下了两个自定义404页面的钩子：

- 第一个是在urls中重新指定handler404的值，也就是用哪个视图来处理404
- 第二个是在page_not_found视图中，使用自定义的404.html

一个是自定义处理视图，一个是自定义展示的404页面。

自定义的404.html页面应当位于模板引擎可以搜索到的路径。

## 四、自定义各种错误页面

接着上面的内容。

当Django找不到与请求匹配的URL时，或者当抛出一个异常时，将调用一个错误处理视图。Django默认的自带的错误视图包括400、403、404和500，分别表示请求错误、拒绝服务、页面不存在和服务器错误。它们分别位于：

- handler400 —— django.conf.urls.handler400。
- handler403 —— django.conf.urls.handler403。
- handler404 —— django.conf.urls.handler404。
- handler500 —— django.conf.urls.handler500。

它们又分别对应下面的内置视图：

- handler400 ——  django.views.defaults.bad_request() 
- handler403 ——  django.views.defaults.permission_denied() 
- handler404 ——  django.views.defaults.page_not_found()
- handler500 ——  django.views.defaults.server_error()

我们可以在根URLconf中设置它们。在其它app中的二级URLconf中设置这些变量无效。

Django有内置的HTML模版，用于返回错误页面给用户，但是这些403，404页面实在丑陋，通常我们都自定义错误页面。

首先，在根URLconf中额外增加下面的条目，并导入views模块：

```python
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
]

# 增加的条目
handler400 = views.bad_request
handler403 = views.permission_denied
handler404 = views.page_not_found
handler500 = views.error
```

然后在，app/views.py文件中增加四个处理视图：

```python
from django.shortcuts import render
from django.views.decorators.csrf import requires_csrf_token

@requires_csrf_token
def bad_request(request, exception):
    return render(request, '400.html')

@requires_csrf_token
def permission_denied(request, exception):
    return render(request, '403.html')

@requires_csrf_token
def page_not_found(request, exception):
    return render(request, '404.html')

@requires_csrf_token
def error(request):
    return render(request, '500.html')
```

再根据自己的需求，创建对应的400、403、404、500.html四个页面文件，就可以了（要注意好模板文件的引用方式，视图的放置位置等等）。

**只有当DEBUG设置为False时，这些错误视图才会被自动使用。DEBUG为True表示开发模式，Django会展示详细的错误信息页面，而不是针对性的错误页面。**(在`settings.py`文件里设置DEBUG)

## 五、异步视图

Django3.1开始支持异步视图函数。

编写异步视图，只需要用Python的`async def`关键字语法。Django将自动地探测和运行视图在一个异步上下文环境中。

为了让异步视图发挥它的性能优势，你需要启动一个基于ASGI的异步服务器。

下面是一个异步视图的例子：

```python
import datetime
from django.http import HttpResponse

async def current_datetime(request):
    now = datetime.datetime.now()
    html = '<html><body>It is now %s.</body></html>' % now
    return HttpResponse(html)
```

或者如下面的例子：

```python
async def my_view(request):
    await asyncio.sleep(0.5)
    return HttpResponse('Welcome to visit https//www.liujiangblog.com for Django course')
```

简要说明：

- 异步功能同时支持WSGI和ASGI模式
- 在WSGI模式下，使用异步功能会有性能损失
- 可以混用异步/同步视图或中间件，Django会自动处理其中的上下文
- 建议主要使用同步模式，在有需求的场景才使用异步功能。
- Django的ORM系统、缓存层和其它的一些需要进行长时间网络/IO调用的代码依然不支持异步访问，在未来的版本中将逐步支持。
- 异步功能不会影响同步代码的执行速度，也不会对已有项目产生明显的影响。

## 六、内置的快捷方法

Django在`django.shortcuts`模块中，为我们提供了很多快捷方便的类和方法，它们都很重要，使用频率很高。

### render()

> render(request, template_name, context=None, content_type=None, status=None, using=None)

结合一个给定的模板和一个给定的上下文字典，返回一个渲染后的HttpResponse对象。

**必需参数：**

- **request**：视图函数处理的当前请求，封装了请求头的所有数据，其实就是视图参数request。
- **template_name**：要使用的模板的完整名称或者模板名称的列表。如果是一个列表，将使用其中能够查找到的第一个模板。

**可选参数：**

- **context**：添加到模板上下文的一个数据字典。默认是一个空字典。可以将认可需要提供给模板的数据以字典的格式添加进去。这里有个小技巧，使用Python内置的`locals()`方法，可以方便地将函数作用域内的所有变量一次性添加进去。
- **content_type**：用于生成的文档的[MIME类型](https://baike.baidu.com/item/MIME/2900607)。 默认为`DEFAULT_CONTENT_TYPE`设置的值，也就是`'text/html'`。
- **status**：响应的状态代码。 默认为200。
- **using**：用于加载模板使用的模板引擎的NAME。

**范例：**

下面的例子将渲染模板`myapp/index.html`，MIME类型为`application/xhtml+xml`：

```python
from django.shortcuts import render

def my_view(request):
    # View code here...
    return render(request, 'myapp/index.html', {
        'foo': 'bar',
    }, content_type='application/xhtml+xml')
```

这个示例等同于：

```python
from django.http import HttpResponse
from django.template import loader

def my_view(request):
    # View code here...
    t = loader.get_template('myapp/index.html')
    c = {'foo': 'bar'}
    return HttpResponse(t.render(c, request), content_type='application/xhtml+xml')
```

### redirect()

> redirect(to, *args, permanent=False,* *kwargs)

根据传递进来的url参数，返回HttpResponseRedirect。

参数to可以是：

- 一个模型实例：将调用模型的`get_absolute_url()`函数，反向解析出目的url；
- URL的name名称：可能带有参数：reverse()将用于反向解析url；
- 一个绝对的或相对的URL：将原封不动的作为重定向的目标位置。

默认情况下是临时重定向，如果设置`permanent=True`将永久重定向。

**范例：**

1.调用对象的`get_absolute_url()`方法来重定向URL：

```python
from django.shortcuts import redirect

def my_view(request):
    ...
    obj = MyModel.objects.get(...)
    return redirect(obj)
```

2.传递URL的name名称，内部会自动使用reverse()方法反向解析url：

```python
def my_view(request):
    ...
    return redirect('some-view-name', foo='bar')
```

1. 重定向到硬编码的URL：

```python
def my_view(request):
    ...
    return redirect('/some/url/')
```

1. 重定向到一个完整的URL：

```python
def my_view(request):
    ...
    return redirect('https://www.liujiangblog.com/')

#或者
def my_view(request):
    ...
    return redirect('/some/url/')
```

所有上述形式都接受permanent参数，如果设置为True，将返回**永久重定向**(?)：

```python
def my_view(request):
    ...
    obj = MyModel.objects.get(...)
    return redirect(obj, permanent=True)
```

### get_object_or_404()

> get_object_or_404(klass, *args,* *kwargs)

这个方法，非常有用，请一定熟记。

常用于查询某个对象，找到了则进行下一步处理，如果未找到则给用户返回404页面。

在后台，Django其实是调用了模型管理器的get()方法，只会返回一个对象。不同的是，如果get()发生异常，会引发Http404异常，从而返回404页面，而不是模型的DoesNotExist异常。

**必需参数**：

- **klass**：要获取的对象的Model类名或者Queryset等；
- `**kwargs`:查询的参数，格式应该可以被get()接受。

**范例：**

1.从MyModel中使用主键1来获取对象：

```python
from django.shortcuts import get_object_or_404

def my_view(request):
    obj = get_object_or_404(MyModel, pk=1)
```

这个示例等同于：

```python
from django.http import Http404

def my_view(request):
    try:
        obj = MyModel.objects.get(pk=1)
    except MyModel.DoesNotExist:
        raise Http404("No MyModel matches the given query.")
```

2.除了传递Model名称，还可以传递一个QuerySet实例：

```python
queryset = Book.objects.filter(title__startswith='M')
get_object_or_404(queryset, pk=1)
```

上面的示例不够简洁，它等同于：

```python
get_object_or_404(Book, title__startswith='M', pk=1)
```

3.还可以使用Manager。 如果你自定义了管理器，这将很有用：

```python
get_object_or_404(Book.dahl_objects, title='Matilda')
```

4.还可以使用related managers：

```python
author = Author.objects.get(name='Roald Dahl')
get_object_or_404(author.book_set, title='Matilda')
```

与get()一样，如果找到多个对象将引发一个MultipleObjectsReturned异常。

### get_list_or_404()

> get_list_or_404(klass, *args,* *kwargs)

这其实就是`get_object_or_404`多值获取版本。

在后台，返回一个给定模型管理器上filter()的结果，并将结果映射为一个列表，如果结果为空则弹出Http404异常。

**必需参数**：

- **klass**：获取该列表的一个Model、Manager或QuerySet实例。
- `**kwargs`：查询的参数，格式应该可以被filter()接受。

**范例：**

下面的示例从MyModel中获取所有发布出来的对象：

```python
from django.shortcuts import get_list_or_404

def my_view(request):
    my_objects = get_list_or_404(MyModel, published=True)
```

这个示例等同于：

```python
from django.http import Http404

def my_view(request):
    my_objects = list(MyModel.objects.filter(published=True))
    if not my_objects:
        raise Http404("No MyModel matches the given query.")
```

## 七、视图装饰器

Django内置了一些装饰器，用来对视图函数进行一些控制。

### require_http_methods()

此装饰器位于 `django.views.decorators.http`模块，用于限制可以访问该视图的HTTP方法。

如果请求的HTTP方法，不是指定的方法之一，则返回`django.http.HttpResponseNotAllowed`响应。

看例子：

```python
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])             # 注意参数的提供方式
def my_view(request):
    # 我们决定只有GET或者POST请求可以访问这个视图
    # ...
    pass
```

参数必须是大写字符串。

### require_GET()

上面的狭隘版本，只允许GET请求访问。位于 `django.views.decorators.http`模块。

### require_POST()

只允许POST请求访问。位于 `django.views.decorators.http`模块。

### require_safe()

只允许安全的请求类型，也就是GET和HEAD访问。位于 `django.views.decorators.http`模块。

### gzip_page()

对视图的响应内容进行压缩，如果浏览器支持。位于 `django.views.decorators.gzip`模块。

更多的装饰器如下所示，有兴趣的可以自行研究：

- condition(etag_func=None, last_modified_func=None)
- etag(etag_func)
- last_modified(last_modified_func)
- vary_on_cookie(func)
- vary_on_headers(*headers)
- cache_control()
- never_cache(view_func)

## 八、serve()视图

Django开发过程中，出了Python代码、前端静态文件，还有一类媒体文件，比如用户上传的图片、文件等等，统称为MEDIA。

这些MEDIA都是有用的资源，我们往往希望根据某个URL，从浏览器上直接获取它们，比如：

- 访问https://www.liujiangblog.com/logo.jpg，浏览器会显示logo图片
- 访问https://www.liujiangblog.com/document.doc，浏览器会自动下载document文档

这些功能，一般都是在代码上线后，通过类似Ngnix的Web服务器代理实现的。

为了方便在开发过程中，对MEDIA资源的使用和测试，Django内置了一个serve()视图，帮我们实现了同样的功能。

但是要谨记：serve()视图只能用于开发环境！

使用步骤：

首先，在根路由urls中添加下面的代码：

```python
from django.conf import settings
from django.urls import re_path
from django.views.static import serve              # 以上三个导入不能忘

# ... 你原来的URLconf放这里...

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
```

然后：

1. 确认`settings.DEBUG`配置项为True，也就是出于开发模式
2. 在settings中添加下面的配置

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = '/media/'
```

1. 如果是windows操作系统，在你的Django项目所在的盘符的根目录下，新建一个`media`文件夹，将你的MEDIA资源全部拷贝进去，比如`c:\media`或者`d:\media`等等。
2. 启动开发服务器
3. 访问类似`127.0.0.1:8000/media/logo.jpg`的地址可以看到图片
4. 访问类似`127.0.0.1:8000/media/blog.md`的地址会自动下载blog.md文件

# [异步视图](https://www.liujiangblog.com/course/django/278)

暂略

# [HttpRequest对象](https://www.liujiangblog.com/course/django/138)

每当一个用户请求发送过来，Django将HTTP数据包中的相关内容，打包成为一个HttpRequest对象，并传递给视图函数作为第一位置参数，也就是request，供我们调用。

HttpRequest对象中包含了非常多的重要的信息和数据，应该熟练掌握它。

所有的请求和响应对象都位于`django.http`模块内。

## 一、属性

HttpRequest对象的大部分属性是只读的，除非特别注明。

### 1. HttpRequest.scheme

字符串类型，表示请求的协议种类，'http'或'https'。

### 2. HttpRequest.body

bytes类型，表示原始HTTP请求的正文。它对于处理非HTML形式的数据非常有用：二进制图像、XML等。如果要处理常规的表单数据，应该使用`HttpRequest.POST`。

还可以使用类似读写文件的方式从HttpRequest中读取数据，参见HttpRequest.read()。

### 3. HttpRequest.path

字符串类型，表示当前请求页面的完整路径，但是不包括协议名和域名。例如："/music/bands/the_beatles/"。

这个属性，常被用于我们进行某项操作时，如果不通过，返回用户先前浏览的页面。非常有用！

### 4. HttpRequest.path_info

在某些Web服务器配置下，主机名后的URL部分被分成脚本前缀部分和路径信息部分。`path_info` 属性将始终包含路径信息部分，不论使用的Web服务器是什么。使用它代替path可以让代码在测试和开发环境中更容易地切换。

例如，如果应用的WSGIScriptAlias设置为`/minfo`，那么`HttpRequest.path`等于`/music/bands/the_beatles/` ，而`HttpRequest.path_info`为`/minfo/music/bands/the_beatles/`。

### 5. HttpRequest.method

字符串类型，表示请求使用的HTTP方法。默认为大写。 像这样：

```python
if request.method == 'GET':
    do_something()
elif request.method == 'POST':
    do_something_else()
```

通过这个属性来判断请求的方法，然后根据请求的方法不同，在视图中执行不同的代码。

### 6. HttpRequest.encoding

字符串类型，表示提交的数据的编码方式（如果为None 则表示使用`DEFAULT_CHARSET`设置）。 这个属性是可写的，可以通过修改它来改变表单数据的编码。任何随后的属性访问（例如GET或POST）将使用新的编码方式。

### 7. HttpRequest.content_type

表示从`CONTENT_TYPE`头解析的请求的MIME类型。

### 8. HttpRequest.content_params

包含在`CONTENT_TYPE`标题中的键/值参数字典。

### 9 HttpRequest.GET

一个类似于字典的对象，包含GET请求中的所有参数，也就是类似http://example.com/?name=jack&age=18之中的name=jack和age=18。 详情参考QueryDict文档。

### 10. HttpRequest.POST

包含所有POST表单数据的键值对字典。 详情请参考QueryDict文档。 如果需要访问请求中的原始或非表单数据，可以使用`HttpRequest.body`属性。

注意：请使用`if request.method == "POST"`来判断一个请求是否POST类型，而不要使用`if request.POST`。

POST中不包含上传文件的数据。 

### 11. HttpRequest.COOKIES

包含所有Cookie信息的字典。 键和值都为字符串。可以类似字典类型的方式，在cookie中读写数据，但是注意cookie是不安全的，因此，不要写敏感重要的信息。

### 12. HttpRequest.FILES

一个类似于字典的对象，包含所有上传的文件数据。 HttpRequest.FILES中的每个键为`<input type="file" name="" />`中的name属性值。 HttpRequest.FILES中的每个值是一个`UploadedFile`对象。

要在Django中实现文件上传，就要靠这个属性！

如果请求方法是POST且请求的`<form>`中带有`enctype="multipart/form-data"`属性，那么HttpRequest.FILES将包含上传的文件的数据。 否则，FILES将为一个空的类似于字典的对象，属于被忽略、无用的情形。

### 13. HttpRequest.META

包含所有HTTP头部信息的字典。 可用的头部信息取决于客户端和服务器，下面是一些示例：

- CONTENT_LENGTH —— 请求正文的长度（以字符串计）。
- CONTENT_TYPE —— 请求正文的MIME类型。
- HTTP_ACCEPT —— 可接收的响应`Content-Type`。
- HTTP_ACCEPT_ENCODING —— 可接收的响应编码类型。
- HTTP_ACCEPT_LANGUAGE —— 可接收的响应语言种类。
- HTTP_HOST —— 客服端发送的Host头部。
- HTTP_REFERER —— Referring页面。
- HTTP_USER_AGENT —— 客户端的`user-agent`字符串。
- QUERY_STRING —— 查询字符串。
- REMOTE_ADDR —— 客户端的IP地址。想要获取客户端的ip信息，就在这里！
- REMOTE_HOST —— 客户端的主机名。
- REMOTE_USER —— 服务器认证后的用户，如果可用。
- REQUEST_METHOD —— 表示请求方法的字符串，例如"GET" 或"POST"。
- SERVER_NAME —— 服务器的主机名。
- SERVER_PORT —— 服务器的端口（字符串）。

以上只是比较重要和常用的，还有很多未列出。

从上面可以看到，除`CONTENT_LENGTH`和`CONTENT_TYPE`之外，请求中的任何HTTP头部键转换为META键时，都会将所有字母大写并将连接符替换为下划线最后加上`HTTP_`前缀。所以，一个叫做`X-Bender`的头部将转换成META中的`HTTP_X_BENDER`键。

### 13.HttpRequest.headers

一个不区分大小写、类似dict的对象，包含请求中HTTP头部的所有信息。

你在访问的时候，可以不区分大小写。

```shell
>>> request.headers
{'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6', ...}

>>> 'User-Agent' in request.headers
True
>>> 'user-agent' in request.headers
True

>>> request.headers['User-Agent']
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6)
>>> request.headers['user-agent']
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6)

>>> request.headers.get('User-Agent')
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6)
>>> request.headers.get('user-agent')
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6)
```

在模板系统中，可以通过下面的方式访问：

```html
{{ request.headers.user_agent }}
```

### 14. HttpRequest.resolver_match

对请求中的URL进行解析，获取一些相关的信息，比如namespace。

在视图中通过request.resolver_match.namespace的方式访问。

## 二、app带来的属性

下面的属性是app带来的：

### 1. HttpRequest.current_app

表示当前app的名字。url模板标签将使用它的值作为`reverse()`方法的`current_app`参数。

### 2. HttpRequest.urlconf

设置当前请求的根`URLconf`，用于指定不同的url路由进入口，这将覆盖settings中的`ROOT_URLCONF`设置。

将它的值修改为None，可以恢复使用`ROOT_URLCONF`设置。

### 3. HttpRequest.exception_reporter_filter

用于替代当前请求的 `DEFAULT_EXCEPTION_REPORTER_FILTER` 。

### 4.HttpRequest.exception_reporter_class

用于替代当前请求的`DEFAULT_EXCEPTION_REPORTER`。

## 三、中间件带来的属性

Django的contrib应用中包含的一些中间件会在请求上设置属性。

### 1. HttpRequest.session

来自`SessionMiddleware`中间件：一个可读写的，类似字典的对象，表示当前会话。我们要保存用户状态，回话过程等等，靠的就是这个中间件和这个属性。

### 2. HttpRequest.site

来自`CurrentSiteMiddleware`中间件：`get_current_site()`方法返回的Site或RequestSite的实例，代表当前站点是哪个。

Django是支持多站点的，如果你同时上线了几个站点，就需要为每个站点设置一个站点id。

### 3. HttpRequest.user

来自`AuthenticationMiddleware`中间件：表示当前登录的用户的`AUTH_USER_MODEL`的实例，这个模型是Django内置的Auth模块下的User模型。如果用户当前未登录，则user将被设置为`AnonymousUser`的实例。 

可以使用`is_authenticated`方法判断当前用户是否合法用户，如下所示：

```
if request.user.is_authenticated:
    ... # Do something for logged-in users.
else:
    ... # Do something for anonymous users.
```

## 四、方法

### 1. HttpRequest.get_host()

根据`HTTP_X_FORWARDED_HOST`和`HTTP_HOST`头部信息获取请求的原始主机。 如果这两个头部没有提供相应的值，则使用`SERVER_NAME`和`SERVER_PORT`。

例如："127.0.0.1:8000"

注：当主机位于多个代理的后面，`get_host()`方法将会失败。解决办法之一是使用中间件重写代理的头部，如下面的例子：

```
class MultipleProxyMiddleware:
    FORWARDED_FOR_FIELDS = [
        'HTTP_X_FORWARDED_FOR',
        'HTTP_X_FORWARDED_HOST',
        'HTTP_X_FORWARDED_SERVER',
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Rewrites the proxy headers so that only the most
        recent proxy is used.
        """
        for field in self.FORWARDED_FOR_FIELDS:
            if field in request.META:
                if ',' in request.META[field]:
                    parts = request.META[field].split(',')
                    request.META[field] = parts[-1].strip()
        return self.get_response(request)
```

### 2. HttpRequest.get_port()

使用META中`HTTP_X_FORWARDED_PORT`和`SERVER_PORT`的信息返回请求的始发端口。

### 3. HttpRequest.get_full_path()

返回包含完整参数列表的path。例如：`/music/bands/the_beatles/?print=true`

### 4. HttpRequest.build_absolute_uri(location)

返回location的绝对URI形式。 如果location没有提供，则使用`request.get_full_path()`的值。

例如："https://example.com/music/bands/the_beatles/?print=true"

注：不鼓励在同一站点混合部署HTTP和HTTPS，如果需要将用户重定向到HTTPS，最好使用Web服务器将所有HTTP流量重定向到HTTPS。

### 5. HttpRequest.get_signed_cookie(key, default=RAISE_ERROR, salt='', max_age=None)

从已签名的Cookie中获取值，如果签名不合法则返回django.core.signing.BadSignature。 

可选参数salt用来为密码加盐，提高安全系数。 `max_age`参数用于检查Cookie对应的时间戳是否超时。

范例：

```shell
>>> request.get_signed_cookie('name')
'Tony'
>>> request.get_signed_cookie('name', salt='name-salt')
'Tony' # assuming cookie was set using the same salt
>>> request.get_signed_cookie('non-existing-cookie')
...
KeyError: 'non-existing-cookie'
>>> request.get_signed_cookie('non-existing-cookie', False)
False
>>> request.get_signed_cookie('cookie-that-was-tampered-with')
...
BadSignature: ...
>>> request.get_signed_cookie('name', max_age=60)
...
SignatureExpired: Signature age 1677.3839159 > 60 seconds
>>> request.get_signed_cookie('name', False, max_age=60)
False
```

### 6. HttpRequest.is_secure()

如果使用的是Https，则返回True，表示连接是安全的。

### 7. HttpRequest.accepts(mime_type)

Django3.1新增。

如果请求头部接收的类型匹配mime_type参数，则返回True，否则返回False：

```shell
>>> request.accepts('text/html')
True
```

大多数浏览器默认的头部Accept设置是：`Accept: */*`，也就是说使用上面的accepts方法进行测试基本都会返回True。

### 8. HttpRequest.read(size=None)

### 9. HttpRequest.readline()

### 10. HttpRequest.readlines()

### 11. `HttpRequest.__iter__()`

上面的几个方法都是从HttpRequest实例读取文件数据的方法。

可以将HttpRequest实例直接传递到XML解析器，例如ElementTree：

```python
import xml.etree.ElementTree as ET
for element in ET.iterparse(request):
    process(element)
```

# [QueryDict对象](https://www.liujiangblog.com/course/django/139)

疑问，实际是怎么获得并使用这个对象的，这篇文章没有给出例子。



- QueryDict: 对HTTP请求数据包中携带的数据的封装
- QuerySet: 对从数据库中查询出来的数据进行的封装。

在HttpRequest对象中，GET和POST属性都是一个`django.http.QueryDict`的实例。也就是说你可以按本文下面提供的方法操作request.POST和request.GET。

request.POST或request.GET的QueryDict都是不可变，只读的。如果要修改它，需要使用QueryDict.copy()方法，获取它的一个拷贝，然后在这个拷贝上进行修改操作。



QueryDict 实现了Python字典数据类型的所有标准方法，因为它是字典的子类。

不同之处在于下面：

### `__init__(query_string=None, mutable=False, encoding=None)`

QueryDict实例化方法。**注意：QueryDict的键值是可以重复的！**

```
>>> QueryDict('a=1&a=2&c=3')
<QueryDict: {'a': ['1', '2'], 'c': ['3']}>
```

如果需要实例化可以修改的对象，添加参数mutable=True。

### fromkeys(iterable, value='', mutable=False, encoding=None)

循环可迭代对象中的每个元素作为键值，并赋予同样的值（来至value参数）。

```
>>> QueryDict.fromkeys(['a', 'a', 'b'], value='val')
<QueryDict: {'a': ['val', 'val'], 'b': ['val']}>
```

## `__getitem__(key)`

根据提供的key，返回对应的值。如果有多个值，返回最后那个。如果key不存在，弹出异常。

### `__setitem__(key, value)`

设置键值对。只能用于可变的QueryDict。

### `__contains__(key)`

如果QueryDict中有该key存在，返回True，否则False

### get(key, default=None)

和`QueryDict.__getitem__(key)`的作用一样，不同在于，如果key不存在，则返回default值。

### setdefault(key, default=None)

类似`__setitem__()`，字典的setdefault()方法。

### update(other_dict)

用新的QueryDict或字典更新当前QueryDict。类似`dict.update()`，但是追加内容，而不是更新并替换它们。 像这样：

```python
>>> q = QueryDict('a=1', mutable=True)
>>> q.update({'a': '2'})
>>> q.getlist('a')
['1', '2']
>>> q['a'] # returns the last
'2'
```

### items()

类似`dict.items()`，如果有重复项目，返回最近的一个，而不是都返回：

```shell
>>> q = QueryDict('a=1&a=2&a=3')
>>> q.items()
[('a', '3')]
```

### values()

类似`dict.values()`，但是只返回最近的值。 像这样：

```shell
>>> q = QueryDict('a=1&a=2&a=3')
>>> q.values()
['3']
```

### copy()

使用`copy.deepcopy()`返回QueryDict对象的副本。 此副本是可变的！

### getlist(key, default=None)

返回键对应的值列表。 如果该键不存在并且未提供默认值，则返回一个空列表。

### setlist(key, list_)

为`list_`设置给定的键。

### appendlist(key, item)

将键追加到内部与键相关联的列表中。

### setlistdefault(key, default_list=None)

类似setdefault()，除了它需要的是一个值的列表而不是单个值。

### lists()

类似items()，只是它将其中的每个键的值作为列表放在一起。 像这样：

```
>>> q = QueryDict('a=1&a=2&a=3')
>>> q.lists()
[('a', ['1', '2', '3'])]
```

### pop(key)

返回给定键的值的列表，并从QueryDict中移除该键。 如果键不存在，将引发KeyError。 像这样：

```
>>> q = QueryDict('a=1&a=2&a=3', mutable=True)
>>> q.pop('a')
['1', '2', '3']
```

### popitem()

删除QueryDict任意一个键，并返回二值元组，包含键和键的所有值的列表。在一个空的字典上调用时将引发KeyError。 像这样：

```
>>> q = QueryDict('a=1&a=2&a=3', mutable=True)
>>> q.popitem()
('a', ['1', '2', '3'])
```

### dict()

将QueryDict转换为Python的字典数据类型，并返回该字典。

如果出现重复的键，则将所有的值打包成一个列表，最为新字典中键的值。

```
>>> q = QueryDict('a=1&a=3&a=5')
>>> q.dict()
{'a': '5'}
```

### urlencode(safe=None)

已url的编码格式返回数据字符串。 像这样：

```
>>> q = QueryDict('a=2&b=3&b=5')
>>> q.urlencode()
'a=2&b=3&b=5'
```

使用safe参数传递不需要编码的字符。 像这样：

```
>>> q = QueryDict(mutable=True)
>>> q['next'] = '/a&b/'
>>> q.urlencode(safe='/')
'next=/a%26b/'
```

# HttpResponse对象

阅读: 31887                  [评论](https://www.liujiangblog.com/course/django/140#comments)：3            

------

HttpResponse类定义在django.http模块中。

HttpRequest对象是浏览器发送过来的请求数据的封装，HttpResponse对象则是你想要返回给浏览器的数据的封装。

HttpRequest对象由Django自动解析HTTP数据包而创建，而HttpResponse对象则由程序员手动创建。

我们编写的每个视图都要实例化、填充和返回一个HttpResponse对象。也就是函数的return值。

## 一、使用方法

### 1. 返回一个字符串

最简单的方式是传递一个string、bytes或者memoryview（Python3.8新增的一种类型）作为页面的内容到HttpResponse构造函数，并返回给用户:

```python
>>> from django.http import HttpResponse
>>> response = HttpResponse("Here's the text of the Web page.")
>>> response = HttpResponse("Text only, please.", content_type="text/plain")
>>> response = HttpResponse(b'Bytestrings are also accepted.')
>>> response = HttpResponse(memoryview(b'Memoryview as well.'))
```

可以将response看做一个类文件对象，使用wirte()方法不断地往里面增加内容。

```python
>>> response = HttpResponse()
>>> response.write("<p>Here's the text of the Web page.</p>")
>>> response.write("<p>Here's another paragraph.</p>")
```

### 2. 传递可迭代对象

你甚至可以传递一个可迭代的对象给HttpResponse。比如 StreamingHttpResponse 。

HttpResponse会立即处理这个迭代器，并把它的内容存成字符串，最后废弃这个迭代器。比如文件在读取后，会立刻调用close()方法，关闭文件。

### 3. 设置头部字段

可以把HttpResponse对象当作一个字典一样，在其中增加和删除头部字段。

```python
>>> response = HttpResponse()
>>> response['Age'] = 120
>>> del response['Age']
```

注意！与字典不同的是，如果要删除的头部字段如果不存在，del不会抛出KeyError异常。

HTTP的头部字段中不能包含换行。所以如果我们提供的头部字段值包含换行符（CR或者LF），将会抛出BadHeaderError异常。

### 4. 附件形式

让浏览器以文件附件的形式处理响应, 需要声明`content_type`类型和设置`Content-Disposition`头信息。 例如，给浏览器返回一个微软电子表格：

```python
>>> response = HttpResponse(my_data, content_type='application/vnd.ms-excel')
>>> response['Content-Disposition'] = 'attachment; filename="foo.xls"'
```

## 二、属性

| 属性          | 说明                                                         |
| ------------- | ------------------------------------------------------------ |
| content       | 响应的内容。bytes类型。                                      |
| charset       | 编码的字符集。 如果没指定，将会从`content_type`中解析出来。  |
| status_code   | 响应的状态码，比如200。                                      |
| reason_phrase | 响应的HTTP原因短语。 使用标准原因短语。<br />除非明确设置，否则`reason_phrase`由`status_code`的值决定。 |
| streaming     | 总是False。由于这个属性的存在，使得中间件能够区别对待流式响应和常规响应。 |
| closed        | 如果响应已关闭，那么这个属性的值为True。                     |

## 三、 方法

### `__init__()`

> ```
> __init__(content=b'', content_type=None, status=200, reason=None, charset=None)
> ```

响应的实例化方法。使用content参数和`content-type`实例化一个HttpResponse对象。

content:

- 迭代器: 这个迭代器返回的应是一串字符串，并且这些字符串连接起来形成response的内容。
- 字符串: 如果不是迭代器或者字符串，那么在其被接收的时候将转换成字符串。

`content_type`是可选地，用于填充HTTP的`Content-Type`头部。如果未指定，默认情况下由`DEFAULT_CONTENT_TYPE`和`DEFAULT_CHARSET`设置组成：`text/html; charset=utf-8`。

status是响应的状态码。reason是HTTP响应短语。charset是编码方式。

### `__setitem__(header, value)`

设置头部的键值对。两个参数都必须为字符串类型。

### `__delitem__(header)`

删除头部的某个键。键不存在的话，不会报错。不区分大小写。

```
__getitem__(header)
```

返回对应键的值。不区分大小写。

### has_header(header)

检查头部中是否有给定的名称（不区分大小写），返回True或 False。

### setdefault(header, value)

设置一个头部，除非该头部已经设置过了。

### set_cookie()

> set_cookie(key, value='', max_age=None, expires=None, path='/', domain=None, secure=False, httponly=False, samesite=None)

这个方法你必须会。

设置一个Cookie。 参数与Python标准库中的`Morsel.Cookie`对象相同。

max_age: 生存周期，以秒为单位。如果设为None，浏览器开启期间保持，关闭后一同删除。

expires：到期时间。

domain: 用于设置跨域的Cookie。例如`domain=".lawrence.com"`将设置一个`www.lawrence.com`、`blogs.lawrence.com`和`calendars.lawrence.com`都可读的Cookie。 否则，Cookie将只能被设置它的域读取。

secure=True：支持https

**httponly=True**：阻止客户端的js代码访问cookie

使用`samesite='Strict'`或`samesite='Lax'`告诉浏览器在执行跨源请求时不要发送此cookie。并非所有浏览器都支持SameSite，因此它不是Django的CSRF保护的替代品，而是一种深度防御措施。

使用`samesite='None'（string）`显式声明此cookie与所有相同站点和跨站点请求一起发送。

### set_signed_cookie()

> set_signed_cookie(key, value, salt='', max_age=None, expires=None,  path='/', domain=None, secure=False, httponly=False, samesite=None)

与`set_cookie()`类似，但是在设置之前将对cookie进行加密签名。通常与`HttpRequest.get_signed_cookie()`一起使用。 

### delete_cookie()

> delete_cookie(key, path='/', domain=None, samesite=None)

删除Cookie中指定的key。 

由于Cookie的工作方式，path和domain应该与`set_cookie()`中使用的值相同，否则Cookie不会删掉。

### close()

在请求结束后WSGI服务器会调用此方法，关闭连接

### write(content)

将HttpResponse实例看作类似文件的对象，往里面添加内容。

### flush()

清空HttpResponse实例的内容。

### tell()

将HttpResponse实例看作类似文件的对象，移动位置指针。

### getvalue()

返回HttpResponse.content的值。 此方法将HttpResponse实例看作是一个类似流的对象。

### readable()

返回的值始终为False。判断是否可读

### seekable()

值始终为False。判断指针是否可以移动。

### writable()

值始终为True。判断是否可写。

### writelines(lines)

将一个包含行的列表写入响应对象中。 不添加分行符。

## 四、HttpResponse的子类

Django包含了一系列的HttpResponse的衍生类（子类），用来处理不同类型的HTTP响应。与HttpResponse相同, 这些衍生类存在于`django.http`之中。这些子类并不算复杂，代码也很简单，主要就是响应码的不同。

- class HttpResponseRedirect：重定向，返回302状态码。已经被redirect()替代。
- class HttpResponsePermanentRedirect:永久重定向，返回301状态码。
- class HttpResponseNotModified：未修改的页面，返回304状态码。
- class HttpResponseBadRequest：错误的请求，返回400状态码。
- class HttpResponseNotFound：页面不存在，返回404状态码。
- class HttpResponseForbidden：禁止访问，返回403状态码。
- class HttpResponseNotAllowed：禁止访问，返回405状态码。
- class HttpResponseGone：过期，返回405状态码。
- class HttpResponseServerError：服务器错误，返回500状态码。

其实，你还可以自定义HttpResponse的子类，如下所示：

```python
from http import HTTPStatus
from django.http import HttpResponse

class HttpResponseNoContent(HttpResponse):
    status_code = HTTPStatus.NO_CONTENT
```

## 五、JsonResponse类

> class JsonResponse(data, encoder=DjangoJSONEncoder, safe=True, json_dumps_params=None, **kwargs)

JsonResponse是HttpResponse的一个子类，是Django提供的用于创建JSON编码类型响应的快捷类。 

它从父类继承大部分行为，并具有以下不同点：

- 它的Content-Type头部为`application/json`
- 它的第一个参数data，应该为一个字典数据类型。
- 只有将safe参数设置为False，才可以将任何可JSON 序列化的对象作为data的参数值，否则会报错。

encoder默认为`django.core.serializers.json.DjangoJSONEncoder`，用于序列化数据。 

典型的用法如下：

```shell
>>> from django.http import JsonResponse
>>> response = JsonResponse({'foo': 'bar'})
>>> response.content
b'{"foo": "bar"}'
```

若要序列化非dict对象，必须设置safe参数为False：

```shell
>>> response = JsonResponse([1, 2, 3], safe=False)
```

如果不传递safe=False，将抛出一个TypeError。

如果你需要使用不同的JSON 编码器类，可以传递encoder参数给构造函数：

```shell
>>> response = JsonResponse(data, encoder=MyJSONEncoder)
```

## 六、StreamingHttpResponse类

StreamingHttpResponse类被用来从Django响应一个流式对象到浏览器。如果生成的响应太长或者是占用的内存较大，这么做更有效率。 例如，生成大型的CSV文件。

StreamingHttpResponse不是HttpResponse的子类（而是兄弟类），但是除了几个明显不同的地方，两者几乎完全相同：

- StreamingHttpResponse接收一个迭代器作为参数。这个迭代器返回bytes类型的字符内容。
- StreamingHttpResponse的内容是一个整体的对象，不能直接访问修改
- StreamingHttpResponse有一个 `streaming_content`属性
- 你不能在StreamingHttpResponse上使用类似文件操作的tell和write方法

由于StreamingHttpResponse的内容无法访问，因此许多中间件无法正常工作。例如，不能为流式响应生成ETag和Content-Length头。

StreamingHttpResponse对象有下面的属性

- **streaming_content**：一个包含响应内容的迭代器，通过HttpResponse.charset编码为bytes类型。
- **status_code**：响应的状态码
- **reason_phrase**：响应的原语
- **streaming**：总是为True

## 七、FileResponse

> class FileResponse(open_file, as_attachment=False, filename='', **kwargs)

文件类型响应。通常用于给浏览器返回一个文件附件。

FileResponse是StreamingHttpResponse的子类，为二进制文件专门做了优化。

FileResponse需要通过二进制模式打开文件，如下:

```
>>> from django.http import FileResponse
>>> response = FileResponse(open('myfile.png', 'rb'))
```

文件会被自动关闭，所以不需要在上下文管理器中打开。

如果 `as_attachment=True`，则Content-`Disposition` 被设置为 `attachment`,，告诉浏览器这是一个附件，以文件形式下载。否则 `Content-Disposition` 会被设置为 `inline` (浏览器默认行为)。

如果open_file参数传递的类文件对象没有名字，或者名字不合适，那么你可以通过filename参数为文件对象指定一个合适的名字。

# 文件上传

Django在处理文件上传时，文件数据会被打包封装在`request.FILES`中。 

## 文件上传

### 一、简单上传，手动保存

首先，写一个form模型，它必须包含一个`FileField`：

```python
from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
```

处理这个表单的视图将在`request.FILES`中收到文件数据，可以用`request.FILES['file']`来获取上传文件的具体数据，其中的键值`'file'`是根据`file = forms.FileField()`的变量名来的。

**注意**：`request.FILES`只有在请求方法为POST,并且提交请求的`<form>`具有`enctype="multipart/form-data"`属性时才有效。 否则，`request.FILES`将为空。

下面是一个接收上传文件的视图范例：

```python
# views.py

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm

# 另外写一个处理上传过来的文件的方法，并在这里导入
from somewhere import handle_uploaded_file

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})  # 思考一下这个return语句是否可以缩进到else语句中呢？
```

请注意，必须将`request.FILES`传递到form的构造函数中。

```python
form = UploadFileForm(request.POST, request.FILES)
```

下面是一个处理上传文件的方法的参考例子：

```python
def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
```

遍历`UploadedFile.chunks()`，而不是直接使用`read()`方法，能确保大文件不会占用系统过多的内存。

### 二、 使用模型处理上传的文件

如果是通过模型层的model来指定上传文件的保存方式的话，使用ModelForm更方便。 调用`form.save()`的时候，文件对象会保存在相应的`FileField`的`upload_to`参数指定的地方。

```python
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import ModelFormWithFileField

def upload_file(request):
    if request.method == 'POST':
        form = ModelFormWithFileField(request.POST, request.FILES)
        if form.is_valid():
            # 这么做就可以了，文件会被保存到Model中upload_to参数指定的位置
            form.save()
            return HttpResponseRedirect('/success/url/')
    else:
        form = ModelFormWithFileField()
    return render(request, 'upload.html', {'form': form})
```

如果手动构造一个对象，还可以简单地把文件对象直接从`request.FILES`赋值给模型：

```python
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from .models import ModelWithFileField

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = ModelWithFileField(file_field=request.FILES['file'])
            instance.save()
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
```

### 三、 同时上传多个文件

如果要使用一个表单字段同时上传多个文件，需要设置字段HTML标签的multiple属性为True，如下所示：

```python
# forms.py

from django import forms

class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
```

然后，自己编写一个`FormView`的子类，并覆盖它的post方法，来处理多个文件上传：

```python
# views.py
from django.views.generic.edit import FormView
from .forms import FileFieldForm

class FileFieldView(FormView):
    form_class = FileFieldForm
    template_name = 'upload.html'  # 用你的模版名替换.
    success_url = '...'  # 用你的URL或者reverse()替换.

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            for f in files:
                ...  # 对每个文件做处理
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
```

### 四、关于上传文件的处理器

当用户上传一个文件的时候，Django会把文件数据传递给上传文件处理器。 

上传处理器的配置定义在`FILE_UPLOAD_HANDLERS`中，默认为：

```python
["django.core.files.uploadhandler.MemoryFileUploadHandler", "django.core.files.uploadhandler.TemporaryFileUploadHandler"]
```

`MemoryFileUploadHandler`和`TemporaryFileUploadHandler`定义了Django的默认文件上传行为：将小文件读取到内存中，大文件放置在磁盘中。

你可以编写自己的 handlers 来自定义如何处理文件。比如，你可以使用自定义强制处理用户层面的配额，动态压缩数据，渲染进度条，甚至可以将数据发送到其他存储地址而不是本地。

在你保存上传文件之前，数据需要储存在某个地方。通常，如果上传文件小于2.5MB，Django会把整个内容存到内存。 这意味着，文件的保存仅仅涉及到内存中的读取和磁盘的写入，所以非常快。

但是，如果上传的文件很大，Django会把它写入一个临时文件，储存在你的系统临时目录中。在类Unix的平台下，Django会生成一个文件，名称类似于`/tmp/tmpzfp6I6.upload`。

### 五、动态修改上传处理器

有时候某些视图需要不同的上传行为。也就是说，在视图中动态修改处理器列表，即`request.upload_handlers`

比如，假设你正在编写 `ProgressBarUploadHandler` ，用来提供上传过程中的反馈。你需要添加这个处理程序到你的上传处理模块：

```
request.upload_handlers.insert(0, ProgressBarUploadHandler(request))
```

在这里使用 `list.insert()` （而不是 `append()` ），因为进度条处理程序需要在其他处理程序之前使用。

**记住，列表中的上传处理程序是按顺序处理的。**

如果你想完全替换掉先前的上传处理程序，只需要指定新列表：

```
request.upload_handlers = [ProgressBarUploadHandler(request)]
```

**你只能在访问 `request.POST` 或 `request.FILES` 之前修改上传处理程序**。开始上传动作后修改上传处理程序没有意义，并且Django 会报错。

而且，默认的，   `CsrfViewMiddleware`中间件会访问`request.POST`。这意味着你需要在视图上使用 `csrf_exempt()` 来允许你改变上传处理程序。然后你需要在实际处理请求的函数上使用 `csrf_protect()` 。注意这可能会让处理程序在 CSRF 检测完成之前开始接受文件上传。如下所示：

```
from django.views.decorators.csrf import csrf_exempt, csrf_protect

@csrf_exempt
def upload_file_view(request):
    request.upload_handlers.insert(0, ProgressBarUploadHandler(request))
    return _upload_file_view(request)

@csrf_protect
def _upload_file_view(request):
    ... # Process request
```

## 全局概念

在详细介绍Django对文件进行处理的功能之前，我们要了解一些它的基本概念、组织方式、使用套路、主要的类和继承关系。

如果你不了解这些，那么复杂的源码、交错的官方文档会让你陷入泥坑。不知道怎么用？什么时候用？用什么？为什么这么用？整个一团乱！

这些代码都位于`django.core.files`模块中，它们主要包括：

- File的概念：Django对Python文件的封装。既可以用于文件上传过程中的处理，也可以单独使用
- `File`类：Django实现File的基类
- `ContentFile`类：继承了File类，不同之处是它处理的是字符串
- `ImageFile` 类：继承了File类，添加了图像的宽度和长度像素值
- `File`类的其它子类：实际上Django为`File`类还编写了一系列`Upload...`子类，只是使用较少。
- File storage的概念：将Django的File对象保存到存储系统的API库，也就是Django如何将数据保存到硬盘中的。
- `settings.DEFAULT_FILE_STORAGE`:一个Django配置项，用来指定默认的文件存储类。默认值为`'django.core.files.storage.FileSystemStorage'`，在`globa_settings`中。
- `get_storage_class()`方法：Django提供的一个函数，通过字符串反射的方式获取指定的存储类或者`DEFAULT_FILE_STORAGE`设置的存储类
- `DefaultStorage`类:对`get_storage_class()`方法返回的对象类的进一步封装
- `default_storage`:`DefaultStorage`类的实例
- `Storage`类：Django源码中所有存储类的基类，提供通用的接口API
- `FileSystemStorage`：继承了`Storage`类，是Django原生实现的最重要、最常用、最普通的存储类。我们绝大多数时间实际使用的就是它！

## File 对象

Django设计了自己的文件对象。要记住，Django的File对象可以脱离本章的文件上传概念，独立使用！

### File 类

File 类是围绕Python原生file对象的轻度包装，添加了一些Django特有的东西。Django在内部使用File类的实例来表示文件对象。

每个File对象都包含下面的属性和方法：

- name：文件名。包括`MEDIA_ROOT`定义的相对路径部分。
- size：文件的尺寸，字节单位。
- file：注意，这是File对象的file属性，不要搞混淆了！它表示File类封装的底层文件对象（Python文件对象）。
- mode：文件的读/写模式
- open(mode=None)：打开或者重新打开文件。mode参数和Python内置的open方法的参数一样。可以使用上下文管理器`with file.open() as f:`
- `__iter__()`：遍历文件一次生成一行。
- chunks(chunk_size=None)：遍历文件，分割成指定大小的“块”。`chunk_size` 默认为64 KB。这对于非常大的文件特别有用，因为它允许从磁盘流式传输，避免将整个文件存储在内存中。
- multiple_chunks(chunk_size=None)：以指定的`chunk_size`进行测试，如果文件大到需要分割成多个数据块进行访问，则返回`True`，否则返回False。
- close()：关闭文件

除以上属性和方法之外，还有下面的方法：

- `encoding`
- `fileno`
- `flush`
- `isatty`
- `newlines`
- `read`
- `readinto`
- `readline`
- `readlines`
- `seek`
- `tell`
- `truncate`
- `write`
- `writelines`,
- `readable()`
- `writable()`
- `seekable()`

望文生义，它们都和Python原生的文件操作方法类似。

如果你想创建一个 `File` 实例，最简单的方法是使用 Python 内置的 `file` 对象：

```
>>> from django.core.files import File

# 使用Python原生的open()方法
>>> f = open('/path/to/hello.world', 'w')
>>> myfile = File(f)
```

注意在这里创建的文件不会自动关闭。下面的方式可以用来自动关闭文件：

```
>>> from django.core.files import File

# Create a Python file object using open() and the with statement
>>> with open('/path/to/hello.world', 'w') as f:
...     myfile = File(f)
...     myfile.write('Hello World')
...
>>> myfile.closed
True
>>> f.closed
True
```

如果文件在访问后没有关闭，可能会出现文件描述符溢出的风险。

```
OSError: [Errno 24] Too many open files
```

### ContentFile类

`ContentFile`类直接继承了`File`类，但是前者操作的是字符串或者字节内容，而不是确切的文件。例如：

```
from django.core.files.base import ContentFile

f1 = ContentFile("esta frase está en español")
f2 = ContentFile(b"these are bytes")
```

### ImageFile 类

Django为图片特别提供了一个内置类，也就是`django.core.files.images.ImageFile`，它也继承了File类。只是额外增加了两个属性：

- width： 图片的像素宽度
- height：图片的像素高度

比如下面的模型，使用 `ImageField` 来存储照片：

```
from django.db import models

class Car(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    photo = models.ImageField(upload_to='cars')
```

所有的 Car 实例都拥有一个 photo 属性，你可以使用它来获取照片的详细信息：

```
>>> car = Car.objects.get(name="57 Chevy")
>>> car.photo
<ImageFieldFile: cars/chevy.jpg>
>>> car.photo.name
'cars/chevy.jpg'
>>> car.photo.path      # 图片在文件系统中的路径
'/media/cars/chevy.jpg'
>>> car.photo.url   # 访问图片的url
'http://media.example.com/cars/chevy.jpg'
```

`car.photo` 其实是一个 `File` 对象，这意味着它拥有下面所描述的所有方法和属性。

可以通过将文件名设置为相对于文件存储位置的路径来更改文件名（如果你正在使用默认的 FileSystemStorage ，则为 MEDIA_ROOT ）。

```
>>> import os
>>> from django.conf import settings
>>> initial_path = car.photo.path
>>> car.photo.name = 'cars/chevy_ii.jpg'
>>> new_path = settings.MEDIA_ROOT + car.photo.name
>>> # Move the file on the filesystem
>>> os.rename(initial_path, new_path)
>>> car.save()
>>> car.photo.path
'/media/cars/chevy_ii.jpg'
>>> car.photo.path == new_path
True
```

更多的 `ImageField` 使用例子：

```
>>> from PIL import Image
>>> car = Car.objects.get(name='57 Chevy')
>>> car.photo.width
191
>>> car.photo.height
287
>>> image = Image.open(car.photo)
# 抛出ValueError异常。因为你在尝试打开已经关闭的文件

>>> car.photo.open()  # 打开文件
<ImageFieldFile: cars/chevy.jpg>
>>> image = Image.open(car.photo)  # 再次创建Image实例
>>> image
<PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=191x287 at 0x7F99A94E9048>
```

另外，此时这个File对象会有两个附加的方法save和delete：

- File.save（name，content，save = True）

使用提供的文件名和内容保存一个新的文件。这不会替换现有文件，但会创建一个新文件并更新该对象以指向该文件（也就是说保留外面那层用来封装的皮，把内部实际的文件内容替换掉）。如果save=True，将立刻执行模型的save方法。

```
>>> car.photo.save('myphoto.jpg', content, save=False)
>>> car.save()
# 等同于
>>> car.photo.save('myphoto.jpg', content, save=True)
```

- File.delete（save = True）

从模型实例中删除文件。如果save=True，删除文件后将立刻执行模型的save方法。

## File storage 类

### 获取当前存储类

在本章的一开始，我们实现了一个简单的文件上传例子。用户从浏览器通过POST发送过来文件数据，Django通过`request.FILES`拿到数据，然后我们简单粗暴地使用Python语言原生的文件操作API将数据保存到了文件系统中，通常也就是硬盘中。

Django为了方便我们，提供了存储类，用来帮助我们将数据保存到存储器中，不需要手动调用open方法。

你在模型中可能看到过这样的写法：

```
file=models.FileField(storage='xxx',......)
```

其中的storage参数就是我们要指定的存储器类。如果你不指定这个参数，Django就会使用settings中配置的默认存储类进行处理。

所以，我们首先要知道`DEFAULT_FILE_STORAGE`配置项，它指定Django默认的存储类，默认值为`'django.core.files.storage.FileSystemStorage'`。一般情况下，我们无感静默使用，什么都不用做。

但是，Django总是千方百计为我们开后门，提供钩子。

Django额外又为我们提供了三种获取存储类的简便方法，用于在代码中动态修改要使用的存储类：

- `get_storage_class`(import_path=None)

先看看它的源代码：

```
def get_storage_class(import_path=None):
    return import_string(import_path or settings.DEFAULT_FILE_STORAGE)
```

就两行！

它的作用是返回实现了存储API的存储类或者模块。

如果不提供参数，就使用`settings.DEFAULT_FILE_STORAGE`，也就是上面说的。

如果提供参数，Django将使用Python的字符串反射机制，获取对应的模块。

`get_storage_class`方法可以用在任何地方，它不属于任何类，是个独立函数。

- `DefaultStorage`类

看看它的源代码：

```
class DefaultStorage(LazyObject):
    def _setup(self):
        self._wrapped = get_storage_class()()
```

三行！调用上面的`get_storage_class`方法并实例化，然后赋值给`_wrapped`，最后获得的就是`'django.core.files.storage.FileSystemStorage'`。

- `default_storage`变量

源代码如下：

```
default_storage = DefaultStorage()
```

根本就是`DefaultStorage`的一个实例。所以，`from django.core.files.storage import default_storage`其实就是获得了一个`FileSystemStorage`对象。

看下面的例子：

```
>>> from django.core.files.base import ContentFile
>>> from django.core.files.storage import default_storage

# 注意，这个save方法是有返回值的！返回值是文件在存储系统中的路径。可以通过这个路径再去查找文件。
>>> path = default_storage.save('path/to/file', ContentFile(b'new content'))
>>> path
'path/to/file'

>>> default_storage.size(path)
11
>>> default_storage.open(path).read()
b'new content'

>>> default_storage.delete(path)
>>> default_storage.exists(path)
False
```

### Storage类

Storage类是Django为我们提供的存储基类，实现了一些标准的API和一些可以被子类重写的默认行为。

name参数：文件名

- `delete`(*name*)：删除指定名字的文件。如果子类没有实现这个方法，会弹出`NotImplementedError` 异常。
- `exists`(*name*)： 如果文件已经存在，返回True，否则False
- `get_accessed_time`(*name*): 返回上次访问该文件的时间，以`datetime`类型。如果子类没有实现这个方法，会弹出`NotImplementedError` 异常。
- `get_alternative_name`(*file_root*, *file_ext*)：返回基于`file_root`和 `file_ext`参数的备用文件名，在扩展名之前，在文件名后附加一个下划线和一个随机的7个字符的字母数字字符串。3.0新增。
- `get_available_name`(*name*, *max_length=None*)：据`name`参数返回自由可用的文件名。文件名的长度将不超过`max_length`（如果提供）。如果找不到自由的唯一文件名，则会引发`SuspiciousFileOperation`异常 。
- `get_created_time`(*name*)： 返回文件的创建时间。如果子类没有实现这个方法，会弹出`NotImplementedError` 异常。
- `get_modified_time`(*name*)：返回上次修改该文件的时间，以`datetime`类型。如果子类没有实现这个方法，会弹出`NotImplementedError` 异常。
- `get_valid_name`(*name*)：根据`name`参数，返回一个在目标存储系统上可用的合法文件名。
- `generate_filename`(*filename*)：验证并返回一个文件名。
- `listdir`(*path*)： 列出指定path下的内容，然会一个列表的二元元组。第一个元素是目录列表，第二个元素是文件列表。如果子类没有实现这个方法，会弹出`NotImplementedError` 异常。
- `open`(*name*, *mode='rb'*)：以指定的mode打开文件
- `path`(*name*)：返回文件的路径，通过该路径可以使用Python原生的open()方法打开文件。如果子类没有实现这个方法，会弹出`NotImplementedError` 异常。
- `save`(*name*, *content*, *max_length=None*)：保存文件。如果文件名已经存在，会自动修改生成合适的文件名。content参数必须是一个`django.core.files.File`的实例，或者可以被File包装的类文件对象。
- `size`(*name*)：返回文件的大小，字节单位。如果子类没有实现这个方法，会弹出`NotImplementedError` 异常。
- `url`(*name*)：返回URL，通过该URL可以访问文件的内容。如果子类没有实现这个方法，会弹出`NotImplementedError` 异常。

方法很多，不一定全要掌握，重点是下面这几个：

- delete
- exists
- listdir
- open
- path
- save
- size
- url

### FileSystemStorage 类

实际上，我们不直接使用Storage类，而是使用FileSystemStorage 类，这也是Django实现的唯一的本地文件系统存储类。

> `FileSystemStorage`（*location = None*，*base_url = None*，*file_permissions_mode = None*，*directory_permissions_mode = None*）

FileSystemStorage类直接继承了Storage类，并提供了下面的额外属性：

- `location`： 存放文件的目录的绝对路径。默认为`MEDIA_ROOT`设置的值。
- `base_url`： 用于访问文件的URL的基础前缀。默认为`MEDIA_URL`的值。
- `file_permissions_mode`： 文件的系统权限。默认为`FILE_UPLOAD_PERMISSIONS`配置项的值。
- `directory_permissions_mode`：目录的系统权限。默认为`FILE_UPLOAD_DIRECTORY_PERMISSIONS`配置项的值。

FileSystemStorage类实现了全套的我们在Storage类中介绍过的子类必须实现的方法。

但是要注意， `FileSystemStorage.delete()` 方法如果删除不存在的文件，不会引发异常。

下面的代码将上传文件存储到 `/media/photos` ，而不是你在 `MEDIA_ROOT` 中设置的路径：

```
from django.core.files.storage import FileSystemStorage
from django.db import models

# 自定义存储路径
fs = FileSystemStorage(location='/media/photos')

class Car(models.Model):
    ...
    photo = models.ImageField(storage=fs)
```

Django 3.1开始，`FileSystemStorage.save()`方法支持使用`pathlib.Path`类，并且支持回调函数形式的storage参数，如下所示：

```
from django.conf import settings
from django.db import models
from .storages import MyLocalStorage, MyRemoteStorage


def select_storage():
    return MyLocalStorage() if settings.DEBUG else MyRemoteStorage()


class MyModel(models.Model):
    my_file = models.FileField(storage=select_storage)
```

这就赋予了我们在运行过程中，动态选择存储类的能力。

## 自定义Storage类

如果你需要自定义文件储存功能，比如把文件储存在远程系统中，你可以自己编写Storage类来实现这一功能。

实际上大多数情况下，对于本地磁盘存储，我们直接使用`FileSystemStorage`即可，对于别的需求，一般有第三方的存储类可用，在Django的生态库里查找即可。自己编写Storage类存在可靠性、可用性、安全性、性能问题，新手绕行，老手慎重。

但无论如何，这里还是给出基本的编写要求，以供参考：

第一：必须继承 `Django.core.files.storage.Storage`

```
from django.core.files.storage import Storage

class MyStorage(Storage):
    ...
```

第二：Django 必须能以无参数的状态，实例化你的存储系统。这意味着所有的设置项都应从 `dango.conf.settings` 中获取:

```
from django.conf import settings
from django.core.files.storage import Storage

class MyStorage(Storage):
    def __init__(self, option=None):
        if not option:
            option = settings.CUSTOM_STORAGE_OPTIONS
        ...
```

第三：在你的存储类中，除了其他自定义的方法外，还必须实现 `_open()` 以及 `_save()` 方法。另外，如果你的类提供了本地文件存储功能，还必须重写 `path()` 方法。

第四：你的存储类必须是 `deconstructible`可解构的，以便在迁移中的字段上使用它时可以序列化。

第五：尽量实现下列方法：

- `Storage.delete()`
- `Storage.exists()`
- `Storage.listdir()`
- `Storage.size()`
- `Storage.url()`

举例来说，如果列出某些存储后端的内容的代价很昂贵，那么你可以不实现 `Storage.listdir()` 方法。

另一个例子是只处理写入文件的后端。在这种情况下，你不需要实现上述任何方法。

------

另外，下面是经常会用到专为自定义存储对象设计的两个钩子函数：

- `_open`(*name*, *mode='rb'*)：真正执行打开文件功能的方法。它将被 `Storage.open()` 调用。
- `_save`(*name*, *content*)：真正执行保存功能的方法。它将被 `Storage.save()`调用。

# 生成CSV文件

CSV (Comma Separated  Values)，以纯文本形式存储数字和文本数据的存储方式。纯文本意味着该文件是一个字符序列，不含必须像二进制数字那样的数据。CSV文件由任意数目的记录组成，记录间以某种换行符分隔；每条记录由字段组成，字段间的分隔符是其它字符或字符串，最常见的是逗号或制表符。通常，所有记录都有完全相同的字段序列。

CSV最常用的场景就是数据分析和机器学习中源数据的载体。

要在Django的视图中生成CSV文件，可以使用Python的CSV库或者Django的模板系统来实现。

## 一、使用Python的CSV库

Python自带处理CSV文件的标准库csv。csv模块的CSV文件创建功能作用于类似于文件对象创建，并且Django的HttpResponse对象也是类似于文件的对象。

下面是个例子：

```python
import csv
from django.http import HttpResponse

def some_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

    return response
```

相关说明：

- 响应对象的MIME类型设置为`text/csv`，告诉浏览器，返回的是一个CSV文件而不是HTML文件。 
- 响应对象设置了附加的`Content-Disposition`协议头，含有CSV文件的名称。文件名随便取，浏览器会在“另存为...”对话框等环境中使用它。
- 要在生成CSV的API中使用钩子非常简单：只需要把response作为第一个参数传递给`csv.writer`。`csv.writer`方法接受一个类似于文件的对象，而HttpResponse对象正好就是这么个东西。
- 对于CSV文件的每一行，调用`writer.writerow`，向它传递一个可迭代的对象比如列表或者元组。
- CSV模板会为你处理各种引用，不用担心没有转义字符串中的引号或者逗号。只需要向writerow()传递你的原始字符串，它就会执行正确的操作。

当处理大尺寸文件时，可以使用Django的`StreamingHttpResponse`类，通过流式传输，避免负载均衡器在服务器生成响应的时候断掉连接，提高传输可靠性。

在下面的例子中，利用Python的生成器来有效处理大尺寸CSV文件的拼接和传输：

```python
import csv

from django.http import StreamingHttpResponse

class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value

def some_streaming_csv_view(request):
    """A view that streams a large CSV file."""
    # Generate a sequence of rows. The range is based on the maximum number of
    # rows that can be handled by a single sheet in most spreadsheet
    # applications.
    rows = (["Row {}".format(idx), str(idx)] for idx in range(65536))
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    return response
```

## 二、使用Django的模板系统

也可以使用Django的模板系统来生成CSV。比起便捷的Python-csv库，这样做比较低级，不建议使用，这里只是展示一下有这种方式而已。

思路是，传递一个项目的列表给你的模板，并且让模板在for循环中输出逗号。下面是一个例子，它像上面一样生成相同的CSV文件：

```
from django.http import HttpResponse
from django.template import loader

def some_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    # The data is hard-coded here, but you could load it from a database or
    # some other source.
    csv_data = (
        ('First row', 'Foo', 'Bar', 'Baz'),
        ('Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"),
    )

    t = loader.get_template('my_template_name.txt')
    c = {'data': csv_data}
    response.write(t.render(c))
    return response
```

然后，创建模板`my_template_name.txt`，带有以下模板代码：

```
{% for row in data %}"{{ row.0|addslashes }}", "{{ row.1|addslashes }}", "{{ row.2|addslashes }}", "{{ row.3|addslashes }}", "{{ row.4|addslashes }}"
{% endfor %}
```

# 生成PDF文件

阅读: 16902                  [评论](https://www.liujiangblog.com/course/django/143#comments)：3            

------

可以通过开源的Python PDF库`ReportLab`来实现PDF文件的动态生成。

## 一、安装ReportLab

ReportLab库在PyPI上提供，可以使用pip来安装：

```
$ pip install reportlab
```

在Python交互解释器中导入它来测试安装：

```
>>> import reportlab
```

如果没有抛出任何错误，证明已安装成功。

## 二、编写视图

利用 Django 动态生成 PDF 的关键是 ReportLab API 作用于类文件对象，而 Django 的 `FileResponse` 对象接收类文件对象。

这有个 "Hello World" 示例:

```
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

def some_view(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
```

相关说明：

- MIME会自动设置为`application/pdf`。 

- 将 `as_attachment=True` 传递给 `FileResponse` 时，表示这是一个可下载附件，它会设置合适的 `Content-Disposition` 头，告诉 Web 浏览器弹出一个对话框，提示或确认如何处理该文档，即便设备已配置默认行为。若省略了 `as_attachment` 参数，浏览器会用已配置的用于处理 PDF 的程序或插件来处理该 PDF。

- 你也可以提供可选参数 `filename`。浏览器的`“另存为…”`对话框会用到它。

- 注意，所有后续生成 PDF 的方法都是在 PDF 对象上调用的（本例中是 `p`）——而不是在 `buffer` 上调用。

- 最后，牢记在 PDF 文件上调用 `showPage()` 和 `save()`。

- 注意：ReportLab并不是线程安全的。生成PDF文件

  阅读: 16902                  [评论](https://www.liujiangblog.com/course/django/143#comments)：3            

  ------

  可以通过开源的Python PDF库`ReportLab`来实现PDF文件的动态生成。

  ## 一、安装ReportLab

  ReportLab库在PyPI上提供，可以使用pip来安装：

  ```
  $ pip install reportlab
  ```

  在Python交互解释器中导入它来测试安装：

  ```
  >>> import reportlab
  ```

  如果没有抛出任何错误，证明已安装成功。

  ## 二、编写视图

  利用 Django 动态生成 PDF 的关键是 ReportLab API 作用于类文件对象，而 Django 的 `FileResponse` 对象接收类文件对象。

  这有个 "Hello World" 示例:

  ```
  import io
  from django.http import FileResponse
  from reportlab.pdfgen import canvas
  
  def some_view(request):
      # Create a file-like buffer to receive PDF data.
      buffer = io.BytesIO()
  
      # Create the PDF object, using the buffer as its "file."
      p = canvas.Canvas(buffer)
  
      # Draw things on the PDF. Here's where the PDF generation happens.
      # See the ReportLab documentation for the full list of functionality.
      p.drawString(100, 100, "Hello world.")
  
      # Close the PDF object cleanly, and we're done.
      p.showPage()
      p.save()
  
      # FileResponse sets the Content-Disposition header so that browsers
      # present the option to save the file.
      buffer.seek(0)
      return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
  ```

  相关说明：

  - MIME会自动设置为`application/pdf`。 
  - 将 `as_attachment=True` 传递给 `FileResponse` 时，表示这是一个可下载附件，它会设置合适的 `Content-Disposition` 头，告诉 Web 浏览器弹出一个对话框，提示或确认如何处理该文档，即便设备已配置默认行为。若省略了 `as_attachment` 参数，浏览器会用已配置的用于处理 PDF 的程序或插件来处理该 PDF。
  - 你也可以提供可选参数 `filename`。浏览器的`“另存为…”`对话框会用到它。
  - 注意，所有后续生成 PDF 的方法都是在 PDF 对象上调用的（本例中是 `p`）——而不是在 `buffer` 上调用。
  - 最后，牢记在 PDF 文件上调用 `showPage()` 和 `save()`。
  - 注意：ReportLab并不是线程安全的。

# 类视图

------

Django的视图可以分为：

- 函数视图FBV：`def index(request):`
- 类视图CBV：`class AboutView(TemplateView):`

早期，人们在视图开发中发现了一些常见的习语和句式，也就是重复性代码和工作。于是引入了基于函数的视图来抽象这些模式，便于一般情况下的视图开发。

基于函数的视图的问题在于，尽管它们覆盖了简单的情况，但是除了一些简单的配置选项之外，没有办法扩展或定制它们，限制了它们在许多现实应用中的实用性。

基于类的通用视图与基于函数的视图的目标相同，都是想让视图开发更容易。但由于类视图可以使用MIXIN等一些面向对象的方法和工具包，使得基于类的视图比基于函数的视图更具扩展性和灵活性。

基于类的视图：

- 通过HTTP请求方法的不同，将代码分隔在不同的类方法中，比如GET和POST，而不是类函数中的条件判断。
- 可以使用面向对象的技巧，比如混入。
- 类具有封装和继承的特性，方便代码复用、分发和重构。

两种视图可以实现同样的功能，本质上是一个东西，没有谁好谁坏之分，只是适用场景不同而已：

- 简单逻辑、快速处理，请用FBV
- 代码复用、功能封装，请用CBV

Django 提供了很多适用于各种应用场景的基本视图类，我们一般不从头自己写起，这些类视图都继承`django.views.generic.base.View`类。比如`RedirectView` 用于 HTTP 重定向，`TemplateView` 用于渲染模板。

类视图有很多简单的用法，甚至不需要去views.py中编写代码，比如下面的例子：

```python
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('about/', TemplateView.as_view(template_name="about.html")),
]
```

重点关注：

- `TemplateView`类视图
- `as_view()`方法
- `template_name`参数

更通用的使用方法是继承Django提供的各种视图类，所以上面的例子的一般性写法如下：

```python
# some_app/views.py
from django.views.generic import TemplateView

class AboutView(TemplateView):
    template_name = "about.html"
```

但是，由于类不是函数，所以需要在URLconf中使用`as_view()`这个类方法将一个基于类的视图转换成函数形式的接口。

```python
# urls.py
from django.urls import path
from some_app.views import AboutView

urlpatterns = [
    path('about/', AboutView.as_view()),
]
```

上面的AboutView视图不涉及模型的访问，比较简单。让我们看一个书籍列表视图的例子：

首先是路由：

```python
from django.urls import path
from books.views import BookListView

urlpatterns = [
    path('books/', BookListView.as_view()),
]
```

`BookListView`视图：

```python
from django.http import HttpResponse
from django.views.generic import ListView
from books.models import Book

class BookListView(ListView):
    model = Book  # 指定模型

    def head(self, request, *args, **kwargs):
        last_book = self.get_queryset().latest('publication_date')
        response = HttpResponse()
        # RFC 1123 date format
        response['Last-Modified'] = last_book.publication_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
        return response
```

这个例子中，如果用户通过GET请求数据，那么将正常的返回响应数据（此处省略）。而如果通过HEAD请求，将使用我们写的head方法中的业务逻辑。

## 一、使用基于类的视图

本质上来说，基于类的视图允许你使用不同的实例方法响应不同的HTTP 请求，而不是在单个视图函数里使用`if/else`代码。

在函数视图里处理 `GET`请求的代码像下面这样：

```python
from django.http import HttpResponse

def my_view(request):
    if request.method == 'GET':
        # <view logic>
        return HttpResponse('result')
```

而在类视图中，则通过不同过的实例方法来处理：

```python
rom django.http import HttpResponse
from django.views import View

class MyView(View):
    def get(self, request):
        # <view logic>
        return HttpResponse('result')
```

上面的继承关系非常重要，不能从头写一个新类，或者随便自己瞎继承一个类，否则你无法和Django系统勾连。

每个类视图都有一个`as_view()`方法，用于在`urlconf`中进行dispatch。这个方法会创建一个类视图的实例，并调用它的`dispatch()`方法。dispatch方法会在类中查找类似GET\POST之类的类方法，然后与请求request中的HTTP方法匹配。匹配上了就调用对应的代码，匹配不上就弹出异常`HttpResponseNotAllowed`，也就是不允许当前的请求类型。

```python
# urls.py
from django.urls import path
from myapp.views import MyView

urlpatterns = [
    path('about/', MyView.as_view()),    # 注意as_view要加括号进行调用
]
```

至于return返回的什么，和函数视图是一样样的。

> `as_view()`方法可以传递参数，例如：
>
> ```python
> urlpatterns = [ path('view/', MyView.as_view(size=42)), ]
> ```
>
> 传递给视图的参数会在视图的每个实例之间共享。这意味着你不应使用列表、字典或任何其他可变对象作为视图的参数。如果你这样做并且共享对象被修改，则会导致一个请求对另外一个请求产生影响，这显然存在极大的风险，完全不可接受。
>
> 每个MyView视图的实例都可以使用 `self.size`接收传入的参数值42，但该参数必须已经在类中定义了。

基于类的视图不强制你添加任何类属性，当需要的时候，有两种方法来配置或设置类属性。

第一种是继承父类，在子类中重写父类的属性，如下所示：

父类：

```python
from django.http import HttpResponse
from django.views import View

class GreetingView(View):
    greeting = "Good Day"

    def get(self, request):
        return HttpResponse(self.greeting)
```

子类：

```python
class MorningGreetingView(GreetingView):
    greeting = "Morning to ya"
```

注意其中的greeting类属性。

另一种就是简单粗暴的在URLconf路由条目中修改as_view()方法的参数。当然，参数名必须是存在的类属性，你不能随便瞎写！如下所示：

```python
urlpatterns = [
    path('about/', GreetingView.as_view(greeting="G'day")),
]
```

但是这种方式有很大的弊端，那就是虽然每次匹配上了url，你的类视图都会被实例化一次，但是你的URLs却是在被导入的时候才配置一次，也就是as_view()方法的参数的配置只有一次。也就是说这么做，就不能再改了！所以，不要偷懒，使用子类吧。

## 二、使用mixin混入

混入是一种多父类继承的形式，其基础理论知识请参考我的Python教程中多继承相关章节。

在编写子类的时候，一个父类负责类的主体结构、主要行为和主要属性，其它的功能都通过各种MIXin父类提供。

MIXIN是跨多个类重用代码的一个很好的方法，但是它们会带来一些代价。你的代码散布在MIXIN中越多，阅读子类就越难，很难知道它到底在做什么。如果你在对具有多级继承树的子类进行分类，就更难以判断子类的方法到底继承的是哪个先祖，俗称‘家谱乱了’。

**需要注意的是你的父类中只有一个类可以继承最顶级的View类，其它的必须以mixin方法混入。**

## 三、使用类视图处理表单

一个用来处理表单的函数视图通常是下面这样的：

```python
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import MyForm

def myview(request):
    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect('/success/')
    else:
        form = MyForm(initial={'key': 'value'})

    return render(request, 'form_template.html', {'form': form})
```

而如果用类视图来实现，是这样的：

```python
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from .forms import MyForm

class MyFormView(View):
    form_class = MyForm
    initial = {'key': 'value'}
    template_name = 'form_template.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect('/success/')

        return render(request, self.template_name, {'form': form})
```

看起来类视图好像比函数视图代码多了很多，复杂了很多，貌似没啥优点啊。但是如果你有多个类似的视图需要编写，那么你就可以发挥子类的继承和复写神操作了，分分钟整出个新的视图来。或者直接在URLConf中修改参数！或者两种操作同时使用！

其实，到现在你应该理解，**类视图适用于大量重复性的视图编写工作**，在简单的场景下，没几个视图需要编写，或者各个视图差别很大的情况时，还是函数视图更有效！所以，**不要认为类视图是多么高大上的东西**，人云亦云！

## 四、装饰类视图

除了mixin，还可以使用装饰器扩展类视图。装饰器的工作方式取决于你是在创建子类还是使用as_view()。

用法一，在URLConf中直接装饰：

```python
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView

from .views import VoteView

urlpatterns = [
    path('about/', login_required(TemplateView.as_view(template_name="secret.html"))),
    path('vote/', permission_required('polls.can_vote')(VoteView.as_view())),
]
```

用法二，在类视图中装饰指定的方法：

```python
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

class ProtectedView(TemplateView):
    template_name = 'secret.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
```

注意：

- 上面要把装饰器用在dispatch这个方法上，才能在每次请求到达URL时，实例化类视图时都运行这个装饰器的功能。
- 不是每个装饰器都能直接运用在类方法上，需要使用`method_decorator`这个装饰器的装饰器方法将装饰器运用在类方法上。感觉很绕？其实就是说，我们有很多很多的装饰器，但其中有一些不能直接装饰dispatch这种类方法。那怎么办呢？套层壳！用`method_decorator`装饰器包裹起来，假装成一个能用的。

有时候，简单地用一下，可以写成下面的精简版：

```python
@method_decorator(login_required, name='dispatch')
class ProtectedView(TemplateView):
    template_name = 'secret.html'
```

有时候，可能你需要对一个对象应用多个装饰器，正常做法是：

```python
@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class ProtectedView(TemplateView):
    template_name = 'secret.html'
```

为了偷懒，我们可以这么做：

```python
decorators = [never_cache, login_required]

@method_decorator(decorators, name='dispatch')
class ProtectedView(TemplateView):
    template_name = 'secret.html'
```

唯一需要注意地是**装饰器是有先后顺序的**。上面的例子中，`never_cache`就要先于`login_required`被调用。

最后，使用`method_decorator`有时会导致`TypeError`异常，因为参数传递的原因。

# 中间件

------

中间件是 Django 用来处理请求和响应的钩子框架。它是一个轻量级的、底层级的“插件”系统，用于全局性地控制Django 的输入或输出，可以理解为一些关卡。

在`django.core.handlers.base`模块中定义了如何接入中间件，这也是学习Django源码的入口之一。

每个中间件组件负责实现一些特定的功能。例如，Django 包含一个中间件组件 `AuthenticationMiddleware`，它使用会话机制将用户与请求request关联起来。

中间件可以放在你的工程的任何地方，并以Python路径的方式进行访问。

Django 具有一些内置的中间件，并自动开启了其中的一部分，我们可以根据自己的需要进行调整。

## 一、如何启用中间件

若要启用中间件组件，请将其添加到 Django 配置文件`settings.py`的 `MIDDLEWARE` 配置项列表中。

在 `MIDDLEWARE` 中，中间件由字符串表示。这个字符串以圆点分隔，指向中间件工厂的类或函数名的完整 Python 路径。下面是使用 `django-admin startproject`命令创建工程后，默认的中间件配置：

```
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

实际上在Django中可以不使用任何中间件，如果你愿意的话，`MIDDLEWARE` 配置项可以为空。但是强烈建议至少使用 `CommonMiddleware`，最好是保持默认的配置，这有助于你提高网站的安全性。

## 二、 中间件最关键的顺序问题

这么多`MIDDLEWARE` 放在一个列表中，它们之间的顺序很重要，具有先后关系，因为有些中间件会依赖其他中间件。例如： `AuthenticationMiddleware` 需要在会话中间件中存储的经过身份验证的用户信息，因此它必须在 `SessionMiddleware` 后面运行 。

**在请求阶段，调用视图之前，Django 按照定义的顺序执行中间件 `MIDDLEWARE`，自顶向下。**

你可以把它想象成一个`洋葱`：每个中间件类都是一个“皮层”，它包裹起了洋葱的核心--`实际业务视图`。如果请求通过了洋葱的所有`中间件`层，一直到内核的视图，那么**响应将在返回的过程中以相反的顺序再通过每个中间件层，最终返回给用户**。

**如果某个层的执行过程认为当前的请求应该被拒绝，或者发生了某些错误，导致短路，直接返回了一个响应，那么剩下的中间件以及核心的视图函数都不会被执行。**

## 三、Django内置的中间件

Django内置了很多中间件，满足了我们一般的需求，下面介绍一些常用的：

### Cache

缓存中间件

如果启用了该中间件，Django会以`CACHE_MIDDLEWARE_SECONDS` 配置的参数进行全站级别的缓存。

### Common

通用中间件

该中间件为我们提供了一些便利的功能：

- 禁止`DISALLOWED_USER_AGENTS`中的用户代理访问服务器
- 自动为URL添加斜杠后缀和`www`前缀功能。如果配置项 `APPEND_SLASH` 为`True` ，并且访问的URL 没有斜杠后缀，在URLconf中没有匹配成功，将自动添加斜杠，然后再次匹配，如果匹配成功，就跳转到对应的url。 `PREPEND_WWW` 的功能类似，为url添加`www.`前缀。
- 为非流式响应设置`Content-Length`头部信息。

作为展示的例子，这里额外贴出它的源代码，它位于`django.middleware.common`模块中，比较简单，很容易读懂和理解：

```
class CommonMiddleware(MiddlewareMixin):
    """
    去掉了doc
    """
    response_redirect_class = HttpResponsePermanentRedirect

    def process_request(self, request):
        # Check for denied User-Agents
        if 'HTTP_USER_AGENT' in request.META:
            for user_agent_regex in settings.DISALLOWED_USER_AGENTS:
                if user_agent_regex.search(request.META['HTTP_USER_AGENT']):
                    raise PermissionDenied('Forbidden user agent')

        # Check for a redirect based on settings.PREPEND_WWW
        host = request.get_host()
        must_prepend = settings.PREPEND_WWW and host and not host.startswith('www.')
        redirect_url = ('%s://www.%s' % (request.scheme, host)) if must_prepend else ''

        # Check if a slash should be appended
        if self.should_redirect_with_slash(request):
            path = self.get_full_path_with_slash(request)
        else:
            path = request.get_full_path()

        # Return a redirect if necessary
        if redirect_url or path != request.get_full_path():
            redirect_url += path
            return self.response_redirect_class(redirect_url)

    def should_redirect_with_slash(self, request):

        if settings.APPEND_SLASH and not request.path_info.endswith('/'):
            urlconf = getattr(request, 'urlconf', None)
            return (
                not is_valid_path(request.path_info, urlconf) and
                is_valid_path('%s/' % request.path_info, urlconf)
            )
        return False

    def get_full_path_with_slash(self, request):

        new_path = request.get_full_path(force_append_slash=True)
        if settings.DEBUG and request.method in ('POST', 'PUT', 'PATCH'):
            raise RuntimeError(
                "You called this URL via %(method)s, but the URL doesn't end "
                "in a slash and you have APPEND_SLASH set. Django can't "
                "redirect to the slash URL while maintaining %(method)s data. "
                "Change your form to point to %(url)s (note the trailing "
                "slash), or set APPEND_SLASH=False in your Django settings." % {
                    'method': request.method,
                    'url': request.get_host() + new_path,
                }
            )
        return new_path

    def process_response(self, request, response):
        # If the given URL is "Not Found", then check if we should redirect to
        # a path with a slash appended.
        if response.status_code == 404:
            if self.should_redirect_with_slash(request):
                return self.response_redirect_class(self.get_full_path_with_slash(request))

        if settings.USE_ETAGS and self.needs_etag(response):
            warnings.warn(
                "The USE_ETAGS setting is deprecated in favor of "
                "ConditionalGetMiddleware which sets the ETag regardless of "
                "the setting. CommonMiddleware won't do ETag processing in "
                "Django 2.1.",
                RemovedInDjango21Warning
            )
            if not response.has_header('ETag'):
                set_response_etag(response)

            if response.has_header('ETag'):
                return get_conditional_response(
                    request,
                    etag=response['ETag'],
                    response=response,
                )
        # Add the Content-Length header to non-streaming responses if not
        # already set.
        if not response.streaming and not response.has_header('Content-Length'):
            response['Content-Length'] = str(len(response.content))

        return response

    def needs_etag(self, response):
        """Return True if an ETag header should be added to response."""
        cache_control_headers = cc_delim_re.split(response.get('Cache-Control', ''))
        return all(header.lower() != 'no-store' for header in cache_control_headers)
```

### GZip

内容压缩中间件

用于减小响应数据的体积，降低带宽压力，提高传输速度。

该中间件必须位于其它所有需要读写响应体内容的中间件之前，此时数据还未被压缩。

如果存在下面情况之一，将不会压缩响应内容：

- 内容少于200 bytes
- 已经设置了 `Content-Encoding` 头部属性
- 请求的 `Accept-Encoding` 头部属性未包含 `gzip`.

可以使用 `gzip_page()`装饰器，为视图单独开启GZip压缩服务。

### Conditional GET

有条件的GET访问中间件，很少使用。

### Locale

本地化中间件

用于处理国际化和本地化，语言翻译。

### Message

消息中间件

基于cookie或者会话的消息功能，比较常用。

### Security

安全中间件

`django.middleware.security.SecurityMiddleware`中间件为我们提供了一系列的网站安全保护功能。主要包括下列所示，可以单独开启或关闭：

- `SECURE_BROWSER_XSS_FILTER`
- `SECURE_CONTENT_TYPE_NOSNIFF`
- `SECURE_HSTS_INCLUDE_SUBDOMAINS`
- `SECURE_HSTS_PRELOAD`
- `SECURE_HSTS_SECONDS`
- `SECURE_REDIRECT_EXEMPT`
- `SECURE_SSL_HOST`
- `SECURE_SSL_REDIRECT`

### Session

会话中间件，非常常用。

### Site

站点框架。

这是一个很有用，但又被忽视的功能。

它可以让你的Django具备多站点支持的功能。

通过增加一个`site`属性，区分当前request请求访问的对应站点。

无需多个IP或域名，无需开启多个服务器，只需要一个site属性，就能搞定多站点服务。

### Authentication

认证框架

Django最主要的中间件之一，提供用户认证服务。后面会有章节详细介绍。

### CSRF protection

提供CSRF防御机制的中间件

### `X-Frame-Options`

点击劫持防御中间件

### 建议的排列顺序

对于Django内置的中间件，有一个建议的排列顺序，按列表下标由小到大：

1. SecurityMiddleware
2. UpdateCacheMiddleware
3. GZipMiddleware
4. SessionMiddleware
5. ConditionalGetMiddleware
6. LocaleMiddleware
7. CommonMiddleware
8. CsrfViewMiddleware
9. AuthenticationMiddleware
10. MessageMiddleware
11. FetchFromCacheMiddleware
12. FlatpageFallbackMiddleware
13. RedirectFallbackMiddleware

## 四、异步支持

从Django3.1开始，支持异步的中间件，以及同步和异步请求的任意组合。如果Django不能同时支持它们，会调整请求来适应中间件的需求，但会有性能损失。

默认情况下，Django假设你的中间件只能处理同步请求。如果要改变这种模式，需要在你的中间件工厂函数或类中添加入如下属性：

- `sync_capable` ：一个布尔值，来表明中间件是否处理同步请求。默认为 `True`。
- `async_capable` ：一个布尔值，来表明中间件是否处理异步请求。默认为 `False`。

`django.utils.decorators` 模块中包含 `sync_only_middleware()`, `async_only_middleware()`和 `sync_and_async_middleware()` 三个装饰器，可以将它们用于中间件工厂函数上，分别代表仅支持同步、仅支持异步和同时支持同步异步三种模式，以实现和上面两个属性相同的作用。

如果你的中间件同时设置了`sync_capable = True` 和`async_capable = True`，Django回直接传递请求而不做任何转换动作。在这种情况下，可以使用`asyncio.iscoroutinefunction()`方法检查你传递给 `get_response` 的参数是否是一个协程函数，从而确定你的中间件是否支持异步请求。

`process_view`，`process_template_response`以及`process_exception` 方法，也应自动适配同步/异步模式。但是如果您不这样做，Django会根据需要单独调整它们，这会带来额外的性能损失。

下面是一个示例，说明如何创建同时支持两者的中间件：

```
import asyncio
from django.utils.decorators import sync_and_async_middleware

@sync_and_async_middleware
def simple_middleware(get_response):
    # One-time configuration and initialization goes here.
    if asyncio.iscoroutinefunction(get_response):
        async def middleware(request):
            # Do something here!
            response = await get_response(request)
            return response

    else:
        def middleware(request):
            # Do something here!
            response = get_response(request)
            return response

    return middleware
```

## 五、自定义中间件

有时候，为了实现一些特定的需求，我们可能需要编写自己的中间件。

**需要注意的是，存在两种编写的方式。一种是Django当前官网上提供的例子，一种是老版本的方式。**本质上，两种方式其实是一样的。

我们先看一下传统的，也是技术文章最多，目前使用最多的方式。

### 传统的方法

#### 五大钩子函数

传统方式自定义中间件其实就是在编写五大钩子函数：

- process_request(self,request)
- process_response(self, request, response)
- process_view(self, request, view_func, view_args, view_kwargs)
- process_exception(self, request, exception)
- process_template_response(self,request,response)

可以实现其中的任意一个或多个！

| 钩子函数                  | 执行时机                                          | 执行顺序       | 返回值                     |
| ------------------------- | ------------------------------------------------- | -------------- | -------------------------- |
| process_request           | 请求刚到来，执行视图之前                          | 配置列表的正序 | None或者HttpResponse对象   |
| process_response          | 视图执行完毕，返回响应时                          | 逆序           | HttpResponse对象           |
| process_view              | process_request之后，路由转发到视图，执行视图之前 | 正序           | None或者HttpResponse对象   |
| process_exception         | 视图执行中发生异常时                              | 逆序           | None或者HttpResponse对象   |
| process_template_response | 视图刚执行完毕，process_response之前              | 逆序           | 实现了render方法的响应对象 |

##### `process_request()`

签名：`process_request(request)`

最主要的钩子之一！

只有一个参数，也就是request请求内容，和视图函数中的request是一样的。所有的中间件都是同样的request，不会发生变化。它的返回值可以是None也可以是HttpResponse对象。返回None的话，表示一切正常，继续走流程，交给下一个中间件处理。返回HttpResponse对象，则发生短路，不继续执行后面的中间件，也不执行视图函数，而将响应内容返回给浏览器。

##### `process_response()`

签名：`process_response(request, response)`

最主要的钩子之一！

有两个参数，request和response。request是请求内容，response是视图函数返回的HttpResponse对象。该方法的返回值必须是一个HttpResponse对象，不能是None。

process_response()方法在视图函数执行完毕之后执行，并且按配置顺序的逆序执行。

##### `process_view()`

签名：`process_view(request, view_func, view_args, view_kwargs)`

- `request` ： `HttpRequest` 对象。
- `view_func` ：真正的业务逻辑视图函数（不是函数的字符串名称）。
- `view_args` ：位置参数列表
- `view_kwargs` ：关键字参数字典

请务必牢记：**`process_view()` 在Django调用真正的业务视图之前被执行，并且以正序执行**。当process_request()正常执行完毕后，会进入urlconf路由阶段，并查找对应的视图，在执行视图函数之前，会先执行`process_view()` 中间件钩子。

这个方法必须返回`None` 或者一个 `HttpResponse` 对象。如果返回的是None，Django将继续处理当前请求，执行其它的 `process_view()` 中间件钩子，最后执行对应的视图。如果返回的是一个 `HttpResponse` 对象，Django不会调用业务视图，而是执行响应中间件，并返回结果。

##### `process_exception()`

签名：`process_exception(request, exception)`

- `request`：`HttpRequest`对象
- `exception`：视图函数引发的具体异常对象

当一个视图在执行过程中引发了异常，Django将自动调用中间件的 `process_exception()`方法。 `process_exception()` 要么返回一个 `None` ，要么返回一个 `HttpResponse` 对象。如果返回的是`HttpResponse`对象 ，模板响应和响应中间件将被调用 ，否则进行正常的异常处理流程。

同样的，此时也是以逆序的方式调用每个中间件的 `process_exception`方法，以短路的机制。

##### `process_template_response()`

签名：`process_template_response(request, response)`

`request`：`HttpRequest` 对象

`response` ： `TemplateResponse` 对象

`process_template_response()` 方法在业务视图执行完毕后调用。

正常情况下一个视图执行完毕，会渲染一个模板，作为响应返回给用户。使用这个钩子方法，你可以重新处理渲染模板的过程，添加你需要的业务逻辑。

对于 `process_template_response()`方法，也是采用逆序的方式进行执行的。

#### 钩子方法执行流程

（注：所有图片来自网络，侵删！）

一个理想状态下的中间件执行过程，可能只有`process_request()`和`process_response()`方法，其流程如下：

![img](images/1762677-20201005204227719-1604868022.png)

**一旦任何一个中间件返回了一个HttpResponse对象，立刻进入响应流程！要注意，未被执行的中间件，其响应钩子方法也不会被执行，这是一个短路，或者说剥洋葱的过程。**

如果有`process_view`方法的介入，那么会变成下面的样子：

![img](images/1762677-20201005204234510-23279000.png)

总的执行流程和机制如下图所示：

![img](images/1762677-20201005204240689-117614881.png)

仔细研究一下下面的执行流程，能够加深你对中间件的理解。

![img](images/1762677-20201005204245675-1051882159.png)

#### 实例演示

介绍完了理论，下面通过实际的例子来演示一下。

要注意，之所以被称为传统的方法，是因为这里要导入一个将来会被废弃的父类，也就是：

```
from django.utils.deprecation import MiddlewareMixin
```

`deprecation`是废弃、贬低、折旧、反对的意思，也就是说，这个`MiddlewareMixin`类将来应该会被删除！

我们看一下`MiddlewareMixin`的源码：

```
class MiddlewareMixin:
    def __init__(self, get_response=None):
        self.get_response = get_response
        super().__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response
```

这个类并没有自己定义五大钩子方法，而是定义了`__call__`方法，通过`hasattr`的反射，寻找`process_request`等钩子函数是否存在，如果存在就执行。它的本质和后面要介绍的Django官网提供的例子，也就是新的写法是一样的！

现在，假设我们有一个app叫做midware，在其中创建一个middleware.py模块，写入下面的代码：

```
from django.utils.deprecation import MiddlewareMixin


class Md1(MiddlewareMixin):

    def process_request(self,request):
        print("Md1处理请求")

    def process_response(self,request,response):
        print("Md1返回响应")
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):

        print("Md1在执行%s视图前" %view_func.__name__)

    def process_exception(self,request,exception):
        print("Md1处理视图异常...")



class Md2(MiddlewareMixin):

    def process_request(self,request):
        print("Md2处理请求")

    def process_response(self,request,response):
        print("Md2返回响应")
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):

        print("Md2在执行%s视图前" %view_func.__name__)

    def process_exception(self,request,exception):
        print("Md2处理视图异常...")
```

然后，我们就可以在setting.py中配置这两个自定义的中间件了：

```
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'midware.middleware.Md1',
    'midware.middleware.Md2',
]
```

在midware/views.py中创建一个简单的视图：

```
from django.shortcuts import render, HttpResponse


def mid_test(request):
    print('执行视图mid_test')
    # raise
    return HttpResponse('200,ok')
```

其中的raise可以用来测试`process_exception()`钩子。

编写一条urlconf，用来测试视图，比如：

```
from midware import views as mid_views

urlpatterns = [
    path('midtest/', mid_views.mid_test),
]
```

重启服务器，访问`...../midtest/`，可以在控制台看到如下的信息：

```
Md1处理请求
Md2处理请求
Md1在执行mid_test视图前
Md2在执行mid_test视图前
执行视图mid_test
Md2返回响应
Md1返回响应
```

如果打开视图中的raise语句，模拟异常状态，执行后的信息如下：

```
Md1处理请求
Md2处理请求
Md1在执行mid_test视图前
Md2在执行mid_test视图前
执行视图mid_test
Md2处理视图异常...
Md1处理视图异常...
Md2返回响应
Md1返回响应
```

在理解中间件什么时候会起作用的时候要记住一句话：凡是穿透过的中间件，响应的时候依然会穿回。如果后面的中间件还没有参与到请求的过程中，就返回响应了，那么就等于不存在。

### Django官方方法

在Django的官方文档中，我们可以看到一种完全不同的编写方式。

**这种编写方式省去了`process_request()`和`process_response()`方法的编写，将它们直接集成在一起了。**

**这种方式是官方推荐的方式！**

中间件本质上是一个可调用的对象（函数、方法、类），它接受一个请求（request），并返回一个响应（response）或者None，就像视图一样。其初始化参数是一个名为`get_response`的可调用对象。

中间件可以被写成下面这样的函数（下面的语法，本质上是一个Python装饰器，不推荐这种写法）：

```
def simple_middleware(get_response):
    # 配置和初始化

    def middleware(request):

        # 在这里编写具体业务视图和随后的中间件被调用之前需要执行的代码

        response = get_response(request)

        # 在这里编写视图调用后需要执行的代码

        return response

    return middleware
```

或者写成一个类（真.推荐形式），这个类的实例是可调用的，如下所示：

```
class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
         # 配置和初始化

    def __call__(self, request):

        # 在这里编写视图和后面的中间件被调用之前需要执行的代码
        # 这里其实就是旧的process_request()方法的代码

        response = self.get_response(request)

        # 在这里编写视图调用后需要执行的代码
        # 这里其实就是旧的process_response()方法的代码

        return response
```

（是不是感觉和前面的`MiddlewareMixin`类很像？）

Django 提供的 `get_response` 方法可能是一个实际视图（如果当前中间件是最后列出的中间件），或者是列表中的下一个中间件。我们不需要知道或关心它到底是什么，它只是代表了下一步要进行的操作。

两个注意事项：

- Django仅使用 `get_response` 参数初始化中间件，因此不能为 `__init__()` 添加其他参数。
- 与每次请求都会调用 `__call__()` 方法不同，当 Web 服务器启动后，`__init__()` 只被调用*一次*。

#### 实例演示

我们只需要把前面的Md1和Md2两个中间件类修改成下面的代码就可以了：

```
class Md1:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        print("Md1处理请求")

        response = self.get_response(request)

        print("Md1返回响应")

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):

        print("Md1在执行%s视图前" %view_func.__name__)

    def process_exception(self,request,exception):
        print("Md1处理视图异常...")


class Md2:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("Md2处理请求")

        response = self.get_response(request)

        print("Md2返回响应")

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        print("Md2在执行%s视图前" % view_func.__name__)

    def process_exception(self, request, exception):
        print("Md2处理视图异常...")
```

可以看到，我们不再需要继承`MiddlewareMixin`类。

实际执行结果是一样的。

## 应用实例一：IP拦截

如果我们想限制某些IP对服务器的访问，可以在settings.py中添加一个BLACKLIST（全大写）列表，将被限制的IP地址写入其中。

然后，我们就可以编写下面的中间件了：

```
from django.http import HttpResponseForbidden
from django.conf import settings

class BlackListMiddleware():

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.META['REMOTE_ADDR'] in getattr(settings, "BLACKLIST", []):
            return HttpResponseForbidden('<h1>该IP地址被限制访问！</h1>')

        response = self.get_response(request)

        return response
```

具体的中间件注册、视图、url就不再赘述了。

## 应用实例二：DEBUG页面

**网站上线正式运行后，我们会将DEBUG改为 False，这样更安全。但是发生服务器5xx系列错误时，管理员却不能看到错误详情，调试很不方便。有没有办法比较方便地解决这个问题呢？**

- 普通访问者看到的是500错误页面
- 管理员看到的是错误详情Debug页面

利用中间件就可以做到！代码如下：

```
import sys
from django.views.debug import technical_500_response
from django.conf import settings


class DebugMiddleware():

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        return response

    def process_exception(self, request, exception):
        # 如果是管理员，则返回一个特殊的响应对象，也就是Debug页面
        # 如果是普通用户，则返回None，交给默认的流程处理
        if request.user.is_superuser or request.META.get('REMOTE_ADDR') in settings.ADMIN_IP:
            return technical_500_response(request, *sys.exc_info())
```

这里通过if判断，当前登录的用户是否超级管理员，或者当前用户的IP地址是否在管理员IP地址列表中。符合两者之一，即判断当前用户有权限查看Debug页面。

接下来注册中间件，然后在测试视图中添加一行raise。再修改settings.py，将Debug设为False，提供`ALLOWED_HOSTS = ["*"]`，设置比如`ADMIN_IP = ['192.168.0.100']`，然后启动服务器`0.0.0.0:8000`，从不同的局域网IP来测试这个中间件。

正常情况下，管理员应该看到类似下面的Debug页面：

```
RuntimeError at /midtest/
No active exception to reraise
Request Method: GET
Request URL:    http://192.168.0.100:8000/midtest/
Django Version: 2.0.7
Exception Type: RuntimeError
Exception Value:    
No active exception to reraise
.....
```

而普通用户只能看到：

```
A server error occurred.  Please contact the administrator.
```