https://developer.mozilla.org/zh-CN/



网页写好以后，对自动生成一个网页对象，这个对象包含了所有的标签包括`htmc, head, div, p...`

这个对象是window.document。比如`window.alert('hello')`。可以在开发者工具的console里面查看window对象。

或者输入document就能查看document对象

js的匿名函数

```javascript
function () {}
```

# JS基本语法

- 外部script

  ```html
  <script src="..."></script>
  ```

- `let`定义的变量值在块级作用域生效

- 反引号字符串可以输入带占位符的字符串：

  ```javascript
  alert(`今年${n}岁了`)
  ```

- 定义常量：`const`关键字

- 整除：`parseInt(3 / 2)`不像Python中可以`3 // 2`。

- 逻辑取反：`!flag`

- 在控制台输出：`console.log('hello')`

- 查看变量类型：`typeof a`

- js中的比较运算符带了隐式类型转换，所以有`===`和`!==`表示不带类型转换的比较。

- 

### JS数据类型

- 简单数据类型：
  - string / number / boolean / undefined / symbol / null
- 其他都是复杂数据类型：object

### 分支和循环

```js
var face = parseInt(Math.random() * 3 + 1)
switch (face) {
    case 1: console.log("1"); break
    case 2: console.log("2"); break
    case 3: console.log("3"); break
    default: console.log("结束")
}
```

### 数组

https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Array

浏览器中的JS包括以下三样内容：

- ECMAScript ES6 核心语法
- BOM 浏览器对象模型 window
- DOM 文档对象模型 document

```js
const array1 = ['a', 'b', 'c'];

array1.forEach(element => console.log(element));

// expected output: "a"
// expected output: "b"
// expected output: "c"
```



### 函数

可以有默认值，用法跟python一样。

```js
// 匿名函数
// 以下三个函数等价
function sub(x, y) {
    return x - y
}

function (x, y) { return x - y}

(x, y) => x - y
```

### 类

老js定义类的方法，构造器法。

```html
<!DOCTYPE html>
<html>
<head>
    <title></title>
</head>
<body>
 <script type="text/javascript">
    // 老版js定义类的方式
    function Person(name, age) {
       this.name = name
       this.age = age
    }
    Person.prototype.eat = function(food) {
        alert(this.name + '正在吃' + food)
    }
    Person.prototype.watch = function() {
        if (this.age < 18) {
            alert(this.name + '在看动画片')
        } else {
            alert(this.name + '在看电影')
        }
    }
    person1 = new Person('tom', 30)
    person2 = new Person('lily', 15)

    person1.eat("面包")
    person2.watch()


 </script>
</body>
</html>
```

新语法定义类

```html
<!DOCTYPE html>
<html>
<head>
    <title></title>
</head>
<body>
 <script type="text/javascript">
    // 新版js定义类的方式
    class Person {
        constructor(name, age) {
            this.name = name
            this.age = age
        }
        eat(food) {
            alert(`${this.name}正在吃${food}`)
        }
        watch() {
            if (this.age < 18) {
                alert(`${this.name}在看动画片`)
            } else {
                alert(`${this.name}在看电影`)
            }
        }
    }
    person1 = new Person('tom', 30)
    person2 = new Person('lily', 15)

    person1.eat("面包")
    person2.watch()
 </script>
</body>
</html>
```

### 回调函数

绑定事件时传入的函数通常我们称之为回调函数，当浏览器执行该回调函数时，会传入一个代表事件的对象，通过event事件对象拿到触发事件的对象。知道事件发生时要做什么，但不知道事件什么时候发生。

回调函数就是，别人写好了一大堆代码，你想自定义一部分代码，你就写个函数，然后就会在某个时刻调用这段代码。

一栋大楼，你想自定义一个灯，你就把灯的颜色，大小什么的制定好。然后做两个方法，一个是开灯一个是关灯，然后把灯挂到指定位置，别人在用这栋楼的时候就会自己开灯关灯，你不需要了解这栋楼的电路构造。

### 代码调试

切换到sources界面

点击行号就可以插入断点。旁边的

![image-20200815125032535](image-20200815125032535.png)

可以执行调试任务，顶部是操作下一步的按钮

# 页面操作

## 获取标签

```js
const divList = document.getElementsByTagName('div')
document.getElementById('id')
document.getElementsByClassName('Person')
document.getElementsByName('boy')  //  标签里边有个name属性
// 这样拿到的是一个文本，div标签紧跟着换行了。
document.getElementById('divid').firstChild
document.getElementById('divid').lastChild
document.getElementById('divid').parentNode
document.getElementById('divid').previousSibling
document.getElementById('divid').previousElementSibling  // 不会取到文本节点
document.getElementById('divid').nextElementSibling

document.getElementById('id').children[0]

document.querySelector('#adv>img')  // 拿到第一个儿子
document.querySelector('#adv img')  // 拿到第一个后代
document.querySelector('#adv+img')  // 拿到第一个后代
document.querySelector('#adv-img')  // 拿到第一个后代

document.querySelectorAll('#adv>img')  // 拿所有的

textContent / innerHTML
// 修改属性直接.属性
imagc.src / img.title / img.style / checkbox.checked
```



# 例子

## 1. 广告关闭

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset='utf8'>
    <title></title>
    <style>
        #adv {
            width: 120px;
            height: 200px;
            background: blue;
            color: white;
            position: fixed;
        }
    </style>
</head>
<body>
    <div id="adv"> 我是广告 
        <button id="closeBtn" style="float: right;">关闭</button>
    </div>
    <script type="text/javascript">
        var btn = document.getElementById('closeBtn')
        btn.addEventListener('click', function () {
            adv = document.getElementById('adv')
            adv.style.display = 'none';
        })
    </script>
</body>
</html>
```

## 2. 判断闰年

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset='utf8'>
    <title></title>
</head>
<body>
    <script type="text/javascript">
        var yearStr = prompt('请输入年份')
        var year = parseInt(yearStr)

        if (year == yearStr && year > 0){
            let isLeap = ((year % 4 == 0 && year % 100 != 0) || year % 400 == 0 )
            let yearOrNo = isLeap? "是" : "不是"
            alert(`${year}年${yearOrNo}闰年`)
        } else {
            alert('请输入有效年份')
        }
    </script>
</body>
</html>
```



## 3. 双色球

数组，函数

```html
<!DOCTYPE html>
<html>
<head>
    <title></title>
    <style type="text/css">
        p {
            width: 100px;
            height: 100px;
            color: white;
            font: 60px/100px Arial;
            border-radius: 50px;
            text-align: center;
            float: left;
            margin-left:10px;
        }
        .red {
            background: red;
        }

        .blue {
            background: blue;
        }

    </style>
</head>
<body>

<script>
    function outputBall(num, color) {
        document.write(`<p class=${color}>`) 
        if (num < 10) {
            document.write('0')
        }
        document.write(num)
        document.write('</p>')
    }

    var redBalls = []
    for (let i = 0; i < 33; i += 1) {
        redBalls.push(i + 1)
    }
    var selectedBalls = []
    for (let i = 1; i < 6; i += 1) {
        // 产生一个随机的下标
        let index = parseInt(Math.random() * redBalls.length);
        selectedBalls.push(redBalls[index])
        // 删除数组中指定位置的元素
        redBalls.splice(index, 1)
    }
    // 给红色球排序（默认按照字符排序）
    // function (x, y) { return x - y}
    selectedBalls.sort((x, y) => x - y)
    for (let i = 0; i < selectedBalls.length; i += 1) {
        let num = selectedBalls[i]
        outputBall(num, 'red')
    }
    let num = parseInt(Math.random() * 16 + 1)
    outputBall(num, 'blue')

</script>
</body>
</html>
```

## 4. 显示时钟

```html
<!DOCTYPE html>
<html>
<head>
    <title></title>
    <style type="text/css">
        #clock {
            width: 800px;
            height: 100px;
            background: lightgreen;
            color: white;
            font: 50px/100px Arial;
        }

    </style>
</head>
<body>
    <div id="clock">asdf</div>

    <script type="text/javascript">
        const clockDiv = document.getElementById('clock')

        const weekdays = ['日', '一', '二', '三', '四', '五', '六']
        function showClock() {
            let now = new Date()
            let year = now.getFullYear()
            let month = now.getMonth() + 1

            let date = now.getDate()
            let hour = now.getHours()
            let min = now.getMinutes()
            let sec = now.getSeconds()
            let day = now.getDay()
            let fullStr = `${year}年${month}月${date}日 ${hour}:${min}:${sec} 星期${weekdays[day]}`
            clockDiv.textContent = fullStr
        }
        window.setInterval(showClock, 1000)
        // alert(fullStr)
    </script>
</body>
</html>
```

## 5.图片轮播

每隔1s换一次图片，鼠标停在图片上时不切换图片。

```html
<!DOCTYPE html>
<html>
<head>
    <title></title>
    <style type="text/css">
        #adv {
            width: 600px;
            margin: 0 auto;
        }

    </style>
</head>
<body>
    <div id='adv'>
        <img src="http://img0.dili360.com/ga/M01/00/A2/wKgBzFQ2cqSAA6XGAAd6xaSf9g4136.jpg@!rw17" width="600" alt="">

    </div>

    <script>
        const imgaeNames = ['http://img0.dili360.com/ga/M01/00/A2/wKgBzFQ2cqSAA6XGAAd6xaSf9g4136.jpg@!rw17',
                            'http://img0.dili360.com/ga/M00/00/A2/wKgBy1Q2cqGANTq2AAIUiM2biLA392.jpg@!rw17',
                            'http://img0.dili360.com/ga/M00/00/A2/wKgBzFQ2cpuAdptiAAEM8vS1CXU167.jpg@!rw17',
                            'http://img0.dili360.com/ga/M01/00/A2/wKgBzFQ2cpeAI9DNAAJJts0YbWM407.jpg@!rw17']
        var imageIndex = 0
        const img = document.querySelector('#adv>img')
        function switchImage() {
            imageIndex += 1
            imageIndex %= imgaeNames.length
            img.src = imgaeNames[imageIndex]
        }
        var timerId = setInterval(switchImage, 1000)

        img.addEventListener('mouseover', () => clearInterval(timerId))
        img.addEventListener('mouseout', () => timerId = setInterval(switchImage, 1000))
    </script>
</body>
</html>
```

## 6. 按钮变色

```html
<!DOCTYPE html>
<html>
<head>
    <title></title>
</head>
<body>
    <div id="buttons">
        <button><input type="checkbox" disabled>苹果</button>
        <button><input type="checkbox" disabled>香蕉</button>
        <button><input type="checkbox" disabled>草莓</button>
        <button><input type="checkbox" disabled>蓝莓</button>
        <button><input type="checkbox" disabled>榴莲</button>
        <button><input type="checkbox" disabled>西瓜</button>
        <button><input type="checkbox" disabled>芒果</button>
        <button><input type="checkbox" disabled>柠檬</button>
        
    </div>
    <script>
        const allButtons = document.querySelectorAll('#buttons>button')
        for (let i = 0; i < allButtons.length; i += 1) {
            // allButtons[i].addEventListener('click', () => {
            //     let checkbox = allButtons[i].firstChild
            //     checkbox.checked = !checkbox.checked
            //     allButtons[i].style.background = checkbox.checked? 'lightgreen': 'lightpink'
            // })

            // 老版的做法，没有let的时候只能用var时会出现bug
            // 绑定事件时传入的函数通常我们称之为回调函数
            // 当浏览器执行该回调函数时，会传入一个代表事件的对象
            // 通过event事件对象拿到触发事件的对象

            allButtons[i].addEventListener('click', (event) => {
                var checkbox = event.target.firstChild
                checkbox.checked = !checkbox.checked
                event.target.style.background = checkbox.checked? 'lightgreen': 'lightpink'
            })
        }
    </script>
</body>
</html>
```

## 7.添加删除元素

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
    <script>
        const ul = document.querySelector("#fruits")
        var anchors = document.querySelectorAll('#fruits a')
        // alert(anchors.forEach)
        // anchors.forEach((delAnchor) => {
        //     delAnchor.addEventListener('click', () => {
        //         ul.removeChild(delAnchor.parentNode)
        //     })
        // })

        // 一种不需要 javascript:void(0) 的方法
        anchors.forEach((delAnchor) => {
            delAnchor.addEventListener('click', (evt) => {
                evt.preventDefault() // 阻止事件的默认行为
                ul.removeChild(delAnchor.parentNode)
            })
        })

        // 新增标签
        const input = document.querySelector('#fruits+input')
        input.addEventListener('keypress', (evt) => {
            let code = evt.keyCode || evt.which
            if (code == 13) {
                addFruit(evt)
            }
        })
        const ok = document.querySelector('#ok')
        
        function addFruit(evt) {
            let name = input.value.trim()
            if (name.length > 0) {
                // 创建新标签
                let li = document.createElement('li')
                li.innerHTML = name
                // 把儿子加到父标签最后
                // ul.appendChild(li)
                let delAnchor = document.createElement('a')
                delAnchor.textContent = 'x'
                delAnchor.addEventListener('click', (evt) => {
                evt.preventDefault() // 阻止事件的默认行为
                ul.removeChild(delAnchor.parentNode)})

                li.appendChild(delAnchor)
                // 将子标签加到指定位置
                ul.insertBefore(li, ul.firstChlid)
                input.value = ''
                // 让标签获得焦点
                // input.blur() 失去焦点
                input.focus()
            }
        }
        ok.addEventListener('click', addFruit)
    </script>
</body>
</html>
```

