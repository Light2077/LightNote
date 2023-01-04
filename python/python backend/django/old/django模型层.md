# Django模型层

ORM(Object Relational Mapping)对象关系映射。简而言之，程序员不需要写MySQL语句了，就按照python的风格操作数据库就行，写好之后框架自动帮你转换成SQL语句



## 模型和字段

```python
from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
```

会在数据库自动建一个名为`myapp_person`的表



**每次对模型进行CRUD时都要执行`python manage.py migrate`**

可以提前执行`python manage.py makemigrations`让修改动作保存到记录文件中，方便GitHub等工具使用

### 模型的属性

隐藏属性`_state`

- adding: 如果当前模型实例还没保存到数据库，为True，否则为False
- db: 指向某个数据，表示当前模型实例是从该数据库读取到的

```
>>> blog = Blog.create('mary', 'ss')
>>> blog._state
<django.db.models.base.ModelState object at 0x00000203CD717D30>
>>> blog._state.adding
True
>>> blog._state.db
# None
```

### 模型方法

模型方法等于说操作一行数据。

类Manager方法提供**表级**数据操作

例子：

```python
class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()

    def baby_boomer_status(self):
        "Returns the person's baby-boomer status."
        import datetime
        if self.birth_date < datetime.date(1945, 8, 1):
            return "Pre-boomer"
        elif self.birth_date < datetime.date(1965, 1, 1):
            return "Baby boomer"
        else:
            return "Post-boomer"

    @property
    def full_name(self):
        "Returns the person's full name."
        return '%s %s' % (self.first_name, self.last_name)
    
    def __str__(self):
        return self.first_name + self.last_name
```

### 模型字段fields

也就是类属性，比如：

```python
from django.db import models

class Musician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    instrument = models.CharField(max_length=100)

class Album(models.Model):
    artist = models.ForeignKey(Musician, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    num_stars = models.IntegerField()
```

字段名规则：

- 不与python关键字冲突
- 不能有两个及以上的下划线，因为两个下划线是django的查询语法
- 不能以下划线结尾

### 常用字段类型

每个字段都是某个`Field`类的实例

- 决定数据表中对应列的数据类型
- HTML中对应的表单标签的类型
- 在admin后台和自动生成的表单中进行数据验证

父类都是`Field`类，`django.db.models.CharField`

| 类型                      | 说明                                                         |
| ------------------------- | ------------------------------------------------------------ |
| AutoField                 | 一个自动增加的整数类型字段。通常你不需要自己编写它，Django会自动帮你添加字段：`id = models.AutoField(primary_key=True)`，这是一个自增字段，从1开始计数。如果你非要自己设置主键，那么请务必将字段设置为`primary_key=True`。Django在一个模型中只允许有一个自增字段，并且该字段必须为主键！ |
| BigAutoField              | 64位整数类型自增字段，数字范围更大，从1到9223372036854775807 |
| BigIntegerField           | 64位整数字段（看清楚，非自增），类似IntegerField ，-9223372036854775808 到9223372036854775807。在Django的模板表单里体现为一个`NumberInput`标签。 |
| BinaryField               | 二进制数据类型。较少使用。                                   |
| **BooleanField**          | 布尔值类型。默认值是None。在HTML表单中体现为CheckboxInput标签。如果设置了参数null=True，则表现为NullBooleanSelect选择框。可以提供default参数值，设置默认值。 |
| **CharField**             | 最常用的类型，字符串类型。必须接收一个max_length参数，表示字符串长度不能超过该值。默认的表单标签是text input。 |
| **DateField**             | `class DateField(auto_now=False, auto_now_add=False, **options)`   ,  日期类型。一个Python中的datetime.date的实例。在HTML中表现为DateInput标签。在admin后台中，Django会帮你自动添加一个JS日历表和一个“Today”快捷方式，以及附加的日期合法性验证。两个重要参数：（参数互斥，不能共存）  `auto_now`:每当对象被保存时将字段设为当前日期，常用于保存最后修改时间。`auto_now_add`：每当对象被创建时，设为当前日期，常用于保存创建日期(注意，它是不可修改的)。设置上面两个参数就相当于给field添加了`editable=False`和`blank=True`属性。如果想具有修改属性，请用default参数。例子：`pub_time = models.DateField(auto_now_add=True)`，自动添加发布时间。 |
| DateTimeField             | 日期时间类型。Python的datetime.datetime的实例。与DateField相比就是多了小时、分和秒的显示，其它功能、参数、用法、默认值等等都一样。 |
| DecimalField              | 固定精度的十进制小数。相当于Python的Decimal实例，必须提供两个指定的参数！参数`max_digits`：最大的位数，必须大于或等于小数点位数 。`decimal_places`：小数点位数，精度。 当`localize=False`时，它在HTML表现为NumberInput标签，否则是textInput类型。例子：储存最大不超过999，带有2位小数位精度的数，定义如下：`models.DecimalField(..., max_digits=5, decimal_places=2)`。 |
| DurationField             | 持续时间类型。存储一定期间的时间长度。类似Python中的timedelta。在不同的数据库实现中有不同的表示方法。常用于进行时间之间的加减运算。但是小心了，这里有坑，PostgreSQL等数据库之间有兼容性问题！ |
| **EmailField**            | 邮箱类型，默认max_length最大长度254位。使用这个字段的好处是，可以使用Django内置的EmailValidator进行邮箱格式合法性验证。 |
| **FileField**             | `class FileField(upload_to=None, max_length=100, **options)`上传文件类型，后面单独介绍。 |
| FilePathField             | 文件路径类型，后面单独介绍                                   |
| FloatField                | 浮点数类型，对应Python的float。参考整数类型字段。            |
| **ImageField**            | 图像类型，后面单独介绍。                                     |
| **IntegerField**          | 整数类型，最常用的字段之一。取值范围-2147483648到2147483647。在HTML中表现为NumberInput或者TextInput标签。 |
| **GenericIPAddressField** | `class GenericIPAddressField(protocol='both', unpack_ipv4=False, **options)`,IPV4或者IPV6地址，字符串形式，例如`192.0.2.30`或者`2a02:42fe::4`。在HTML中表现为TextInput标签。参数`protocol`默认值为‘both’，可选‘IPv4’或者‘IPv6’，表示你的IP地址类型。 |
| JSONField                 | JSON类型字段。Django3.1新增。签名为`class JSONField(encoder=None,decoder=None,**options)`。其中的encoder和decoder为可选的编码器和解码器，用于自定义编码和解码方式。如果为该字段提供default值，请务必保证该值是个不可变的对象，比如字符串对象。 |
| PositiveBigIntegerField   | 正的大整数，0到9223372036854775807                           |
| PositiveIntegerField      | 正整数，从0到2147483647                                      |
| PositiveSmallIntegerField | 较小的正整数，从0到32767                                     |
| SlugField                 | slug是一个新闻行业的术语。一个slug就是一个某种东西的简短标签，包含字母、数字、下划线或者连接线，通常用于URLs中。可以设置max_length参数，默认为50。 |
| SmallAutoField            | Django3.0新增。类似AutoField，但是只允许1到32767。           |
| SmallIntegerField         | 小整数，包含-32768到32767。                                  |
| **TextField**             | 用于储存大量的文本内容，在HTML中表现为Textarea标签，最常用的字段类型之一！如果你为它设置一个max_length参数，那么在前端页面中会受到输入字符数量限制，然而在模型和数据库层面却不受影响。只有CharField才能同时作用于两者。 |
| TimeField                 | 时间字段，Python中datetime.time的实例。接收同DateField一样的参数，只作用于小时、分和秒。 |
| **URLField**              | 一个用于保存URL地址的字符串类型，默认最大长度200。           |
| **UUIDField**             | 用于保存通用唯一识别码（Universally Unique Identifier）的字段。使用Python的UUID类。在PostgreSQL数据库中保存为uuid类型，其它数据库中为char(32)。这个字段是自增主键的最佳替代品，后面有例子展示。 |

**1.FileField**

上传文件字段，真实的文件保存在服务器的文件系统

```python
class MyModel(models.Model):
    # 文件被传至`MEDIA_ROOT/uploads`目录，MEDIA_ROOT由你在settings文件中设置
    upload = models.FileField(upload_to='uploads/')
    # 或者
    # 被传到`MEDIA_ROOT/uploads/2015/01/30`目录，增加了一个时间划分
    upload = models.FileField(upload_to='uploads/%Y/%m/%d/')
```

**`upload_to`参数也可以接收一个回调函数，该函数返回具体的路径字符串**，如下例：

```python
# 实现了每个用户文件保存的位置都不同的作用
def user_directory_path(instance, filename):
    #文件上传到MEDIA_ROOT/user_<id>/<filename>目录中
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class MyModel(models.Model):
    upload = models.FileField(upload_to=user_directory_path)
```

例子中，`user_directory_path`这种回调函数，必须接收两个参数，然后返回一个Unix风格的路径字符串。参数`instace`代表一个定义了`FileField`的模型的实例，说白了就是当前数据记录。`filename`是原本的文件名。



当你访问一个模型对象中的文件字段时，Django会自动给我们提供一个 FieldFile实例作为文件的代理，通过这个代理，我们可以进行一些文件操作，主要如下：

- FieldFile.name ： 获取文件名
- FieldFile.size： 获取文件大小
- FieldFile.url ：用于访问该文件的url
- FieldFile.open(mode='rb')： 以类似Python文件操作的方式，打开文件
- FieldFile.close()： 关闭文件
- FieldFile.save(name, content, save=True)： 保存文件
- FieldFile.delete(save=True)： 删除文件

这些代理的API和Python原生的文件读写API非常类似，其实本质上就是进行了一层封装，让我们可以在Django内直接对模型中文件字段进行读写，而不需要绕弯子。

**2.ImageField**

```python
class ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, **options)
```

类似于FileField

**使用Django的ImageField需要提前安装pillow模块，pip install pillow即可。**

**3. 使用FileField或者ImageField字段的步骤：**

1. 在settings文件中，配置`MEDIA_ROOT`，作为你上传文件在服务器中的基本路径（为了性能考虑，这些文件不会被储存在数据库中）。再配置个`MEDIA_URL`，作为公用URL，指向上传文件的基本路径。请确保Web服务器的用户账号对该目录具有写的权限。
2. 添加FileField或者ImageField字段到你的模型中，定义好`upload_to`参数，文件最终会放在`MEDIA_ROOT`目录的“`upload_to`”子目录中。
3. 所有真正被保存在数据库中的，只是指向你上传文件路径的字符串而已。可以通过url属性，在Django的模板中方便的访问这些文件。例如，假设你有一个ImageField字段，名叫`mug_shot`，那么在Django模板的HTML文件中，可以使用`{{ object.mug_shot.url }}`来获取该文件。其中的object用你具体的对象名称代替。
4. 可以通过`name`和`size`属性，获取文件的名称和大小信息。

安全建议：

无论你如何保存上传的文件，一定要注意他们的内容和格式，避免安全漏洞！务必对所有的上传文件进行安全检查，确保它们不出问题！如果你不加任何检查就盲目的让任何人上传文件到你的服务器文档根目录内，比如上传了一个CGI或者PHP脚本，很可能就会被访问的用户执行，这具有致命的危害。

4. **FilePathField**

```python
class FilePathField(path='', match=None, recursive=False, allow_files=True, allow_folders=False, max_length=100, **options)
```

一种用来保存文件路径信息的字段。在数据表内以字符串的形式存在，默认最大长度100，可以通过max_length参数设置。

它包含有下面的一些参数：

`path`：必须指定的参数。表示一个系统绝对路径。path通常是个字符串，也可以是个可调用对象，比如函数。

`match`:可选参数，一个正则表达式，用于过滤文件名。只匹配基本文件名，不匹配路径。例如`foo.*\.txt$`，只匹配文件名`foo23.txt`，不匹配`bar.txt`与`foo23.png`。

`recursive`:可选参数，只能是True或者False。默认为False。决定是否包含子目录，也就是是否递归的意思。

`allow_files`:可选参数，只能是True或者False。默认为True。决定是否应该将文件名包括在内。它和`allow_folders`其中，必须有一个为True。

`allow_folders`： 可选参数，只能是True或者False。默认为False。决定是否应该将目录名包括在内。

比如：

```python
FilePathField(path="/home/images", match="foo.*", recursive=True)
```

它只匹配`/home/images/foo.png`，但不匹配`/home/images/foo/bar.png`，因为默认情况，只匹配文件名，而不管路径是怎么样的。

例子：

```python
import os
from django.conf import settings
from django.db import models

def images_path():
    return os.path.join(settings.LOCAL_FILE_DIR, 'images')

class MyModel(models.Model):
    file = models.FilePathField(path=images_path)
```

**5.UUIDField**

```python
import uuid     # Python的内置模块
from django.db import models

class MyUUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 其它字段
```

## 关系类型字段

### 一、多对一(ForeignKey)

```python
class ForeignKey(to, on_delete, **options)
```

比如多个学生由一个班主任负责？

```python
from django.db import models

class Manufacturer(models.Model):
    # ...
    pass

class Car(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    # ...
```

**外键要定义在‘多’的一方！**，每辆车都会有一个生产工厂，一个工厂可以生产N辆车

```python
from django.db import models

# 如果要关联的模型定义在当前模型之后，用字符串进行引用
class Car(models.Model):
    manufacturer = models.ForeignKey(
        'Manufacturer',    # 注意这里
        on_delete=models.CASCADE,
    )
    # ...

class Manufacturer(models.Model):
    # ...
    pass
```



如果要关联的对象在另外一个app中，可以显式的指出。下例假设Manufacturer模型存在于production这个app中，则Car模型的定义如下：

```python
class Car(models.Model):
    manufacturer = models.ForeignKey(
        'production.Manufacturer',      # 关键在这里！！
        on_delete=models.CASCADE,
    )
```

如果要创建一个递归的外键，也就是自己关联自己的的外键，使用下面的方法：

```python
models.ForeignKey('self', on_delete=models.CASCADE)
```

核心在于‘self’这个引用。什么时候需要自己引用自己的外键呢？典型的例子就是评论系统！一条评论可以被很多人继续评论，如下所示：

```python
class Comment(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField()
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE)
    # .....
```

注意上面的外键字段定义的是父评论，而不是子评论。为什么呢？因为外键要放在‘多’的一方！

在数据库里边，会给外键添加`_id`后缀

当一个外键关联的对象被删除时，Django将模仿`on_delete`参数定义的SQL约束执行相应操作。比如，你有一个可为空的外键，并且你想让它在关联的对象被删除时，自动设为null，可以如下定义：

```
user = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    blank=True,
    null=True,
)
```

#### on_delete

该参数可选的值都内置在`django.db.models`中（全部为大写），包括：

- CASCADE：模拟SQL语言中的`ON DELETE CASCADE`约束，将定义有外键的模型对象同时删除！（我理解为：把工厂删了，这些工厂生产的车也要删掉）
- PROTECT:阻止上面的删除操作，但是弹出`ProtectedError`异常
- SET_NULL：将外键字段设为null，只有当字段设置了`null=True`时，方可使用该值。
- SET_DEFAULT:将外键字段设为默认值。只有当字段设置了default参数时，方可使用。
- DO_NOTHING：什么也不做。
- SET()：设置为一个传递给SET()的值或者一个回调函数的返回值。注意大小写。
- RESTRICT: Django3.1新增。这个模式比较难以理解。它与PROTECT不同，在大多数情况下，同样不允许删除，但是在某些特殊情况下，却是可以删除的。

#### limit_choices_to

该参数用于限制外键所能关联的对象，只能用于Django的ModelForm（Django的表单模块）和admin后台，对其它场合无限制功能。其值可以是一个字典、Q对象或者一个返回字典或Q对象的函数调用，如下例所示：

```
staff_member = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    limit_choices_to={'is_staff': True},
)
```

这样定义，则ModelForm的`staff_member`字段列表中，只会出现那些`is_staff=True`的Users对象，这一功能对于admin后台非常有用。

可以参考下面的方式，使用函数调用：

```python
def limit_pub_date_choices():
    return {'pub_date__lte': datetime.date.utcnow()}

# ...
limit_choices_to = limit_pub_date_choices
# ...
```

#### related_name

用于关联对象反向引用模型的名称。以前面车和工厂的例子解释，就是从工厂反向关联到车的关系名称。

通常情况下，这个参数我们可以不设置，Django会默认以模型的小写加上`_set`作为反向关联名，比如对于工厂就是`car_set`，如果你觉得`car_set`还不够直观，可以如下定义：

```python
class Car(models.Model):
    manufacturer = models.ForeignKey(
        'production.Manufacturer',      
        on_delete=models.CASCADE,
        related_name='car_producted_by_this_manufacturer',  # 看这里！！
    )
```

也许我定义了一个蹩脚的词，但表达的意思很清楚。以后从工厂对象反向关联到它所生产的汽车，就可以使用`maufacturer.car_producted_by_this_manufacturer`了。

如果你不想为外键设置一个反向关联名称，可以将这个参数设置为“+”或者以“+”结尾，如下所示：

```
user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='+',
)
```

#### related_query_name

反向关联查询名。用于从目标模型反向过滤模型对象的名称。（过滤和查询在后续章节会介绍）

这个参数的默认值是定义有外键字段的模型的小写名，如果设置了`related_name`参数，那么就是这个参数值，如果在此基础上还指定了`related_query_name`的值，则是`related_query_name`的值。三者依次有优先顺序。

要注意`related_query_name`和`related_name`的区别，前者用于在做查询操作时候作为参数使用，后者主要用于在属性调用时使用。

```python
class Tag(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="tags",
        related_query_name="tag",       # 注意这一行
    )
    name = models.CharField(max_length=255)

# 现在可以使用‘tag’作为查询名了
Article.objects.filter(tag__name="important")
```

#### to_field

默认情况下，外键都是关联到被关联对象的主键上（一般为id）。如果指定这个参数，可以关联到指定的字段上，但是该字段必须具有`unique=True`属性，也就是具有唯一属性。

### 二、多对多(ManyToManyField)

```python
class ManyToManyField(to, **options)
```

多对多的字段可以定义在任何的一方，请尽量定义在符合人们思维习惯的一方，但不要同时都定义，只能选择一个模型设置该字段（比如我们通常将披萨上的配料字段放在披萨模型中，而不是在配料模型中放置披萨字段）

```python
from django.db import models

class Topping(models.Model):
    # ...
    pass

class Pizza(models.Model):
    # ...
    toppings = models.ManyToManyField(Topping)
```

- through与through_fields

  ```python
  from django.db import models
  
  class Person(models.Model):
      name = models.CharField(max_length=50)
  
  class Group(models.Model):
      name = models.CharField(max_length=128)
      members = models.ManyToManyField(
          Person,
          through='Membership',       ## 自定义中间表
          through_fields=('group', 'person'),
      )
  
  class Membership(models.Model):  # 这就是具体的中间表模型
      group = models.ForeignKey(Group, on_delete=models.CASCADE)
      person = models.ForeignKey(Person, on_delete=models.CASCADE)
      inviter = models.ForeignKey(
          Person,
          on_delete=models.CASCADE,
          related_name="membership_invites",
      )
      invite_reason = models.CharField(max_length=64)
  ```

  

###  三、一对一

```python
class OneToOneField(to, on_delete, parent_link=False, **options)
```

从概念上讲，一对一关系非常类似具有`unique=True`属性的外键关系，但是反向关联对象只有一个。

这种关系类型多数用于当一个模型需要从别的模型扩展而来的情况。

比如，Django自带auth模块的User用户表，如果你想在自己的项目里创建用户模型，又想方便的使用Django的auth中的一些功能，那么一个方案就是在你的用户模型里，使用一对一关系，添加一个与auth模块User模型的关联字段。

该关系的第一位置参数为关联的模型，其用法和前面的多对一外键一样。

如果你没有给一对一关系设置`related_name`参数，Django将使用当前模型的小写名作为默认值。

看下面的例子：

```python
from django.conf import settings
from django.db import models

# 两个字段都使用一对一关联到了Django内置的auth模块中的User模型
class MySpecialUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    supervisor = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='supervisor_of',
    )
```

这样下来，你的User模型将拥有下面的属性：

```python
>>> user = User.objects.get(pk=1)
>>> hasattr(user, 'myspecialuser')
True
>>> hasattr(user, 'supervisor_of')
True
```

跨模块的模型：

有时候，我们关联的模型并不在当前模型的文件内，没关系，就像我们导入第三方库一样的从别的模块内导入进来就好，如下例所示：

```python
from django.db import models
from geography.models import ZipCode

class Restaurant(models.Model):
    # ...
    zip_code = models.ForeignKey(
        ZipCode,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
```

## 字段的参数

### null

该值为True时，Django在数据库用NULL保存空值。默认值为False。对于保存字符串类型数据的字段，请尽量避免将此参数设为True，那样会导致两种‘没有数据’的情况，一种是`NULL`，另一种是空字符串`''`。Django 的惯例是使用空字符串而不是 `NULL`。

### blank

True时，字段可以为空。默认False。和null参数不同的是，null是纯数据库层面的，而blank是验证相关的，它与表单验证是否允许输入框内为空有关，与数据库无关。所以要小心一个null为False，blank为True的字段接收到一个空值可能会出bug或异常。

### choices

用于页面上的选择框标签，需要先提供一个二维的二元元组，第一个元素表示存在数据库内真实的值，第二个表示页面上显示的具体内容。在浏览器页面上将显示第二个元素的值。例如：

```
    YEAR_IN_SCHOOL_CHOICES = (
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
        ('GR', 'Graduate'),
    )
```

一般来说，最好将选项定义在类里，并取一个直观的名字，如下所示：

```
from django.db import models

class Student(models.Model):
    FRESHMAN = 'FR'
    SOPHOMORE = 'SO'
    JUNIOR = 'JR'
    SENIOR = 'SR'
    YEAR_IN_SCHOOL_CHOICES = (
        (FRESHMAN, 'Freshman'),
        (SOPHOMORE, 'Sophomore'),
        (JUNIOR, 'Junior'),
        (SENIOR, 'Senior'),
    )
    year_in_school = models.CharField(
        max_length=2,
        choices=YEAR_IN_SCHOOL_CHOICES,
        default=FRESHMAN,
    )

    def is_upperclass(self):
        return self.year_in_school in (self.JUNIOR, self.SENIOR)
```

注意：每当 `choices` 的顺序变动时将会创建新的迁移。

如果一个模型中有多个字段需要设置choices，可以将这些二维元组组合起来，显得更加整洁优雅，例如下面的做法：

```
MEDIA_CHOICES = [
    ('Audio', (
            ('vinyl', 'Vinyl'),
            ('cd', 'CD'),
        )
    ),
    ('Video', (
            ('vhs', 'VHS Tape'),
            ('dvd', 'DVD'),
        )
    ),
    ('unknown', 'Unknown'),
]
```

反过来，要获取一个choices的第二元素的值，可以使用`get_FOO_display()`方法，其中的FOO用字段名代替。对于下面的例子：   

```
from django.db import models

class Person(models.Model):
    SHIRT_SIZES = (
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    )
    name = models.CharField(max_length=60)
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)
```

使用方法：

```
>>> p = Person(name="Fred Flintstone", shirt_size="L")
>>> p.save()
>>> p.shirt_size
'L'
>>> p.get_shirt_size_display()
'Large'
```

从Django3.0开始，新增了TextChoices、IntegerChoices和Choices三个类，用来达到类似Python的enum枚举库的作用，下面是一个例子：

```
from django.utils.translation import gettext_lazy as _

class Student(models.Model):

    class YearInSchool(models.TextChoices):
        FRESHMAN = 'FR', _('Freshman')
        SOPHOMORE = 'SO', _('Sophomore')
        JUNIOR = 'JR', _('Junior')
        SENIOR = 'SR', _('Senior')
        GRADUATE = 'GR', _('Graduate')

    year_in_school = models.CharField(
        max_length=2,
        choices=YearInSchool.choices,
        default=YearInSchool.FRESHMAN,
    )

    def is_upperclass(self):
        return self.year_in_school in {
            self.YearInSchool.JUNIOR,
            self.YearInSchool.SENIOR,
        }
```

简要解释一下：

- 第一句导入是废话，搞国际化翻译的，和本例的内容其实没关系
- 核心在Student模型中创建了个内部类YearInSchool
- YearInSchool继承了Django新增的TextChoices类
- TextChoices中没定义别的，只定义了一些类变量，这些类变量看起来和我们前面使用的二维二元元组本质上是一个套路
- Student模型中有一个`year_in_school` 字段，其中定义了choices参数，参数的值是`YearInSchool.choices`
- `year_in_school` 字段还定义了default参数，值是`YearInSchool.FRESHMAN`
- 从本质上来说，这和我们开始使用choice的方式是一样的，只不过换成了类的方式，而不是二维元组

吐个槽，这么设计除了增加学习成本有什么好处？有多少Choice选项需要你非得用类的形式管理起来封装起来？二维元组它就不香吗？新手学习就不累吗？

吐槽归吐槽，该介绍的还得介绍，否则是不敬业。

如果你不需要人类可读的帮助文本，那么类似的YearInSchool还可以写成下面的方式：

```
>>> class Vehicle(models.TextChoices):
...     CAR = 'C'
...     TRUCK = 'T'
...     JET_SKI = 'J'
...
>>> Vehicle.JET_SKI.label
'Jet Ski'
```

*哎，我都写内部类了，还差这点吗？*

另外，由于使用整数作为选项的场景太常见了，Django除了提供TextChoices还提供了一个IntegerChoices，例子如下：

```
class Card(models.Model):

    class Suit(models.IntegerChoices):
        DIAMOND = 1
        SPADE = 2
        HEART = 3
        CLUB = 4

    suit = models.IntegerField(choices=Suit.choices)
```

实际上，Django为这几个类提供了一些属性，典型的有下面的：

- .label
- .choices
- .values
- .name

读者可以多尝试，看看每个的意义。

参考用法：

```
>>> MedalType = models.TextChoices('MedalType', 'GOLD SILVER BRONZE')
>>> MedalType.choices
[('GOLD', 'Gold'), ('SILVER', 'Silver'), ('BRONZE', 'Bronze')]
>>> Place = models.IntegerChoices('Place', 'FIRST SECOND THIRD')
>>> Place.choices
[(1, 'First'), (2, 'Second'), (3, 'Third')]
```

如果文本或数字类型不满足你的要求，你也可以继承Choice类，自己写。比如下面就创建了一个时间类型选项的choices类：

```
class MoonLandings(datetime.date, models.Choices):
    APOLLO_11 = 1969, 7, 20, 'Apollo 11 (Eagle)'
    APOLLO_12 = 1969, 11, 19, 'Apollo 12 (Intrepid)'
    APOLLO_14 = 1971, 2, 5, 'Apollo 14 (Antares)'
    APOLLO_15 = 1971, 7, 30, 'Apollo 15 (Falcon)'
    APOLLO_16 = 1972, 4, 21, 'Apollo 16 (Orion)'
    APOLLO_17 = 1972, 12, 11, 'Apollo 17 (Challenger)'
```

最后，如果想设置空标签，可以参考下面的做法：

```
class Answer(models.IntegerChoices):
    NO = 0, _('No')
    YES = 1, _('Yes')

    __empty__ = _('(Unknown)')
```

### db_column

该参数用于定义当前字段在数据表内的列名。如果未指定，Django将使用字段名作为列名。

### db_index

该参数接收布尔值。如果为True，数据库将为该字段创建索引。

### db_tablespace

用于字段索引的数据库表空间的名字，前提是当前字段设置了索引。默认值为工程的`DEFAULT_INDEX_TABLESPACE`设置。如果使用的数据库不支持表空间，该参数会被忽略。

### default

字段的默认值，可以是值或者一个可调用对象。如果是可调用对象，那么每次创建新对象时都会调用。设置的默认值不能是一个可变对象，比如列表、集合等等。lambda匿名函数也不可用于default的调用对象，因为匿名函数不能被migrations序列化。

注意：在某种原因不明的情况下将default设置为None，可能会引发`intergyerror：not null constraint failed`，即非空约束失败异常，导致`python manage.py migrate`失败，此时可将None改为False或其它的值，只要不是None就行。

### editable

如果设为False，那么当前字段将不会在admin后台或者其它的ModelForm表单中显示，同时还会被模型验证功能跳过。参数默认值为True。

### error_messages

用于自定义错误信息。参数接收字典类型的值。字典的键可以是`null`、 `blank`、 `invalid`、 `invalid_choice`、 `unique`和`unique_for_date`其中的一个。

### help_text

额外显示在表单部件上的帮助文本。即便你的字段未用于表单，它对于生成文档也是很有用的。

该帮助文本默认情况下是可以带HTML代码的，具有风险：

```
help_text="Please use the following format: <em>YYYY-MM-DD</em>."
```

所以使用时请注意转义为纯文本，防止脚本攻击。

### primary_key

如果你没有给模型的任何字段设置这个参数为True，Django将自动创建一个AutoField自增字段，名为‘id’，并设置为主键。也就是`id = models.AutoField(primary_key=True)`。

如果你为某个字段设置了primary_key=True，则当前字段变为主键，并关闭Django自动生成id主键的功能。

**`primary_key=True`隐含`null=False`和`unique=True`的意思。一个模型中只能有一个主键字段！** 

另外，主键字段不可修改，如果你给某个对象的主键赋个新值实际上是创建一个新对象，并不会修改原来的对象。

```
from django.db import models
class Fruit(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
###############    
>>> fruit = Fruit.objects.create(name='Apple')
>>> fruit.name = 'Pear'
>>> fruit.save()
>>> Fruit.objects.values_list('name', flat=True)
['Apple', 'Pear']
```

### unique

设为True时，在整个数据表内该字段的数据不可重复。

注意：对于ManyToManyField和OneToOneField关系类型，该参数无效。

注意： 当unique=True时，db_index参数无须设置，因为unqiue隐含了索引。

### unique_for_date

日期唯一。可能不太好理解。举个栗子，如果你有一个名叫title的字段，并设置了参数`unique_for_date="pub_date"`，那么Django将不允许有两个模型对象具备同样的title和pub_date。有点类似联合约束。

### unique_for_month

同上，只是月份唯一。

### unique_for_year

同上，只是年份唯一。

### verbose_name

为字段设置一个人类可读，更加直观的别名。

对于每一个字段类型，除了`ForeignKey`、`ManyToManyField`和`OneToOneField`这三个特殊的关系类型，其第一可选位置参数都是`verbose_name`。如果没指定这个参数，Django会利用字段的属性名自动创建它，并将下划线转换为空格。

下面这个例子的`verbose name`是"person’s first name":

```
first_name = models.CharField("person's first name", max_length=30)
```

下面这个例子的`verbose name`是"first name":

```
first_name = models.CharField(max_length=30)
```

对于外键、多对多和一对一字字段，由于第一个参数需要用来指定关联的模型，因此必须用关键字参数`verbose_name`来明确指定。如下：

```
poll = models.ForeignKey(
    Poll,
    on_delete=models.CASCADE,
    verbose_name="the related poll",
    )
sites = models.ManyToManyField(Site, verbose_name="list of sites")
    place = models.OneToOneField(
    Place,
    on_delete=models.CASCADE,
    verbose_name="related place",
)
```

另外，你无须大写`verbose_name`的首字母，Django自动为你完成这一工作。

### validators

运行在该字段上的验证器的列表。

## 多对多中间表详解

我们都知道对于ManyToMany字段，Django采用的是第三张中间表的方式。通过这第三张表，来关联ManyToMany的双方。下面我们根据一个具体的例子，详细解说中间表的使用。

### 一、默认中间表

首先，模型是这样的：

```
class Person(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person)

    def __str__(self):
        return self.name
```

在Group模型中，通过members字段，以ManyToMany方式与Person模型建立了关系。

让我们到数据库内看一下实际的内容，Django为我们创建了三张数据表，其中的app1是应用名。

![img](images/1762677-20201005193611044-454048719.png)

然后我在数据库中添加了下面的Person对象：

![img](images/1762677-20201005193614593-2091964418.png)

再添加下面的Group对象：

![img](images/1762677-20201005193619375-675570646.png)

让我们来看看，中间表是个什么样子的：

![img](images/1762677-20201005193623514-619690717.png)

首先有一列id，这是Django默认添加的，没什么好说的。然后是Group和Person的id列，这是默认情况下，Django关联两张表的方式。如果你要设置关联的列，可以使用to_field参数。

可见在**中间表中，并不是将两张表的数据都保存在一起，而是通过id的关联进行映射。**

中间表保存，这个小组有谁谁

### 二、自定义中间表

一般情况，普通的多对多已经够用，无需自己创建第三张关系表。但是某些情况可能更复杂一点，比如如果你想保存某个人加入某个分组的时间呢？想保存进组的原因呢？

Django提供了一个`through`参数，用于指定中间模型，你可以将类似进组时间，邀请原因等其他字段放在这个中间模型内。例子如下：

```python
from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=128)
    def __str__(self): 
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through='Membership')
    def __str__(self): 
        return self.name

class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()        # 进组时间
    invite_reason = models.CharField(max_length=64)  # 邀请原因
```

在中间表中，我们至少要编写两个外键字段，分别指向关联的两个模型。在本例中就是‘Person’和‘group’。 这里，我们额外增加了‘date_joined’字段，用于保存人员进组的时间，‘invite_reason’字段用于保存邀请进组的原因。

下面我们依然在数据库中实际查看一下（应用名为app2）：

![img](images/1762677-20201005193631055-731373086.png)

注意中间表的名字已经变成“app2_membership”了。

![img](images/1762677-20201005193635014-1022551854.png)

![img](images/1762677-20201005193641411-1981161453.png)

Person和Group没有变化。

![img](images/1762677-20201005193645282-1401697360.png)

但是中间表就截然不同了！它完美的保存了我们需要的内容。

使用中间表的例子

```python
>>> ringo = Person.objects.create(name="Ringo Starr")
>>> paul = Person.objects.create(name="Paul McCartney")
>>> beatles = Group.objects.create(name="The Beatles")
>>> m1 = Membership(person=ringo, group=beatles,
...     date_joined=date(1962, 8, 16),
...     invite_reason="Needed a new drummer.")
>>> m1.save()
>>> beatles.members.all()
<QuerySet [<Person: Ringo Starr>]>
>>> ringo.group_set.all()
<QuerySet [<Group: The Beatles>]>
>>> m2 = Membership.objects.create(person=paul, group=beatles,
...     date_joined=date(1960, 8, 1),
...     invite_reason="Wanted to form a band.")
>>> beatles.members.all()
<QuerySet [<Person: Ringo Starr>, <Person: Paul McCartney>]>
```

可以使用 add(), create(), 或 set() 创建关联对象，只需指定 

clear()方法能清空所有的多对多关系。

```
>>> # 甲壳虫乐队解散了
>>> beatles.members.clear()
>>> # 删除了中间模型的对象
>>> Membership.objects.all()
<QuerySet []>
```

## 模型的元数据Meta

模型的元数据，指的是“除了字段外的所有内容”，例如排序方式、数据库表名、人类可读的单数或者复数名等等。

模型Ox增加了两个元数据‘ordering’和‘verbose_name_plural’，分别表示排序和复数名

```python
from django.db import models

class Ox(models.Model):
    horn_length = models.IntegerField()

    class Meta:         # 注意，是模型的子类，要缩进！
        ordering = ["horn_length"]
        verbose_name_plural = "oxen"
```

**强调：每个模型都可以有自己的元数据类，每个元数据类也只对自己所在模型起作用。**

### abstract

如果`abstract=True`，那么模型会被认为是一个抽象模型。抽象模型本身不实际生成数据库表，而是作为其它模型的父类，被继承使用。具体内容可以参考Django模型的继承。

------

### app_label

如果定义了模型的app没有在`INSTALLED_APPS`中注册，则必须通过此元选项声明它属于哪个app，例如：

```
app_label = 'myapp'
```

------

### base_manager_name

模型的`_base_manager`管理器的名字，默认是`'objects'`。模型管理器是Django为模型提供的API所在。

------

### db_table

指定在数据库中，当前模型生成的数据表的表名。比如：

```
db_table = 'my_freinds'
```

如果你没有指定这个选项，那么Django会自动使用app名和模型名，通过下划线连接生成数据表名，比如`app_book`。

不要使用SQL语言或者Python的保留字，注意冲突。

友情建议：使用MySQL和MariaDB数据库时，`db_table`用小写英文。

------

### db_tablespace

自定义数据库表空间的名字。默认值是项目的`DEFAULT_TABLESPACE`配置项指定的值。

------

### default_manager_name

模型的`_default_manager`管理器的名字。

------

### default_related_name

默认情况下，从一个模型反向关联设置有关系字段的源模型，我们使用`<model_name>_set`，也就是源模型的名字+下划线+`set`。

这个元数据选项可以让你自定义反向关系名，同时也影响反向查询关系名！看下面的例子：

```
from django.db import models

class Foo(models.Model):
    pass

class Bar(models.Model):
    foo = models.ForeignKey(Foo, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'bars'   # 关键在这里
```

具体的使用差别如下：

```
>>> bar = Bar.objects.get(pk=1)
>>> # 不能再使用"bar"作为反向查询的关键字了。
>>> Foo.objects.get(bar=bar)
>>> # 而要使用你自己定义的"bars"了。
>>> Foo.objects.get(bars=bar)
```

------

### get_latest_by

Django管理器给我们提供有latest()和earliest()方法，分别表示获取最近一个和最前一个数据对象。但是，如何来判断最近一个和最前面一个呢？也就是根据什么来排序呢？

`get_latest_by`元数据选项帮你解决这个问题，它可以指定一个类似 `DateField`、`DateTimeField`或者`IntegerField`这种可以排序的字段，作为latest()和earliest()方法的排序依据，从而得出最近一个或最前面一个对象。例如：

```
get_latest_by = "order_date"   # 根据order_date升序排列

get_latest_by = ['-priority', 'order_date']  # 根据priority降序排列，如果发生同序，则接着使用order_date升序排列
```

------

### managed

该元数据默认值为True，表示Django将按照既定的规则，管理数据库表的生命周期。

如果设置为False，将不会针对当前模型创建和删除数据库表，也就是说Django暂时不管这个模型了。

在某些场景下，这可能有用，但更多时候，你可以忘记该选项。

------

### order_with_respect_to

这个选项不好理解。其用途是根据指定的字段进行排序，通常用于关系字段。看下面的例子：

```
from django.db import models

class Question(models.Model):
    text = models.TextField()
    # ...

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # ...

    class Meta:
        order_with_respect_to = 'question'
```

上面在Answer模型中设置了`order_with_respect_to = 'question'`，这样的话，Django会自动提供两个API，`get_RELATED_order()`和`set_RELATED_order()`，其中的`RELATED`用小写的模型名代替。假设现在有一个Question对象，它关联着多个Answer对象，下面的操作返回包含关联的Anser对象的主键的列表[1,2,3]：

```
>>> question = Question.objects.get(id=1)
>>> question.get_answer_order()
[1, 2, 3]
```

我们可以通过`set_RELATED_order()`方法，指定上面这个列表的顺序：

```
>>> question.set_answer_order([3, 1, 2])
```

同样的，关联的对象也获得了两个方法`get_next_in_order()`和`get_previous_in_order()`，用于通过特定的顺序访问对象，如下所示：

```
>>> answer = Answer.objects.get(id=2)
>>> answer.get_next_in_order()
<Answer: 3>
>>> answer.get_previous_in_order()
<Answer: 1>
```

这个元数据的作用......还没用过，囧。

------

### ordering

最常用的元数据之一了！

用于指定该模型生成的所有对象的排序方式，接收一个字段名组成的元组或列表。默认按升序排列，如果在字段名前加上字符“-”则表示按降序排列，如果使用字符问号“？”表示随机排列。请看下面的例子：

这个顺序是你通过查询语句，获得Queryset后的列表内元素的顺序，切不可和前面的`get_latest_by`等混淆。

```
ordering = ['pub_date']             # 表示按'pub_date'字段进行升序排列
ordering = ['-pub_date']            # 表示按'pub_date'字段进行降序排列
ordering = ['-pub_date', 'author']  # 表示先按'pub_date'字段进行降序排列，再按`author`字段进行升序排列。
```

------

### permissions

该元数据用于当创建对象时增加额外的权限。它接收一个所有元素都是二元元组的列表或元组，每个元素都是`(权限代码, 直观的权限名称)`的格式。比如下面的例子：

这个Meta选项非常重要，和auth框架的权限系统紧密相关。

```
permissions = (("can_deliver_pizzas", "可以送披萨"),)
```

------

### default_permissions

Django默认会在建立数据表的时候就自动给所有的模型设置('add', 'change',  'delete')的权限，也就是增删改。你可以自定义这个选项，比如设置为一个空列表，表示你不需要默认的权限，但是这一操作必须在执行migrate命令之前。也是配合auth框架使用。

------

### proxy

如果设置了`proxy = True`，表示使用代理模式的模型继承方式。具体内容与abstract选项一样，参考模型继承章节。

------

### required_db_features

声明模型依赖的数据库功能。比如['gis_enabled']，表示模型的建立依赖GIS功能。

------

### required_db_vendor

声明模型支持的数据库。Django默认支持`sqlite, postgresql, mysql, oracle`。

------

### select_on_save

决定是否使用1.6版本之前的`django.db.models.Model.save()`算法保存对象。默认值为False。这个选项我们通常不用关心。

------

### indexes

接收一个应用在当前模型上的索引列表，如下例所示：

```
from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
            models.Index(fields=['first_name'], name='first_name_idx'),
        ]
```

------

### unique_together

这个元数据是非常重要的一个！它等同于数据库的联合约束！

举个例子，假设有一张用户表，保存有用户的姓名、出生日期、性别和籍贯等等信息。要求是所有的用户唯一不重复，可现在有好几个叫“张伟”的，如何区别它们呢？（不要和我说主键唯一，这里讨论的不是这个问题）

我们可以设置不能有两个用户在同一个地方同一时刻出生并且都叫“张伟”，使用这种联合约束，保证数据库能不能重复添加用户（也不要和我谈小概率问题）。在Django的模型中，如何实现这种约束呢？

使用`unique_together`，也就是联合唯一！

比如：

```
unique_together = [['name', 'birth_day', 'address'],......]
```

这样，哪怕有两个在同一天出生的张伟，但他们的籍贯不同，也就是两个不同的用户。一旦三者都相同，则会被Django拒绝创建。这个元数据选项经常被用在admin后台，并且强制应用于数据库层面。

unique_together接收一个二维的列表，每个元素都是一维列表，表示一组联合唯一约束，可以同时设置多组约束。为了方便，对于只有一组约束的情况下，可以简单地使用一维元素，例如：

```
unique_together = ['name', 'birth_day', 'address']
```

联合唯一无法作用于普通的多对多字段。

### index_together

联合索引，用法和特性类似unique_together。

### constraints

为模型添加约束条件。通常是列表的形式，每个列表元素就是一个约束。

```
from django.db import models

class Customer(models.Model):
    age = models.IntegerField()

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(age__gte=18), name='age_gte_18'),
        ]
```

上例中，会检查age年龄的大小，不得低于18。

### verbose_name

最常用的元数据之一！用于设置模型对象的直观、人类可读的名称，用于在各种打印、页面展示等场景。可以用中文。例如：

```
verbose_name = "story"
verbose_name = "披萨"
```

如果你不指定它，那么Django会使用小写的模型名作为默认值。

------

### verbose_name_plural

英语有单数和复数形式。这个就是模型对象的复数名，比如“apples”。因为我们中文通常不区分单复数，所以保持和`verbose_name`一致也可以。

```
verbose_name_plural = "stories"
verbose_name_plural = "披萨"
verbose_name_plural = verbose_name
```

如果不指定该选项，那么默认的复数名字是`verbose_name`加上‘s’

------

### label

前面介绍的元数据都是可修改和设置的，但还有两个只读的元数据，label就是其中之一。

label等同于`app_label.object_name`。例如`polls.Question`，polls是应用名，Question是模型名。

------

### label_lower

同上，不过是小写的模型名。

## 模型继承

Django有三种继承的方式：

- 抽象基类：被用来继承的模型被称为`Abstract base classes`，将子类共同的数据抽离出来，供子类继承重用，它不会创建实际的数据表；
- 多表继承：`Multi-table inheritance`，每一个模型都有自己的数据库表，父子之间独立存在；
- 代理模型：如果你只想修改模型的Python层面的行为，并不想改动模型的字段，可以使用代理模型。

**注意！同Python的继承一样，Django也是可以同时继承两个以上父类的！**

### 一、 抽象基类：

只需要在模型的Meta类里添加`abstract=True`元数据项，就可以将一个模型转换为抽象基类。

Django不会为这种类创建实际的数据库表，它们也没有管理器，不能被实例化也无法直接保存，它们就是被当作父类供起来，让子类继承的。抽象基类完全就是用来保存子模型们共有的内容部分，达到重用的目的。当它们被继承时，它们的字段会全部复制到子模型中。看下面的例子：

```python
from django.db import models

class CommonInfo(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()

    class Meta:
        abstract = True

class Student(CommonInfo):
    home_group = models.CharField(max_length=5)
```

Student模型将拥有name，age，home_group三个字段，并且CommonInfo模型不能当做一个正常的模型使用。

那如果我想修改CommonInfo父类中的name字段的定义呢？在Student类中创建一个name字段，覆盖父类的即可。这其实就是很简单的Python语法。

那如果我不需要CommonInfo父类中的name字段呢？在Student类中创建一个name变量，值设为None即可。

#### 抽象基类的Meta数据：

如果子类没有声明自己的Meta类，那么它将自动继承抽象基类的Meta类。

如果子类要设置自己的Meta属性，则需要扩展基类的Meta

```python
from django.db import models

class CommonInfo(models.Model):
    # ...
    class Meta:
        abstract = True
        ordering = ['name']

class Student(CommonInfo):
    # ...
    class Meta(CommonInfo.Meta):   # 注意这里有个继承关系
        db_table = 'student_info'
```

这里有几点要特别说明：

- 抽象基类中有的元数据，子模型没有的话，直接继承；
- 抽象基类中有的元数据，子模型也有的话，直接覆盖；
- 子模型可以额外添加元数据；
- **抽象基类中的`abstract=True`这个元数据不会被继承**。也就是说如果想让一个抽象基类的子模型，同样成为一个抽象基类，那你必须显式的在该子模型的Meta中同样声明一个`abstract = True`；
- 有一些元数据对抽象基类无效，比如`db_table`，首先是抽象基类本身不会创建数据表，其次它的所有子类也不会按照这个元数据来设置表名。
- 由于Python继承的工作机制，如果子类继承了多个抽象基类，则默认情况下仅继承第一个列出的基类的 Meta 选项。如果要从多个抽象基类中继承 Meta 选项，必须显式地声明 Meta 继承。例如：

```python
from django.db import models

class CommonInfo(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()

    class Meta:
        abstract = True
        ordering = ['name']

class Unmanaged(models.Model):
    class Meta:
        abstract = True
        managed = False

class Student(CommonInfo, Unmanaged):
    home_group = models.CharField(max_length=5)

    class Meta(CommonInfo.Meta, Unmanaged.Meta):
        pass
```

#### 警惕related_name和related_query_name参数

如果在你的抽象基类中存在ForeignKey或者ManyToManyField字段，并且使用了`related_name`或者`related_query_name`参数，那么一定要小心了。因为按照默认规则，每一个子类都将拥有同样的字段，这显然会导致错误。为了解决这个问题，当你在抽象基类中使用`related_name`或者`related_query_name`参数时，它们两者的值中应该包含`%(app_label)s`和`%(class)s`部分：

- `%(class)s`用字段所属子类的小写名替换
- `%(app_label)s`用子类所属app的小写名替换

例如，对于`common/models.py`模块：

```
from django.db import models

class Base(models.Model):
    m2m = models.ManyToManyField(
    OtherModel,
    related_name="%(app_label)s_%(class)s_related",
    related_query_name="%(app_label)s_%(class)ss",
    )

    class Meta:
        abstract = True

class ChildA(Base):
    pass

class ChildB(Base):
    pass
```

对于另外一个应用中的`rare/models.py`:

```
from common.models import Base

class ChildB(Base):
    pass
```

对于上面的继承关系：

- `common.ChildA.m2m`字段的`reverse name`（反向关系名）应该是`common_childa_related`；`reverse query name`(反向查询名)应该是`common_childas`。
- `common.ChildB.m2m`字段的反向关系名应该是`common_childb_related`；反向查询名应该是`common_childbs`。
- `rare.ChildB.m2m`字段的反向关系名应该是`rare_childb_related`；反向查询名应该是`rare_childbs`。

当然，如果你不设置`related_name`或者`related_query_name`参数，这些问题就不存在了。

### 二、多表继承

这种继承方式下，父类和子类都是独立自主、功能完整、可正常使用的模型，都有自己的数据库表，内部隐含了一个一对一的关系。例如：

```python
from django.db import models

class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

class Restaurant(Place):
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)
```

Restaurant将包含Place的所有字段，并且各有各的数据库表和字段

多表继承不能继承父类的Meta功能

只有`ordering`和`get_latest_by`可以被继承

#### 多表继承和反向关联

因为多表继承使用了一个隐含的OneToOneField来链接子类与父类，所以象上例那样，你可以从父类访问子类。但是这个OnetoOneField字段默认的`related_name`值与ForeignKey和 ManyToManyField默认的反向名称相同。如果你与父类或另一个子类做多对一或是多对多关系，你就必须在每个多对一和多对多字段上强制指定`related_name`。如果你没这么做，Django就会在你运行或验证(validation)时抛出异常。

仍以上面Place类为例，我们创建一个带有ManyToManyField字段的子类：

```
class Supplier(Place):
    customers = models.ManyToManyField(Place)
```

这会产生下面的错误：

```
Reverse query name for 'Supplier.customers' clashes with reverse query
name for 'Supplier.place_ptr'.
HINT: Add or change a related_name argument to the definition for
'Supplier.customers' or 'Supplier.place_ptr'.
```

解决方法是：向customers字段中添加`related_name`参数.

```
customers = models.ManyToManyField(Place, related_name='provider')
```

### 三、 代理模型

使用多表继承时，父类的每个子类都会创建一张新数据表，通常情况下，这是我们想要的操作，因为子类需要一个空间来存储不包含在父类中的数据。但有时，你可能只想更改模型在Python层面的行为，比如更改默认的manager管理器，或者添加一个新方法。

代理模型就是为此而生的。你可以创建、删除、更新代理模型的实例，并且所有的数据都可以像使用原始模型（非代理类模型）一样被保存。不同之处在于你可以在代理模型中改变默认的排序方式和默认的manager管理器等等，而不会对原始模型产生影响。

代理模型其实就是给原模型换了件衣服（API），实际操作的还是原来的模型和数据。

**声明一个代理模型只需要将Meta中proxy的值设为True。**

例如你想给Person模型添加一个方法。你可以这样做：

```
from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

class MyPerson(Person):
    class Meta:
        proxy = True

    def do_something(self):
        # ...
        pass
```

MyPerson类将操作和Person类同一张数据库表。并且任何新的Person实例都可以通过MyPerson类进行访问，反之亦然。

```
>>> p = Person.objects.create(first_name="foobar")
>>> MyPerson.objects.get(first_name="foobar")
<MyPerson: foobar>
```

下面的例子通过代理进行排序，但父类却不排序：

```
class OrderedPerson(Person):
    class Meta:
        # 现在，普通的Person查询是无序的，而OrderedPerson查询会按照`last_name`排序。
        ordering = ["last_name"]
        proxy = True
```

**一些约束：**

- 代理模型必须继承自一个非抽象的基类，并且不能同时继承多个非抽象基类；
- 代理模型可以同时继承任意多个抽象基类，前提是这些抽象基类没有定义任何模型字段。
- 代理模型可以同时继承多个别的代理模型，前提是这些代理模型继承同一个非抽象基类。

如果你理解透彻了代理模型的本质，那么上面的三条约束是顺理成章的。

**代理模型的管理器**

如不指定，则继承父类的管理器。如果你自己定义了管理器，那它就会成为默认管理器，但是父类的管理器依然有效。如下例子：

```
from django.db import models

class NewManager(models.Manager):
    # ...
    pass

class MyPerson(Person):
    objects = NewManager()

    class Meta:
        proxy = True
```

如果你想要向代理中添加新的管理器，而不是替换现有的默认管理器，你可以创建一个含有新的管理器的基类，并在继承时把他放在主基类的后面：

```
# Create an abstract class for the new manager.
from django.db import models

class NewManager(models.Manager):
    # ...
    pass

class ExtraManagers(models.Model):
    secondary = NewManager()

    class Meta:
        abstract = True

class MyPerson(Person, ExtraManagers):
    class Meta:
        proxy = True
```

### 四、多重继承

注意，多重继承和多表继承是两码事，两个概念。

Django的模型体系支持多重继承，就像Python一样。如果多个父类都含有Meta类，则只有第一个父类的会被使用，剩下的会忽略掉。

一般情况，能不要多重继承就不要，尽量让继承关系简单和直接，避免不必要的混乱和复杂。

#### 警告

在Python语言层面，子类可以拥有和父类相同的属性名，这样会造成覆盖现象。但是对于Django，如果继承的是一个非抽象基类，那么子类与父类之间不可以有相同的字段名！

比如下面是不行的！

```
class A(models.Model):
    name = models.CharField(max_length=30)

class B(A):
    name = models.CharField(max_length=30)
```

如果你执行`python manage.py makemigrations`会弹出下面的错误：

```
django.core.exceptions.FieldError: Local field 'name' in class 'B' clashes with field of the same name from base class 'A'.
```

但是！如果父类是个抽象基类就没有问题，如下：

```
class A(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        abstract = True

class B(A):
    name = models.CharField(max_length=30)
```

### 五、用包来组织模型

在我们使用`python manage.py startapp xxx`命令创建新的应用时，Django会自动帮我们建立一个应用的基本文件组织结构，其中就包括一个`models.py`文件。通常，我们把当前应用的模型都编写在这个文件里，但是如果你的模型很多，那么将单独的`models.py`文件分割成一些独立的文件是个更好的做法。

首先，我们需要在应用中新建一个叫做`models`的包，再在包下创建一个`__init__.py`文件，这样才能确立包的身份。然后将`models.py`文件中的模型分割到一些`.py`文件中，比如`organic.py`和`synthetic.py`，然后删除`models.py`文件。最后在`__init__.py`文件中导入所有的模型。如下例所示：

```
#  myapp/models/__init__.py

from .organic import Person
from .synthetic import Robot
```

要显式明确地导入每一个模型，而不要使用`from .models import *`的方式，这样不会混淆命名空间，让代码更可读，更容易被分析工具使用。

## 验证器

模型相关验证器，表单验证器，验证器在模型的字段参数中`validators`

### 一、自定义验证器

验证器本质上就是可调用的对象（函数或类）如果不满足某些规则，则抛出`ValidationError`异常，例如：

```python
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(
            _('%(value)s is not an even number'),
            params={'value': value},
        )
```

通过下面的方式，将偶数验证器应用在字段上：

```python
from django.db import models

class MyModel(models.Model):
    even_field = models.IntegerField(validators=[validate_even])
```

因为验证器运行之前，（输入的）数据会被转换为 Python 对象，因此我们可以将同样的验证器用在 Django form 表单中（事实上Django为表单提供了另外一些验证器）：

```python
from django import forms

class MyForm(forms.Form):
    even_field = forms.IntegerField(validators=[validate_even])
```

你还可以通过Python的魔法方法`__call__()`编写更复杂的可配置的验证器，比如Django内置的`RegexValidator`验证器就是这么干的。

验证器也可以是一个类，但这时候就比较复杂了，需要确保它可以被迁移框架序列化，确保编写了`deconstruction()`和`__eq__()`方法。*这种做法很难找到参考文献和博文，要靠自己摸索或者研究DJango源码。*

### 总结

Django中模型验证器的使用套路：

- 编写字段级别的验证器，在字段中作为参数指定
- 或者编写clean()方法，实现模型级别、跨字段的验证功能
- 重写save()方法，调用`full_clean()`，实现全自动的验证
- 或者在视图中，通过模型实例调用`full_clean()`方法，实现手动验证

### 三、内置验证器

验证器的作用很重要，需求也很广泛，Django为此内置了一些验证器，我们直接拿来使用即可：

#### RegexValidator

这是正则匹配验证器。用于对输入的值进行正则搜索，如果命中，则平安无事，如果没命中则弹出 `ValidationError` 异常。

数字签名：`class RegexValidator(regex=None, message=None, code=None, inverse_match=None, flags=0)`

参数说明：

- regex：用于匹配的正则表达式
- message：自定义异常错误信息。默认是`"Enter a valid value"`
- code：自定义错误码。默认是`"invalid"`
- inverse_match：将通过和不通过验证的判断逻辑反转。也就是未命中则平安，命中则出错。
- flags：编译正则表达式时使用的正则flags。默认为0。

#### EmailValidator

数字签名：`class EmailValidator(message=None, code=None, whitelist=None)`

邮件格式验证器。

参数说明：

- message: 自定义错误信息，默认为 "Enter a valid email address"。
- code： 自定义错误码，默认为"invalid"。
- whitelist：邮件域名白名单，默认为`['localhost']`。

#### URLValidator

数字签名：`class URLValidator(schemes=None, regex=None, message=None, code=None)`

RegexValidator的子类，用于验证url的格式是否正确。

schemes：指定URL/URI的协议模式，默认值为`['http', 'https', 'ftp', 'ftps']`

### 有帮助的`ValidationError`

综合在一起，推荐的例子：

```python
raise ValidationError(
    _('Invalid value: %(value)s'),
    code='invalid',
    params={'value': '42'},
)
```

当需要同时展示多个验证错误的时候：

```python
# 好的做法
raise ValidationError([
    ValidationError(_('Error 1'), code='error1'),
    ValidationError(_('Error 2'), code='error2'),
])

# 差的做法
raise ValidationError([
    _('Error 1'),
    _('Error 2'),
])
```

## 查询操作

### 一、创建对象

创建一个模型实例，也就是一条数据库记录，最一般的方式是使用模型类的实例化构造方法：

```python
>>> from blog.models import Blog
>>> b = Blog(name='Beatles Blog', tagline='All the latest Beatles news.')
>>> b.save()
```

但是不会验证完整性。



如果想要一行代码完成上面的操作，请使用`creat()`方法，它可以省略save的步骤，比如：

```python
b = Blog.objects.create(name='刘江的博客', tagline='主页位于liujiangblog.com.')
```

有很多人喜欢在模型的初始化上做文章，实现一些额外的业务需求，常见的做法是自定义`__init__`方法。这不好，容易打断Django源码的调用链，存在漏洞。更推荐的是下面两种方法。

第一种方法：为模型增加create类方法，在其中夹塞你的代码：

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)

    @classmethod
    def create(cls, title):
        book = cls(title=title)
        # 将你的个人代码放在这里
        print('测试一下是否工作正常')
        return book

book = Book.create("liujiangblog.com")   # 注意，改为使用created方法创建Book对象
book.save()           # 只有调用save后才能保存到数据库
```

第二种方法：自定义管理器，并在其中添加创建对象的方法，推荐！

```python
class BookManager(models.Manager):   # 继承默认的管理器
    def create_book(self, title):
        book = self.create(title=title)
        # 将你的个人代码放在这里
        print('测试一下是否工作正常')
        return book

class Book(models.Model):
    title = models.CharField(max_length=100)

    objects = BookManager()   # 赋值objects

book = Book.objects.create_book("liujiangblog.com")   #改为使用create_book方法创建对象
```

### 二、修改对象并保存

可以重写save()方法，实现自己的业务逻辑。正常情况

```python
# b5 是 Blog 类的对象
b5.name = 'Tom'
b5.save()
```

**可以重写Blog类的save方法**

```python
from django.db import models

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def save(self, *args, **kwargs):
        do_something()   # 保存前做点私活
        super().save(*args, **kwargs)  # 一定不要忘记这行代码
        do_something_else()  # 保存后又加塞点东西
```



**实现类似点赞+1的功能**

要使用F表达式，这样就能直接在数据库中进行操作

```python
from django.db.models import F

entry = Entry.objects.get(name='blog name')
entry.number_of_pingbacks = F('number_of_pingbacks') + 1
entry.save()
```



**保存外键**

和保存普通字段完全一样。



**保存多对多字段**

使用add，不需要调用save方法

```python
from blog.models import Author
john = Author.objects.create(name="John")
paul = Author.objects.create(name="Paul")
entry.authors.add(john, paul)
```

### 三、检索对象

就相当于用mysql的select ... from ...

**检索所有对象**

```python
all_entries = Entry.objects.all()
```



**过滤对象**

- `filter()`: 返回满足指定参数查出来的QuerySet
- `exclude()`: 和`filter()`相反



**可以链式调用**

```python
Entry.objects.filter(...).exclude(...).filter(...)
```



**QuerySets的独立性**

q1.filter()不会对q1有影响

```python
q1 = Entry.objects.filter(headline__startswith="What")
q2 = q1.exclude(pub_date__gte=datetime.date.today())
q3 = q1.filter(pub_date__gte=datetime.date.today())
```



**QuerySets的惰性**

意思就是代码运行到这步了并没有对数据库进行操作。只有实际用到数据时才会操作

```python
q = Entry.objects.filter(headline__startswith="What")
q = q.filter(pub_date__lte=datetime.date.today())
q = q.exclude(body_text__icontains="food")
# 前三句执行完后，并没有对数据库进行操作
print(q)
```



**检索单一对象**

使用`get()`，但注意，如果返回对象为空，或者大于1个对象，都会报错。其余用法和`filter()`完全一致

```python
one_entry = Entry.objects.get(pk=1)
```



**QuerySet切片**

和python列表一样，但是**不允许负索引**

```python
Entry.objects.all()[:5]      # 返回前5个对象

# Entry.objects.all()[-1]  # 禁止负索引
```

#### 如何进行字段查询

`<字段名>__<查询方式>`，比如：

```python
>>> Entry.objects.filter(pub_date__lte='2020-01-01')
#　相当于：
SELECT * FROM blog_entry WHERE pub_date <= '2020-01-01';
```

默认是exact查询，比如：

这两个是一样的

```python
Blog.objects.get(id__exact=14)  # 显示指定
Blog.objects.get(id=14)         # 隐含__exact
```



| 字段名          | 说明                       |
| --------------- | -------------------------- |
| **exact**       | 精确匹配                   |
| **iexact**      | 不区分大小写的精确匹配     |
| **contains**    | 包含匹配                   |
| **icontains**   | 不区分大小写的包含匹配     |
| **in**          | 在..之内的匹配             |
| **gt**          | 大于                       |
| **gte**         | 大于等于                   |
| **lt**          | 小于                       |
| **lte**         | 小于等于                   |
| **startswith**  | 从开头匹配                 |
| **istartswith** | 不区分大小写从开头匹配     |
| **endswith**    | 从结尾处匹配               |
| **iendswith**   | 不区分大小写从结尾处匹配   |
| **range**       | 范围匹配                   |
| **date**        | 日期匹配                   |
| **year**        | 年份                       |
| iso_year        | 以ISO 8601标准确定的年份   |
| **month**       | 月份                       |
| **day**         | 日期                       |
| **week**        | 第几周                     |
| **week_day**    | 周几                       |
| iso_week_day    | 以ISO 8601标准确定的星期几 |
| quarter         | 季度                       |
| **time**        | 时间                       |
| **hour**        | 小时                       |
| **minute**      | 分钟                       |
| **second**      | 秒                         |
| **regex**       | 区分大小写的正则匹配       |
| **iregex**      | 不区分大小写的正则匹配     |

#### 跨越关系查询

也就是mysql中join查询。

`<其他的模型名>__<其他模型的字段>__<查询方式>`，比如：

```python
Entry.objects.filter(blog__name='Beatles Blog')
```

反之亦然

```python
Blog.objects.filter(entry__headline__contains='Lennon')
```



有坑，先记着不用理解，就知道链式查询和一次性查询结果可能不一样：

```python
Blog.objects.filter(entry__headline__contains='Lennon', entry__pub_date__year=2008)
Blog.objects.filter(entry__headline__contains='Lennon').filter(entry__pub_date__year=2008)
```



**F表达式**

允许模型的某个字段，与该模型的另一个字段进行比较：

假设Entry模型（在数据库中也就是Entry表）有两个字段`number_of_comments`和`number_of_pingbacks`

```python
from django.db.models import F
Entry.objects.filter(number_of_comments__gt=F('number_of_pingbacks'))
```

F()对象支持基本的算数操作

```python
Entry.objects.filter(number_of_comments__gt=F('number_of_pingbacks') * 2)
Entry.objects.filter(rating__lt=F('number_of_comments') + F('number_of_pingbacks'))
# 甚至可以跨表查询
Entry.objects.filter(authors__name=F('blog__name'))

# 甚至可以加减timedelta对象
from datetime import timedelta
Entry.objects.filter(mod_date__gt=F('pub_date') + timedelta(days=3))

# 甚至可以支持位运算
F('somefield').bitand(16)

```



**主键查询**

```python
Blog.objects.get(pk=14)
```



**缓存与查询集效率提高**

缓存，不要重复调用查询

```python
# 不好，查询了两次
print([e.headline for e in Entry.objects.all()])
print([e.pub_date for e in Entry.objects.all()])

# 好，只查询了一次
queryset = Entry.objects.all()
print([p.headline for p in queryset]) # 提交查询
print([p.pub_date for p in queryset]) # 重用查询缓存
```

**何时不会被缓存**

有一些操作不会缓存QuerySet，例如切片和索引。这就导致这些操作没有缓存可用，每次都会执行实际的数据库查询操作。例如：

```python
>>> queryset = Entry.objects.all()
>>> print(queryset[5]) # 查询数据库
>>> print(queryset[5]) # 再次查询数据库
```

但是，如果已经遍历过整个QuerySet，那么就相当于缓存过，后续的操作则会使用缓存，例如：

```python
>>> queryset = Entry.objects.all()
>>> [entry for entry in queryset] # 查询数据库
>>> print(queryset[5]) # 使用缓存
>>> print(queryset[5]) # 使用缓存
```

下面的这些操作都将遍历QuerySet并建立缓存：

```python
>>> [entry for entry in queryset]
>>> bool(queryset)
>>> entry in queryset
>>> list(queryset)
```

注意：简单的打印QuerySet并不会建立缓存，因为`__repr__()`调用只返回全部查询集的一个切片。

### 四、查询JSONField

什么是JSONField？我猜应该就是JSON字符串，给前端用的

这里None值可能会混淆。直接例子吧虽然觉得不关键

```python
from django.db import models

class Dog(models.Model):
    name = models.CharField(max_length=200)
    data = models.JSONField(null=True)

    def __str__(self):
        return self.name
```



```python
Dog.objects.create(name='Max', data=None)  # SQL NULL.  <Dog: Max>
Dog.objects.create(name='Archie', data=Value('null'))  # JSON null.  <Dog: Archie>

Dog.objects.filter(data=None)  # <QuerySet [<Dog: Archie>]>
Dog.objects.filter(data=Value('null'))  # <QuerySet [<Dog: Archie>]>

Dog.objects.filter(data__isnull=True)  # <QuerySet [<Dog: Max>]>
Dog.objects.filter(data__isnull=False)  # <QuerySet [<Dog: Archie>]>
```



**可以通过json的键来进行查询**

```shell
>>> Dog.objects.create(name='Rufus', data={
...     'breed': 'labrador',
...     'owner': {
...         'name': 'Bob',
...         'other_pets': [{
...             'name': 'Fishy',
...         }],
...     },
... })
<Dog: Rufus>
>>> Dog.objects.create(name='Meg', data={'breed': 'collie', 'owner': None})
<Dog: Meg>
>>> Dog.objects.filter(data__breed='collie')
<QuerySet [<Dog: Meg>]>
```



**对于嵌套的情况**

```shell
>>> Dog.objects.filter(data__owner__name='Bob')
<QuerySet [<Dog: Rufus>]>
```



**整数的情况，就当做索引**

```shell
>>> Dog.objects.filter(data__owner__other_pets__0__name='Fishy')
<QuerySet [<Dog: Rufus>]>
```



#### 包含与查找键

**contains**

对于JSONField，contains与其他Field略有区别，主要查找的是键值对，**也就是查某个键有某个值的所有对象**

```shell
>>> Dog.objects.create(name='Rufus', data={'breed': 'labrador', 'owner': 'Bob'})
<Dog: Rufus>
>>> Dog.objects.create(name='Meg', data={'breed': 'collie', 'owner': 'Bob'})
<Dog: Meg>
>>> Dog.objects.create(name='Fred', data={})
<Dog: Fred>
>>> Dog.objects.filter(data__contains={'owner': 'Bob'})
<QuerySet [<Dog: Rufus>, <Dog: Meg>]>
>>> Dog.objects.filter(data__contains={'breed': 'collie'})
<QuerySet [<Dog: Meg>]>
```



**contained_by**

感觉不好懂，不关键



**has_key**

通过键过滤对象，匹配的键必须位于嵌套的最顶层：

```shell
>>> Dog.objects.create(name='Rufus', data={'breed': 'labrador'})
<Dog: Rufus>
>>> Dog.objects.create(name='Meg', data={'breed': 'collie', 'owner': 'Bob'})
<Dog: Meg>
>>> Dog.objects.filter(data__has_key='owner')
<QuerySet [<Dog: Meg>]>
```

**has_keys**

**has_any_keys**

### 五、Q对象

之前都是and逻辑，用Q对象可以实现or逻辑

```python
from django.db.models import Q
Q(question__startswith='What')
```

可以使用`&`或者`|`或`~`来组合Q对象，分别表示与、或、非逻辑。它将返回一个新的Q对象。

逗号分隔表示and关系

当关键字参数和Q对象组合使用时，Q对象必须放在前面：



```python
Poll.objects.get(
Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6)), question__startswith='Who')
```

### 六、比较对象

比较模型实例，其实就是比较主键值

```shell
>>> some_entry == other_entry
>>> some_entry.id == other_entry.id
```

### 七、删除对象

删除对象使用的是对象的`delete()`方法。该方法将返回被删除对象的总数量和一个字典，字典包含了每种被删除对象的类型和该类型的数量。如下所示：

```shell
>>> e.delete()
(1, {'weblog.Entry': 1})
```

也可以批量删除。每个QuerySet都有一个delete()方法，它能删除该QuerySet的所有成员。例如：

```shell
>>> Entry.objects.filter(pub_date__year=2020).delete()
(5, {'webapp.Entry': 5})
```



如果改写delete方法，就要手动迭代QuerySet进行逐一删除



删除一个对象是，默认受SQL的ON DELETE CASCADE约束，也就是有外键指向要删除对象的对象会被一起删除。

### 八、复制模型实例

```python
blog = Blog(name='My blog', tagline='Blogging is easy')
blog.save() # blog.pk == 1
#
blog.pk = None
blog.save() # blog.pk == 2
```

有继承时，要同时将pk和id设为None



如果有多对多关系，还要给复制后的新实例设置多对多关系

```shell
entry = Entry.objects.all()[0] # some previous entry
old_authors = entry.authors.all()
entry.pk = None
entry.save()
entry.authors.set(old_authors)
```



对于OneToOneField，还要复制相关对象并将其分配给新对象的字段，以避免违反一对一唯一约束。 例如，假设entry已经如上所述重复：

```
detail = EntryDetail.objects.all()[0]
detail.pk = None
detail.entry = entry
detail.save()
```



### 九、批量更新对象

使用`update()`方法可以批量为QuerySet中所有的对象进行更新操作。

```python
# 更新所有2007年发布的entry的headline
Entry.objects.filter(pub_date__year=2020).update(headline='刘江的Django教程')
```

只可以对普通字段和ForeignKey字段使用这个方法。若要更新一个普通字段，只需提供一个新的常数值。若要更新ForeignKey字段，需设置新值为你想指向的新模型实例。例如：

```shell
>>> b = Blog.objects.get(pk=1)
# 修改所有的Entry，让他们都属于b
>>> Entry.objects.all().update(blog=b)
```

update方法会被立刻执行，并返回操作匹配到的行的数目（有可能不等于要更新的行的数量，因为有些行可能已经有这个新值了）。

唯一的约束是：只能访问一张数据库表。你可以根据关系字段进行过滤，但你只能更新模型主表的字段。例如：

```shell
>>> b = Blog.objects.get(pk=1)
# Update all the headlines belonging to this Blog.
>>> Entry.objects.select_related().filter(blog=b).update(headline='Everything is the same')
```

要注意的是update()方法会直接转换成一个SQL语句，并立刻批量执行。

update方法不会运行模型的save()方法，或者产生`pre_save`或`post_save`信号（调用`save()`方法产生）或者服从`auto_now`字段选项。如果你想保存QuerySet中的每个条目并确保每个实例的save()方法都被调用，你不需要使用任何特殊的函数来处理。只需要迭代它们并调用save()方法：

```python
for item in my_queryset:
    item.save()
```

update方法可以配合F表达式。这对于批量更新同一模型中某个字段特别有用。例如增加Blog中每个Entry的pingback个数：

```powershell
>>> Entry.objects.all().update(number_of_pingbacks=F('number_of_pingbacks') + 1)
```



然而，与filter和exclude子句中的F()对象不同，在update中你不可以使用F()对象进行跨表操作，你只可以引用正在更新的模型的字段。如果你尝试使用F()对象引入另外一张表的字段，将抛出FieldError异常：

```shell
# 这将会导致一个FieldError异常
>>> Entry.objects.update(headline=F('blog__name'))
```

### 十、关联对象的查询

```python
# 正向查询
e.blog
# 相当于
Blog.objects.filter(entry=e)


# 反向查询
b.entry_set
# 等同于
Entry.objects.filter(blog=b)
```



#### 多对多

其实跟上面的差不多

多对多关系的两端都会自动获得访问另一端的API。这些API的工作方式与前面提到的“反向”一对多关系的用法一样。

```python
e = Entry.objects.get(id=3)

e.authors.all() # Returns all Author objects for this Entry.
e.authors.count()
e.authors.filter(name__contains='John')
#
a = Author.objects.get(id=5)
a.entry_set.all() # Returns all Entry objects for this Author.
```

与外键字段中一样，在多对多的字段中也可以指定`related_name`名。

（注：在一个模型中，如果存在多个外键或多对多的关系指向同一个外部模型，必须给他们分别加上不同的`related_name`，用于反向查询）



#### 一对一

也差不多



### 十一、关联对象的增删改

关联对象就是和外键有关的对象

- add(obj1, obj2, ...)：添加指定的模型对象到关联的对象集中。
- create(**kwargs)：创建一个新的对象，将它保存并放在关联的对象集中。返回新创建的对象。
- remove(obj1, obj2, ...)：从关联的对象集中删除指定的模型对象。
- clear()：清空关联的对象集。
- set([obj1,obj2...])：重置关联的对象集。

若要一次性给关联的对象集赋值，使用set()方法，并给它赋值一个可迭代的对象集合或者一个主键值的列表。例如：

```python
b = Blog.objects.get(id=1)
b.entry_set.set([e1, e2])
```

在这个例子中，e1和e2可以是完整的Entry实例，也可以是整数的主键值。

如果clear()方法可用，那么在将可迭代对象中的成员添加到集合中之前，将从`entry_set`中删除所有已经存在的对象。如果clear()方法不可用，那么将直接添加可迭代对象中的成员而不会删除所有已存在的对象。

这节中的每个反向操作都将立即在数据库内执行。所有的增加、创建和删除操作也将立刻自动地保存到数据库内。

下面是更多的使用案例：

```shell
# 增加
>>> b = Blog.objects.get(id=1)
>>> e = Entry.objects.get(id=2)
>>> b.entry_set.add(e) # Associates Entry e with Blog b.

# 创建
# 此时不需要调用e.save()，会自动保存
>>> e = b.entry_set.create(
...     headline='Hello',
...     body_text='Hi',
...     pub_date=datetime.date(2005, 1, 1)
... )

# 和上面相当
>>> b = Blog.objects.get(id=1)
>>> e = Entry(
...     blog=b,
...     headline='Hello',
...     body_text='Hi',
...     pub_date=datetime.date(2005, 1, 1)
... )
>>> e.save(force_insert=True)

# 删除
>>> b = Blog.objects.get(id=1)
>>> e = Entry.objects.get(id=2)
>>> b.entry_set.remove(e) # Disassociates Entry e from Blog b.

# 清空
>>> b = Blog.objects.get(id=1)
>>> b.entry_set.clear()

# 批量设置
>>> new_list = [obj1, obj2, obj3]
>>> e.related_set.set(new_list)
```

## QuerySet的API

| 方法名                | 解释                                         |
| --------------------- | -------------------------------------------- |
| **filter()**          | 过滤查询对象。                               |
| **exclude()**         | 排除满足条件的对象                           |
| **annotate()**        | 为查询集添加注解或者聚合内容                 |
| **order_by()**        | 对查询集进行排序                             |
| **reverse()**         | 反向排序                                     |
| **distinct()**        | 对查询集去重                                 |
| **values()**          | 返回包含对象具体值的字典的QuerySet           |
| **values_list()**     | 与values()类似，只是返回的是元组而不是字典。 |
| dates()               | 根据日期获取查询集                           |
| datetimes()           | 根据时间获取查询集                           |
| **none()**            | 创建空的查询集                               |
| **all()**             | 获取所有的对象                               |
| union()               | 并集                                         |
| intersection()        | 交集                                         |
| difference()          | 差集                                         |
| **select_related()**  | 附带查询关联对象，利用缓存提高效率           |
| `prefetch_related()`  | 预先查询，提高效率                           |
| extra()               | 将被废弃的方法                               |
| defer()               | 不加载指定字段，也就是排除一些列的数据       |
| only()                | 只加载指定的字段，仅选择需要的字段           |
| using()               | 选择数据库                                   |
| `select_for_update()` | 锁住选择的对象，直到事务结束。               |
| raw()                 | 接收一个原始的SQL查询                        |

## 不返回QuerySets的API

以下的方法不会返回QuerySets，但是作用非常强大，尤其是粗体显示的方法，需要背下来。

| 方法名                 | 解释                             |
| ---------------------- | -------------------------------- |
| **get()**              | 获取单个对象                     |
| **create()**           | 创建对象，无需save()             |
| **get_or_create()**    | 查询对象，如果没有找到就新建对象 |
| **update_or_create()** | 更新对象，如果没有找到就创建对象 |
| `bulk_create()`        | 批量创建对象                     |
| bulk_update()          | 批量更新对象                     |
| **count()**            | 统计对象的个数                   |
| `in_bulk()`            | 根据主键值的列表，批量返回对象   |
| `iterator()`           | 获取包含对象的迭代器             |
| **latest()**           | 获取最近的对象                   |
| **earliest()**         | 获取最早的对象                   |
| **first()**            | 获取第一个对象                   |
| **last()**             | 获取最后一个对象                 |
| **aggregate()**        | 聚合操作                         |
| **exists()**           | 判断queryset中是否有对象         |
| **update()**           | 更新对象                         |
| **delete()**           | 删除对象                         |
| as_manager()           | 获取管理器                       |
| explain()              | 对数据库操作的解释性信息         |

## aggregate()

aggregate(*args,* *kwargs)

聚合，进行数据统计，详见后面的章节。

例如，想知道所有Blog下的所有Entry 的数目：

```shell
>>> from django.db.models import Count
>>> q = Blog.objects.aggregate(Count('entry'))
{'entry__count': 16}
```

通过使用关键字参数来指定聚合函数，可以控制返回的聚合的值的名称：

```shell
>>> q = Blog.objects.aggregate(number_of_entries=Count('entry'))
{'number_of_entries': 16}
```

## 注解与聚合

类似pandas，就是数据分析和统计

首先认识两个单词：

- aggregate:  `[ˈæɡrɪɡət ]` ，聚合。做一些统计方面的工作。返回的是聚合后的数据字典
- annotate:  `[ˈænəteɪt]`，注解。为返回的查询集添加一些额外的数据。返回的依然是查询集。

```python
# 书籍的总数
>>> Book.objects.count()
2452

# BaloneyPress出版社出版的书籍总数
>>> Book.objects.filter(publisher__name='BaloneyPress').count()
73

# 所有书籍的平均价格
# 要注意！Avg，Count等聚合工具是由Django提供的，不是Python内置的，也不是你自己编写的。
>>> from django.db.models import Avg
>>> Book.objects.all().aggregate(Avg('price'))
{'price__avg': 34.35}   # 本来返回的是查询集，聚合后返回的是一个数据字典，字典的键名是有规律的

# 所有书籍中最高的价格
>>> from django.db.models import Max
>>> Book.objects.all().aggregate(Max('price'))
{'price__max': Decimal('81.20')}

# 所有书籍中最高价和平均价的差
>>> from django.db.models import FloatField
>>> Book.objects.aggregate(
...     price_diff=Max('price', output_field=FloatField()) - Avg('price'))
{'price_diff': 46.85}


# 下面是annonte注解的用法

# 每一个被过滤出来的出版社对象都被附加了一个"num_books"属性，这个属性就是所谓的注释
# 和aggregate不同，annotate返回的依然是查询集，添加了私货的查询集。
>>> from django.db.models import Count
>>> pubs = Publisher.objects.annotate(num_books=Count('book'))
>>> pubs
<QuerySet [<Publisher: BaloneyPress>, <Publisher: SalamiPress>, ...]>
>>> pubs[0].num_books
73

# 每一个出版商都被附加了两个额外的属性，分别表示好评率大于5和好评率小于等于5的书籍的总数
>>> from django.db.models import Q
# 统计每个出版社中好评率大于5的书籍的数量
>>> above_5 = Count('book', filter=Q(book__rating__gt=5))
>>> below_5 = Count('book', filter=Q(book__rating__lte=5))

# 要理解这里的链式调用含义。annotate不是filter，不会增减查询集的元素。
# 所以Publisher.objects实际上等于pubs=Publisher.objects.all()
# 第一个annotate为pubs增加below_5属性，第二个annotate又再次增加above_5属性
# 虽然是链式调用，但不是过滤行为，而是追加行为
>>> pubs = Publisher.objects.annotate(below_5=below_5).annotate(above_5=above_5)
>>> pubs[0].above_5
23
>>> pubs[0].below_5
12

# 这个比较复杂。首先获取了所有的出版社。其次统计每个出版社的发行书籍数量，保存在num_books属性中。
# 然后对所有的出版社进行排序，根据num_books属性进行反向由多到少排序，最后切片获取前5个出版社。
The top 5 publishers, in order by number of books.
>>> pubs = Publisher.objects.annotate(num_books=Count('book')).order_by('-num_books')[:5]
>>> pubs[0].num_books
1323
```



| 内置聚合函数 | 说明                                                         |
| ------------ | ------------------------------------------------------------ |
| Avg          |                                                              |
| Count        | 如果distinct=True，Count 将只计算唯一的实例。默认值为False。 |
| Max          |                                                              |
| Min          |                                                              |
| StdDev       |                                                              |
| Sum          |                                                              |
| Variance     |                                                              |

### aggregate

如果你想生成更多的聚合内容，你需要在 `aggregate()` 子句中加入其它参数即可，以逗号分隔。比如假设我们也想知道所有书中最高和最低的价格，我们可以写这样的查询：

```shell
>>> from django.db.models import Avg, Max, Min
>>> Book.objects.aggregate(Avg('price'), Max('price'), Min('price'))
{'price__avg': 34.35, 'price__max': Decimal('81.20'), 'price__min': Decimal('12.99')}
```

如果想指定名字

```shell
>>> Book.objects.aggregate(average_price=Avg('price'))
{'average_price': 34.35}
```

### annotate

```shell
# 统计每本书有多少个作者
>>> from django.db.models import Count
>>> q = Book.objects.annotate(Count('authors'))


# 查询集第一个对象
>>> q[0]
<Book: 刘江的Django教程>
>>> q[0].authors__count
1

# 查询集的第二个对象
>>> q[1]
<Book: 刘江的Python教程>
>>> q[1].authors__count
1
```

与 `aggregate()` 不同的是，`annotate()` 子句的输出依然是个 `QuerySet`，可以被链式调用；这个 `QuerySet` 可以被其他的 `QuerySet` API操作，包括 filter()`,`order_by()，甚至可以再次annotate()，如一开始的例子中所示。



组合多个聚合时，用distnct避免bug

```shell
>>> q = Book.objects.annotate(Count('authors', distinct=True), Count('store', distinct=True))
>>> q[0].authors__count
2
>>> q[0].store__count
3
```



### 连接(joins)与聚合

寻找每个书店提供的书籍价格区间

```shell
>>> from django.db.models import Max, Min
>>> Store.objects.annotate(min_price=Min('books__price'), max_price=Max('books__price'))
```



### 聚合和其他 QuerySet 子句

**filter()和exclude()**

比如统计每本，以Django开头的书籍，的作者，的数量：

```shell
>>> from django.db.models import Avg, Count
>>> Book.objects.filter(name__startswith="Django").annotate(num_authors=Count('authors'))
```



**annotate后的值也可以过滤**

```shell
>>> Book.objects.annotate(num_authors=Count('authors')).filter(num_authors__gt=1)
```



**order_by**

注解可以当做排序的一句来使用。

比如，通过书籍的作者数量来对书籍的 `QuerySet` 排序，可以使用下面的查询：

```python
>>> Book.objects.annotate(num_authors=Count('authors')).order_by('num_authors')
```