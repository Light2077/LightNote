第一个django应用

https://www.liujiangblog.com/course/django/88

## part1：请求与响应

- 启动服务器

- 创建应用 `python manage.py startapp <app name>`

- 编写视图`polls/views.py`

  ```python
  from django.http import HttpResponse
  
  def index(request):
      return HttpResponse("这里是liujiangblog.com的投票站点")
  ```

  - 还需要编写`urlconf`（路由配置）`polls/urls.py`

  - ```python
    from django.urls import path
    
    from . import views
    
    urlpatterns = [
        path('', views.index, name='index'),
    ]
    ```

  - 在主`urls.py`文件添加`urlpattern`条目

  - ```python
    rom django.contrib import admin
    from django.urls import include, path
    
    urlpatterns = [
        path('polls/', include('polls.urls')),
        path('admin/', admin.site.urls),
    ]
    ```

  - 访问`http://localhost:8000/polls/` 注：没有polls的话会报错





### `django.urls.path()`方法介绍

用来安排路径

```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]

```

`path(route, view, kwargs, name)`

- `route`：匹配url的准则，使用的是短路机制，比如上面这里就是只匹配`polls/`如果后面有`polls/?page=3`也是不会匹配的
- `view`：寻找当前url请求的视图函数
- `kwargs`：我猜是把请求发过来的一些参数传给目标视图
- `name`：对url进行命名，相当于全局变量名

## Part2：模型与后台

### 一、数据库配置

- 在`mysite/settings.py`文件里查看数据库配置

- ```python
  # https://docs.djangoproject.com/en/3.1/ref/settings/#databases
  
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': BASE_DIR / 'db.sqlite3',
      }
  }
  ```

- ENGINE（引擎）：

  - `django.db.backends.sqlite3`
  - `django.db.backends.mysql`
  - `django.db.backends.oracle`
  - `django.db.backends.postgresql`

- 使用非SQLite3数据库时有一些**注意事项**

- 创建数据库表（数据库迁移？）`python manage.py migrate`

### 二、创建模型

实质上就是python的类，这个类就对应数据的表

类中的属性对应表的列

- 修改`polls/models.py`

### 三、启用模型

- 把应用添加到`mysite/settings.py`内

  ```python
  # mysite/settings.py
  
  INSTALLED_APPS = [
  'polls',
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  ]
  ```

- 创建数据库迁移命令`python manage.py makemigrations polls`，这步执行以后并没有修改数据库，可以使用`python manage.py sqlmigrate polls 0001`查看迁移的时候实际执行的SQL语句

- 实行数据库迁移`python manage.py migrate`

右键项目下的`db.sqlite3`文件，选`open SQLite database`文件可以查看数据库的信息，里面有增加了新表

### 四、体验模型自带的API

- 修改`polls/models.py`使得之后在查看表中数据时更加清晰

  ```python
  class Question(models.Model):
  
      ...
      
      def __str__(self):
          return self.question_text
  
  
  class Choice(models.Model):
      
      ...
  
      def __str__(self):
          return self.choice_text
  ```

- 定义模型的方法

  ```python
  # polls/models.py
  
  import datetime
  
  from django.db import models
  from django.utils import timezone
  
  
  class Question(models.Model):
      # 是否在当前发布的问卷
      def was_published_recently(self):
          return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
  ```

  

- `python manage.py shell`启动django提供的数据库访问API

### 五、admin后台管理站点

- 创建管理员用户，输入用户名，邮箱，密码

  ```shell
  python manage.py createsuperuser
  ```

- 启动开发服务器，runserver后在浏览器访问`http://127.0.0.1:8000/admin/

  可以在`mysite/urls.py`中，修改admin的路径

  ```python
  urlpatterns = [
      path('polls/', include('polls.urls')),
      path('admin/', admin.site.urls),
      # path('control/', admin.site.urls),
  ]
  ```

- 输入账户密码进入界面

- 注册投票应用`polls/admin.py`

  ```python
  from django.contrib import admin
  from .models import Question
  
  admin.site.register(Question)
  ```

  注册完毕后刷新页面即可。点击对象可以查看相关属性

## part3：视图和模板

视图应该是功能函数，模板是页面该怎么显示

`Django`使用`URLconfs`来配置路由



### 二、编写视图

- 打开`polls/views.py`输入

  ```python
  # 注意函数的参数
  def detail(request, question_id):
      return HttpResponse("You're looking at question %s." % question_id)
  
  def results(request, question_id):
      response = "You're looking at the results of question %s."
      return HttpResponse(response % question_id)
  
  def vote(request, question_id):
      return HttpResponse("You're voting on question %s." % question_id)
  ```

- 在`polls/urls.py`文件中加入下面的路由

  ```python
  from django.urls import path
  
  from . import views
  
  urlpatterns = [
      # 例如: /polls/
      path('', views.index, name='index'),
  
      # 例如: /polls/5/
      path('<int:question_id>/', views.detail, name='detail'),
  
      # 例如: /polls/5/results/
      path('<int:question_id>/results/', views.results, name='results'),
  
      # 例如: /polls/5/vote/
      path('<int:question_id>/vote/', views.vote, name='vote'),
  ]
  ```

- 访问 http://127.0.0.1:8000/polls/34/ 查看结果。

  http://127.0.0.1:8000/polls/34/results/

  http://127.0.0.1:8000/polls/34/vote/

- 注意这个写法

  ```python
  path('<int:question_id>/results/', views.results, name='results')
  ```

  实际上就把`<int:question_id>`作为参数，传入了`views.results`函数内了。

### 三、编写能实际干点活的视图

视图必做的两件事，返回请求页面的HttpResponse对象

弹出，Http404异常

- 创建新的index视图

  ```python
  from django.http import HttpResponse
  
  from .models import Question
  
  
  def index(request):
      latest_question_list = Question.objects.order_by('-pub_date')[:5]
      output = ', '.join([q.question_text for q in latest_question_list])
      return HttpResponse(output)
  
  # 省略了那些没改动过的视图(detail, results, vote)
  ```

  重要问题：当前视图中HTML页面是硬编码的(?，应该指的就是返回的不是html页面，而是字符串)。需要创建模板文件

- 在polls目录下创建templates目录，观察`mysite/settings.py`中有关`TEMPLATES`的配置项

  ```python
  TEMPLATES = [
      {
          'BACKEND': 'django.template.backends.django.DjangoTemplates',
          'DIRS': [],
          'APP_DIRS': True,
          'OPTIONS': {
              'context_processors': [
                  'django.template.context_processors.debug',
                  'django.template.context_processors.request',
                  'django.contrib.auth.context_processors.auth',
                  'django.contrib.messages.context_processors.messages',
              ],
          },
      },
  ]
  ```

  

- 在`polls/templates/`目录下创建`polls`目录，在这个目录下创建`index.html`文件

  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <title>index</title>
  </head>
  <body>
  
  {% if latest_question_list %}
      <ul>
      {% for question in latest_question_list %}
          <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
      {% endfor %}
      </ul>
  {% else %}
      <p>No polls are available.</p>
  {% endif %}
  
  </body>
  </html>
  ```

- 修改视图文件`polls/views.py`

  ```python
  from django.http import HttpResponse
  from django.template import loader
  
  from .models import Question
  
  
  def index(request):
      latest_question_list = Question.objects.order_by('-pub_date')[:5]
      template = loader.get_template('polls/index.html')
      context = {
          'latest_question_list': latest_question_list,
      }
      return HttpResponse(template.render(context, request))
  ```

  了解index函数做了什么：

  - 从数据库取出前5条数据
  - 载入html文件
  - 以字典的形式设定好html文件的内容
  - 返回并渲染模板文件

- 更加简洁的render函数

  ```python
  from django.shortcuts import render
  
  from .models import Question
  
  
  def index(request):
      latest_question_list = Question.objects.order_by('-pub_date')[:5]
      context = {'latest_question_list': latest_question_list}
      return render(request, 'polls/index.html', context)
  ```

### 四、返回404错误

- 修改`polls/views.py`

  ```python
  # polls/views.py
  
  from django.http import Http404
  from django.shortcuts import render
  
  from .models import Question
  # ...
  def detail(request, question_id):
      try:
          question = Question.objects.get(pk=question_id)
      except Question.DoesNotExist:
          raise Http404("Question does not exist")
      return render(request, 'polls/detail.html', {'question': question})
  ```

- 新建`templates/polls/detail.html`文件

  ```html
  {{ question }}
  ```

- 快捷方式`get_object_or_404()`，修改`polls/views.py`

  ```python
  from django.shortcuts import get_object_or_404, render
  
  from .models import Question
  # ...
  def detail(request, question_id):
      question = get_object_or_404(Question, pk=question_id)
      return render(request, 'polls/detail.html', {'question': question})
  ```

  访问http://127.0.0.1:8000/polls/234234/ 查看报错的效果

  此外`get_list_or_404()`也是类似的功能，在get列表时使用。替代了`filter()`函数



### 五、使用模板系统

- 修改`polls/detail.html`

  ```python
  <h1>{{ question.question_text }}</h1>
  <ul>
  {% for choice in question.choice_set.all %}
      <li>{{ choice.choice_text }}</li>
  {% endfor %}
  </ul>
  ```

  注意，这里的优点是可以访问对象的属性。

  访问http://127.0.0.1:8000/polls

### 六、删除模板中硬编码的URLs

在`templates/polls/index.html`文件中，还有一部分硬编码存在`href`里。如果不修改，那万一改变了路由，就要改变模板中所有对应的链接。

我们之前在`polls/urls.py`定义了urls的别名，可以把href修改如下：

```html
<!--<a href="/polls/{{ question.id }}/"> -->

<li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>
```

如果想调整视图，只需要在`polls/urls.py`文件中修改即可。

### 七、URL names的命名空间

- 在`polls/urls.py`文件中添加一个`app_name`变量

  ```python
  from django.urls import path
  
  from . import views
  
  app_name = 'polls'   # 重点是这一行
  
  urlpatterns = [
      path('', views.index, name='index'),
      path('<int:question_id>/', views.detail, name='detail'),
      path('<int:question_id>/results/', views.results, name='results'),
      path('<int:question_id>/vote/', views.vote, name='vote'),
  ]
  ```

- 把`templates/polls/index.html`中的：

  ```html
  <li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>
  ```

  改为：

  ```html
  <li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
  ```



## Part4：表单和类视图

### 一、表单form

- 先写一个前端的投票页面`templates/polls/index.html`

  ```python
  <h1>{{ question.question_text }}</h1>
  
  {% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}
  
  <form action="{% url 'polls:vote' question.id %}" method="post">
  {% csrf_token %}
  {% for choice in question.choice_set.all %}
      <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}">
      <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br>
  {% endfor %}
  <input type="submit" value="Vote">
  </form>
  ```

  解释：

  - `forloop.counter`表示当前循环的次数
  - 跨站请求伪造安全问题，用`{% csrf_token %}`来解决这个问题。

- 补上`polls/views.py`中vote的视图函数

  ```python
  from django.http import HttpResponse, HttpResponseRedirect
  from django.shortcuts import get_object_or_404, render
  from django.urls import reverse
  
  from .models import Choice, Question
  # ...
  def vote(request, question_id):
      question = get_object_or_404(Question, pk=question_id)
      try:
          selected_choice = question.choice_set.get(pk=request.POST['choice'])
      except (KeyError, Choice.DoesNotExist):     
          return render(request, 'polls/detail.html', {
              'question': question,
              'error_message': "You didn't select a choice.",
          })
      else:
          selected_choice.votes += 1
          selected_choice.save()       
          return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
  ```

  解释：

  - `request.POST`是一个类似字典的对象，可以通过键名访问提交的数据，具体可以查看templates里的html文件。
  - 如果`request.POST['choice']`返回异常，说明模板中的表单没有提供choice键值。
  - 这里返回了个重定向`HttpResponseRedirect`。重定向的地址根据`polls/urls.py`确定
  - `reverse`是为了避免硬编码URL。

- 补全`views.results`函数

- 访问http://127.0.0.1:8000/polls/1/进行投票

### 二、使用通用视图：减少重复代码

也就是flask中的视图模板。

整个过程的流程：

- 修改URLconf，打开`polls/urls.py`

  ```python
  from django.urls import path
  
  from . import views
  
  app_name = 'polls'
  urlpatterns = [
      path('', views.IndexView.as_view(), name='index'),
      path('<int:pk>/', views.DetailView.as_view(), name='detail'),
      path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
      path('<int:question_id>/vote/', views.vote, name='vote'),
  ]
  ```

  

- 删除旧的无用视图，删除`polls/views.py`中的index，detail，results视图。替换成django的通用视图

  ```python
  from django.http import HttpResponseRedirect
  from django.shortcuts import get_object_or_404, render
  from django.urls import reverse
  from django.views import generic
  
  from .models import Choice, Question
  
  
  class IndexView(generic.ListView):
      template_name = 'polls/index.html'
      context_object_name = 'latest_question_list'
  
      def get_queryset(self):
          """Return the last five published questions."""
          return Question.objects.order_by('-pub_date')[:5]
  
  
  class DetailView(generic.DetailView):
      model = Question
      template_name = 'polls/detail.html'
  
  
  class ResultsView(generic.DetailView):
      model = Question
      template_name = 'polls/results.html'
  
  
  def vote(request, question_id):
      ... # 同前面的一样，不需要修改
  ```

- 访问http://127.0.0.1:8000/polls/1/

- 疑惑

  - 如果使用了不止一个数据表怎么办



## Part5：测试

### 二、编写测试程序

测试程序会自己创建一个临时数据库，测试有没有问题。

- 将下面的代码输入投票应用的`polls/tests.py`文件中：

  ```python
  import datetime
  from django.utils import timezone
  from django.test import TestCase
  from .models import Question
  
  class QuestionMethodTests(TestCase):
      def test_was_published_recently_with_future_question(self):
          """
          在将来发布的问卷应该返回False
          """
          time = timezone.now() + datetime.timedelta(days=30)
          future_question = Question(pub_date=time)
          self.assertIs(future_question.was_published_recently(), False)
  ```

- 执行`python manage.py test polls`后，可以发现相应的bug

- 修复`polls/models.py`内的bug

  ```python
  # polls/models.py
  
  def was_published_recently(self):
      now = timezone.now()
      return now - datetime.timedelta(days=1) <= self.pub_date <= now
  ```

- 更全面的测试，在上面的测试类中增加两个函数

  ```python
  # polls/tests.py
  
  def test_was_published_recently_with_old_question(self):
      """
      只要是早于1天前的问卷，返回False
      """
      time = timezone.now() - datetime.timedelta(days=1, seconds=1)
      old_question = Question(pub_date=time)
      self.assertIs(old_question.was_published_recently(), False)
  
  def test_was_published_recently_with_recent_question(self):
      """
      最近一天内的问卷，返回True
      """
      time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
      recent_question = Question(pub_date=time)
      self.assertIs(recent_question.was_published_recently(), True)
  ```

  

## Part 6：静态文件

存放样式表和背景图片的。把静态文件放到统一指定的地方。

### 一、使用静态文件

- 在polls目录下创建`static/polls/style.css`，并写入

  ```css
  li a {
      color: green;
  }
  ```

- 在`polls/templates/polls/index.html`的头部加入下面的代码：

  ```html
  {% load static %}   # 这一行放到文件最顶部
  
  
  # 这一行放到head标签中
  <link rel="stylesheet" type="text/css" href="{% static 'polls/style.css' %}"> 
  ```

- 访问http://127.0.0.1:8000/polls/

### 二、添加背景图片

- 在`polls/static/polls/`下创建`images`子目录

- 随便从网上下个背景图片，放到`images`里，命名为`background.jpg`

- 在css样式文件`polls/static/polls/style.css`中添加下面的代码：

  ```python
  body {
      background: white url("images/background.jpg") no-repeat;
  }
  ```

- 访问http://127.0.0.1:8000/polls/



### 三、直接访问静态文件

访问http://127.0.0.1:8000/static/polls/images/background.jpg

## Part7: 自定义admin

### 一、自定义后台表单

修改admin表单默认排序，修改`polls/admin.py`

![](https://img2020.cnblogs.com/blog/1762677/202010/1762677-20201005191206035-1453376763.png)

```python
from django.contrib import admin

from .models import Question


class QuestionAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'question_text']

admin.site.register(Question, QuestionAdmin)
```



将表单划分为字段的集合

```python
from django.contrib import admin

from .models import Question


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]

admin.site.register(Question, QuestionAdmin)
```

### 二、添加关联对象

修改`polls/admin.py`，增加：

```python
from django.contrib import admin
from .models import Choice, Question

# ...
admin.site.register(Choice)
```

choice是和question关联的，但是我们希望创建question的同时把choice也给创建了。

```python
from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)
```

这个显示要更加扁平化

```python
class ChoiceInline(admin.TabularInline):
```

### 三、定制实例的列表页面

在管理页面中，只显示`__str()__`方法指定的内容，可以利用`list_display`展示属性在页面上

```python
class QuestionAdmin(admin.MolelAdmin):
    # ...
    list_display = ('question_text', 'pub_date', 'was_published_recently')
```

可以通过提供一些属性来改进输出的样式，修改`polls/models.py`文件

```python
# polls/models.py

class Question(models.Model):
    # ...
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
```



可以使用`list_filter`属性对显示结果进行过滤。会在页面顶部增加一个而过滤面板。

```python
# polls/admin.py 添加
# 在QuestionAdmin中添加
list_filter = ['pub_date']
```



添加这个可以增加搜索能力

### 四、定制admin整体页面

在manage.py 文件同级下创建一个templates目录。打开`mysite/settings.py`修改TEMPLATES

```python
# mysite/settings.py

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # 添加这一行
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

找到django源码存放的位置。

`django/contrib/admin/templates`把里面的`base_site.html`复制到刚刚创建的`admin`文件夹内。

可以修改里面的东西

ps：这一步失败了，但是应该不关键。