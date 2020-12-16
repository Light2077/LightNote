# [第四章：Django表单](https://www.liujiangblog.com/course/django/151)

## 一、HTML表单概述

Django开发的是动态Web服务，而非单纯提供静态页面。动态服务的本质在于和用户进行互动，接收用户的输入，根据输入的不同，返回不同的内容给用户。返回数据是我们服务器后端做的，而接收用户输入就需要靠HTML表单。表单`<form>...</form>`可以收集其内部标签中的用户输入，然后将数据发送到服务端。

一个HTML表单必须指定两样东西：

- 目的地：用户数据发送的目的URL
- 方式：发送数据所使用的HTTP方法

例如，Django Admin站点的登录表单包含几个`<input>`元素：`type="text"`用于用户名，`type="password"`用于密码，`type="submit"`用于“登录"按钮。它还包含一些用户看不到的隐藏的文本字段，Django 使用它们来提高安全性和决定下一步的行为。它还告诉浏览器表单数据应该发往`<form>`的action属性指定的URL:`/admin/`，而且应该使用method属性指定的HTTP post方法发送数据。当点击`<input type="submit" value="Log in">`元素时，数据将发送给`/admin/`。

其HTML源码如下：

```html
<form action="/admin/login/?next=/admin/" method="post" id="login-form">

    <input type='hidden' name='csrfmiddlewaretoken'              value='NNHZaDVJGduajNMECXygKZkAt8vyEcw9HS2qm2Vdf7brDZrA0qK1R0I7M2p3TKcs' />

    <div class="form-row">
        <label class="required" for="id_username">用户名:</label> 
        <input type="text" name="username" autofocus maxlength="254" required id="id_username" />
    </div>

    <div class="form-row">
        <label class="required" for="id_password">密码:</label> 
        <input type="password" name="password" required id="id_password" />
        <input type="hidden" name="next" value="/admin/" />
    </div>

    <div class="submit-row">
        <label>&nbsp;</label><input type="submit" value="登录" />
    </div>
</form>
```

**GET和POST** ：

处理表单时候只会用到POST和GET方法。

GET方法将用户数据以`键=值`的形式，以‘&’符号组合在一起成为一个整体字符串，最后添加前缀“？”，将字符串拼接到url内，生成一个类似`https://docs.djangoproject.com/search/?q=forms&release=1`的URL。

而对于POST方法，浏览器会组合表单数据、对它们进行编码，然后打包将它们发送到服务器，数据不会出现在url中。

GET方法通常用来请求数据，不适合密码表单这一类保密信息的发送，也不适合数据量大的表单和二进制数据。对于这些类型的数据，应该使用POST方法。但是，GET特别适合网页搜索的表单，因为这种表示一个GET请求的URL可以很容易地设置书签、分享和重新提交。

## 二、 Django的form表单

通常情况下，我们需要自己手动在HTML页面中，编写form标签和其内的其它元素。但这费时费力，而且有可能写得不太恰当，数据验证也比较麻烦。有鉴于此，Django在内部集成了一个表单模块，专门帮助我们快速处理表单相关的内容。Django的表单模块给我们提供了下面三个主要功能：

- 准备和重构数据用于页面渲染
- 为数据创建HTML表单元素
- 接收和处理用户从表单发送过来的数据

编写Django的form表单，非常类似我们在模型系统里编写一个模型。在模型中，一个字段代表数据表的一列，而form表单中的一个字段代表`<form>`中的一个`<input>`元素。