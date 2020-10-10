https://jquery.com

https://www.bootcdn.cn

[中文文档](https://jquery.cuishifeng.cn/)

使用压缩后的版本jquery.min.js



引入jquery的方式

下载下来然后引用

```html
<script src="jquery.min.js"></script>
```

通过cdn服务器（推荐）

```html
<script src="https://cdn.bootcdn.net/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
```

`() => x+y`这个语法如果后面不接花括号，就表示返回值是`x+y`。也可以`() => { return x+y }`

$函数的四种用法：

- 函数的参数是匿名函数或箭头函数：传入的函数是页面加载完成后要执行的回调函数。
- 参数是样式表选择器，获取页面元素得到一个jQuery对象。是一个伪数组，数组中装的是原生JS对象
- 参数是标签字符串：创建一个标签并获得对应的jQuery对象
- 参数是原生的JS对象，把增对象转成jQuery对象

```js
$(() => {
    
})

$('#fruits>li>a')

$('<li>')

$(evt.target)
```



`$`是jquery的一个重要的对象

## 1. 表格效果操作

```html
<!DOCTYPE html>
<html>
<head>
    <title></title>
    <style>
        #data{
            margin:0 auto;
        }
        #buttons {
            margin:0 auto;
            width: 300px;
        }
        table {
            border-collapse: collapse;
        }
        td, th {
            border: 1px solid black;
            height: 40px;
            width: 80px;
            text-align: center;
        }
    </style>
</head>
<body>
    <table id="data">
        <caption>数据统计表</caption>
        <thead>
            <tr>
                <th>姓名</th>
                <th>年龄</th>
                <th>性别</th>
                <th>身高</th>
                <th>体重</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Item1</td>
                <td>Item2</td>
                <td>Item3</td>
                <td>Item4</td>
                <td>Item5</td>
            </tr>
            <tr>
                <td>Item1</td>
                <td>Item2</td>
                <td>Item3</td>
                <td>Item4</td>
                <td>Item5</td>
            </tr>
            <tr>
                <td>Item1</td>
                <td>Item2</td>
                <td>Item3</td>
                <td>Item4</td>
                <td>Item5</td>
            </tr>
            <tr>
                <td>Item1</td>
                <td>Item2</td>
                <td>Item3</td>
                <td>Item4</td>
                <td>Item5</td>
            </tr>
            <tr>
                <td>Item1</td>
                <td>Item2</td>
                <td>Item3</td>
                <td>Item4</td>
                <td>Item5</td>
            </tr>
            <tr>
                <td>Item1</td>
                <td>Item2</td>
                <td>Item3</td>
                <td>Item4</td>
                <td>Item5</td>
            </tr>
        </tbody>
    </table>
    <div id="buttons">
        <button id="pretty">隔行换色</button>
        <button id="clear">清除数据</button>
        <button id="remove">删除一行</button>
        <button id="hide">表格淡出</button>
    </div>

<script src="https://cdn.bootcdn.net/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script>
    // $ 对象封装了很多对象
    // $() 相当于document.querySelectorAll()
    // on 相当于 addEventListener

    // $('#pretty').off() 移除事件
    // $('#pretty').one() 只监听一次
    $('#pretty').on('click', () => {
        
        // 选择器加冒号是过滤器: even 偶数 odd 奇数 

        // css只传一个参数表示读样式
        $('#data>tbody>tr:odd').css('background', 'lightblue')
        $('#data>tbody>tr:even').css('background', 'lightgreen')
    })
    $('#clear').on('click', () => {
        $('#data>tbody>tr>td').empty()
    })
    $('#remove').on('click', () => {
        $('#data>tbody>tr:last-child').remove()
    })
    $('#hide').on('click', () => {
        let title = $('#hide').text()
        if (title == '表格淡出') {
            $('#data').fadeOut(1000, () => {
                $('#hide').text('表格淡入')
            })
        } else {
            $('#data').fadeIn(1000, () => {
                $('#hide').text('表格淡出')
            })
        }
    })

</script>
</body>
</html>
```

## 2.增加删除进阶

```html
<!DOCTYPE html>
<html>
<head>
    <title></title>
    <style>
        * {
            margin: 0;
            padding: 0;
        }

        #container {
            margin: 20px 50px;
        }
        #fruits>li {
            list-style: none;
            width: 200px;
            height: 50px;
            font-size: 20px;
            line-height: 50px;
            background: cadetblue;
            color: white;
            text-align: center;
            margin: 2px 0;
        }
        #fruits>li>a {
            float: right;
            text-decoration: none;
            color: white;
            position: relative;
            right: 5px;
        }
        #fruits~input {
            border: none;
            outline: none;
            font-size: 18px;
        }
        #fruits~input[type=button] {
            width: 80px;
            height: 30px;
            background: coral;
            color: white;
            vertical-align: bottom;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div id="container">
        <ul id="fruits">
            <!-- 空字符串会刷新当前页面 -->
            <!-- javascript:void(0)阻止默认操作 -->
            <li>苹果<a href="javascript:void(0)" >x</a></li>
            <li>香蕉<a href="javascript:void(0)">x</a></li>
            <li>火龙果<a href="javascript:void(0)">x</a></li>
            <li>西瓜<a href="javascript:void(0)">x</a></li>

        </ul>
        <input type="text" name="fruits">
        <input id="ok" type="button" value="确定">
    </div>
    <script src="https://cdn.bootcdn.net/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script>
        function removeListItem(evt) {
            // evt.stopPropagation  阻止事件的传播行为
            evt.preventDefault()
            // 加$符号会拿到jquery对象的标签
            $(evt.target).parent().remove()
        }

        function addFruit(evt) {
            let input = $('#ok').prev()
            let name = input.val().trim()
            if (name) {
                $('#fruits').append(
                    $('<li>').text(name).append(
                        $('<a href="">').html('&times;').on('click', removeListItem)
                        )
                    )
                input.val('').get(0).focus()
            }
        }
        // 避免全局变量的几种方式，以下都是页面加载完后执行
        // window.addEventListener('load', () => {})
        // +function() {}()
        // $(document).ready(function() {})
        // $(function() {})
        $(() => {
            $('#fruits>li>a').on('click', removeListItem)
            $('#ok').on('click', addFruit)
            $(document).keyup((evt) => {
                let code = evt.keyCode || evt.which
                if (code == 13) {
                    addFruit(evt)
                }
            })
        })
    </script>
</body>
</html>
```

