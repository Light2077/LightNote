可以安装集成开发环境

- WebStorm
- HBuilder http://dcloud.io

`<hr>`horizontal ruler 水平标尺

ctrl + [  可以批量加标签

列表标签

有序列表 ol

无序列表 ul

定义列表 dl ：**dt** definition title **dd** definition description

### 图像标签

`<img src='https://www.python.org/static/img/python-logo@2x.png'>`

figure标签

### 链接标签

```html
<style>
a {
    color: red;
    text-decoration: None;
}
a:hover {
    color: green;
}
</style>

<a href='https://www.baidu.com' target="_blank">百度</a>
```



属性：target

### 锚点链接

怎么放锚点

怎么用锚点

怎么去别的页面的锚点

```html
<a name='top'></a>
<p>
    <a href='#top'>回顶部</a>
    <a href='hello.html#foo'>回顶部</a>
</p>
```

### 功能链接

```html
<a href='mailto:123@qq.com'>打开邮箱</a>


```

打开qq，用这个网页生成代码

http://shang.qq.com

### 表格

table

tr 行元素 有多少个这个就有多少行

td 列元素 有多少个这个就有多少列

caption标题标签

th 加粗的表头

thead，tbody，ttail 这三个只是为了代码可读性

表格的属性

- rowspan跨行
- colspan跨列
- align 对齐方式

### 表单

type="hidden" 这个可以隐藏的传一个参数

action 这个是服务器的操作。之后学了就能使用。

method 是请求post还是获取get

name是key

value是值，这个对应于单选框和复选框

required 必须要填的字段

placeholder="提示信息" 在输入框是空的时候显示提示字符

size 改长度

maxlength="20" 最大长度

readonly 只能看不能改

enctype='multipart/form-data' 表单要上传文件必须加这个

```html
<!-- 文本框 -->
<form>
First name: <input type="text" name="firstname"><br>
Last name: <input type="text" name="lastname">
</form> 

<!-- 密码框 -->
<form>
Password: <input type="password" name="pwd">
</form> 

<!-- 单选框 -->
<form>
<input type="radio" name="sex" value="male">Male<br>
<input type="radio" name="sex" value="female">Female
</form> 

<!-- 复选框 -->
<form>
<input type="checkbox" name="vehicle" value="Bike">I have a bike<br>
<input type="checkbox" name="vehicle" value="Car" checked>I have a car
</form> 

<!-- 提交按钮 -->
<form name="input" action="html_form_action.php" method="get">
Username: <input type="text" name="user">
<input type="submit" value="Submit">
</form> 

<!-- 下拉 -->
<select name="province">
    <option value="beijing">北京</option>
    <option value="shanghai">上海</option>
    <option value="chongqin">重庆</option>
    <option value="shenzhen" selected>深圳</option>
</select>

<!-- 日历 -->
<input type="date" name='birthday'>

<!-- 邮箱 -->
<input type="email" name='email'>

<!-- 文本区域，多行文本 -->
<textarea cols='30' rows='10' name='info'></textarea>

<input type='submit' value='确认注册'>
<input type='reset' value='重新填写'>


```

### 音视频标签

iframe，相当于在你的页面又打开了一个别人页面的小窗口

<iframe frameborder="no" border="0" marginwidth="0" marginheight="0" width=330 height=86 src="//music.163.com/outchain/player?type=2&id=451703279&auto=0&height=66"></iframe>

```html
<audio controls autoplay loop>
    <source src="">
</audio>

<video controls>
	<source src="">
</video>
```

### 块级元素和行级元素

行级元素不会独占整行，块级元素会换行。

块级：div / p / h1-h6 / ul / ol / dl / table 

行级元素：a / img /iframe / button / span /input ...

## 层叠样式表

css cascading style sheet

写在head标签内，负责渲染页面

### 标签选择器和类选择器

- 语法
- 标签可以同时是多个类，这样设置的多个风格可以叠加到标签上

```html
<!DOCTYPE html>
<html>
<head>
    <title>css</title>
    <style>
        /* 标签选择器 */
        h1 {
            width: 960px;
            height: 30px;
            background-color: cyan;
            margin: 0 auto;
        }
        /* 类选择器 */
        .a {
            background-color: red;
        }

        .b {
            background-color: orange;
        }
        .h {
            color: blue;
            text-align: center;
            width: 100px;
            height: 35px;
            overflow: hidden; /* scroll */
        }
        /* id选择器 */
        #header {
            width: 800px;
            border: 1px solid red;
            margin: 10px auto;
        }
        </style>
</head>
<body>
    <div id="header">
        
    </div>
    <h1></h1>
    <h1 class='a'></h1>
    <h1 class='b'></h1>
    <p class="a h">
        hello
    </p>
</body>
</html>
```

### id选择器

保证只有一个标签用这个样式

### 通配符选择器

`*`

### 外部样式表

```css
/* 标签选择器 */
h1 {
    width: 960px;
    height: 30px;
    background-color: cyan;
    margin: 0 auto;
}
/* 类选择器 */
.a {
    background-color: red;
}

.b {
    background-color: orange;
}
.h {
    color: blue;
    text-align: center;
    width: 100px;
    height: 35px;
    overflow: hidden; /* scroll */
}
/* id选择器 */
#header, #footer {
    width: 800px;
    height: 100px;
    border: 1px solid red;
    margin: 10px auto;
}
```



```html
<!DOCTYPE html>
<html>
<head>
    <title>css</title>
    <!-- 外部样式表 -->
    <link rel='stylesheet' href='style.css'>
</head>
<body>
    <div id="header">
        
    </div>
    <h1></h1>
    <h1 class='a'></h1>
    <h1 class='b'></h1>
    <p class="a h">
        hello
    </p>
</body>
</html>
```

### 内嵌样式表

直接在标签里写样式，利用style这个属性。不建议。

### 样式覆盖规则

1.就近原则

2.具体性原则：id选择器>类选择器>标签选择器

3.`.a {color: green !important;}`加了!important的优先级最高

### 文本和字体属性

letter-spacing 字符间距

line-height 行高

text-align

text-decoration: underline;

text-shadow: 2px 2px gray;

#### 字体的分类

serif 衬线字体 笔画粗细有变化，边角有修饰。字很小时不太好看

sans-serif 非衬线字体  文字粗细一致

monospace 等宽字体，字母的大小是等宽的。



#### 字体大小的单位

#### 给用户发送字体

这里的font-family的字体是随便设置的

```html
<style>
    @font-face{
        font-family: 'FatDog';
        src: url('fonts/chunkfive.ttf');
    }
</style>
```

### 字体的font属性

可以压缩代码量，一定程度上加快访问速度。

```html
<style>
    h3{
        font: italic bolder 2cm/60px "FatDog";
        /* font-size: 2cm;
        font-family: "FatDog";
        font-style: oblique; */
    }
</style>
```

### 边框(border)和轮廓(outline)

轮廓是获得焦点的时候会显示，边框是本来就显示

```html
<style>
    /* 属性选择器 */
    input[type=text], input[type=password] {
        border: none;
        outline: none;
        border-bottom: 1px solid darkgray;
    }
    /* 后代选择器 */
    /*form input[type=text]
    这样写法的意思是，只在表单内出现的input才会被应用样式*/
    
    /* 兄弟选择器 */
    /*form~input[type=text]
    这样写法的意思是，只有和form互为兄弟才会应用样式*/
    
    /* 相邻兄弟选择器 
    form+input*/
    
    /* 儿子选择器 
    form>input*/
    
    input[type=text] {
        outline:none;
        border: 1px solid lightgrey;
    }
    
    input[type=text]:focus {
        outline:none;
        border: 1px solid #00FFFF;
    }
</style>
```

### css抠图

略过了

### 盒子的显示隐藏

```css
h3 {
/*block . inline-block / none*/
    display: block; /*内容隐藏，位置不占用*/
    visibility: hidden; /*内容隐藏，位置占用*/
}

.button {
    display: inline-block;  /*行级元素改宽高要加这句*/
    background-color: red;
    color: white;
    width: 120px;
    height: 40px;
}
```

### 定位属性

```html
<!DOCTYPE html>
<html>
<head>
    <title></title>
    <style>
        #adv {
            width: 100px;
            height: 200px;
            background-color: blue;
            color: white;
        }
        /*position属性的取值
        static
        relative 相对于原来的位置
        absolute 相对于父元素
        fixed 相对于浏览器窗口
        */
    </style>
</head>
<body>
    <div id="adv">广告位招租</div>
</body>
</html>
```



### 表格边框

```css
table {
    border-collapse: collapse;
}
td, th {
    border: 1px solib black;
}
```

### 标签浮动时的问题

标签浮动时，div不会被撑开，加边框时会变成上下边框连在一起

方法1：加这一句到最底部可以清除浮动，使得边框可以撑开

`<div style='clear:both;'></div>`

方法2：容器加个属性`overflow:auto;`也能自动撑开边框

俗称css hack

### 网站经典布局

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset='utf8'>
    <title></title>
    <style>
        #page{
            width: 960px;
            margin: 0 auto;
        }
        header, footer, #main {
            margin: 10px 0;

        }
        header {
            width: 100%;
            height: 150px;
            background-color: lightgoldenrodyellow;
        }
        #main {
            height: 600px;
        }

        footer {
            height: 150px;
            background-color: lightsalmon;
        }
        #logo {
            height: 70%;
        }

        nav {
            height: 30%;
            background: lightgrey;
        }

        article {
            height: 100%;
            width: 74%;
            float: left;
            margin-right: 1%;
            background: lightpink;

        }

        aside {
            width: 25%;
            height: 100%;
            background: lightcyan;
            float: left;
        }
    </style>
</head>
<body>
    <div id="page">
        <header>
            <div id="logo"></div>
            <nav></nav>
        </header>

        <div id="main">
            <article></article>
            <aside></aside>
        </div>

        <footer></footer>
    </div>
</body>
</html>
```



## JavaScript

交互式行为，放在body标签的最后



