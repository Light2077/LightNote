

## 功能说明

点击按钮获得（1 - 100）之间的随机金币

![](E:\Github\LightNote\前端\经验书\点击按钮发送ajax\images\点击获得随机金币.gif)

项目结构

```
  |- 点击按钮发送ajax
    |- README.md
    |- app.py
    |- index.html
```

项目运行，进入到项目目录

```
flask run
```

参考：https://wangdoc.com/javascript/bom/xmlhttprequest.html

## 代码构建

先搭建一个简单的后端

`app.py`编写

```python
import random
from flask import Flask, jsonify, make_response

app = Flask(__name__)

@app.route('/')
def index():
    return 'hello!'

@app.route('/gold')
def get_gold():
    gold = random.randint(1, 100)
    return jsonify({'gold': gold})

# 解决跨域问题
@app.after_request
def func_res(resp):     
    res = make_response(resp)
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res
```

`index.html`页面编写

```html
<!DOCTYPE html>
<html>
<head>
    <title>获得随机金币</title>
    <meta charset="utf-8">
    <style>
        body {
          max-width:200px;
          margin: 0 auto;
    }
    </style>
</head>
<body>

<div>
    <p>金币：<span id="glod">0</span></p>
    <button id="goldBtn">
        点击获得随机金币
    </button>
</div>

<script type="text/javascript">
function getGold(url) {
    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function(){
        // 通信成功时，状态值为4
        if (xhr.readyState === 4){
            if (xhr.status === 200){
                // 通信成功时的操作
                let json = JSON.parse(xhr.responseText);
                const glod = document.querySelector('#glod')
                glod.innerText = json.gold;
            } else {
                console.error(xhr.statusText);
            }
        }
    };

    xhr.onerror = function (e) {
        console.error(xhr.statusText);
    };

    xhr.open('GET', 'http://127.0.0.1:5000/gold', true);
    xhr.send();
}

(() => {
    const goldBtn = document.querySelector('#goldBtn')
    goldBtn.addEventListener('click', (evt) => {
        url = 'http://127.0.0.1:5000/gold'
        getGold(url)
    })
})()
</script>
</body>
</html>
```

### ajax相关代码解释

为按钮绑定事件函数：当id为`#goldBtn`的按钮被点击时调用`getGold(url)`

```js
(() => {
    const goldBtn = document.querySelector('#goldBtn')
    goldBtn.addEventListener('click', (evt) => {
        url = 'http://127.0.0.1:5000/gold'
        getGold(url)
    })
})()
```

> `(() => {...})()`表示创建一个函数并立即执行。



`getGold()`函数才是实现ajax的核心函数。

```js
function getGold(url) {
    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function(){
        // 通信成功时，状态值为4
        if (xhr.readyState === 4){
            if (xhr.status === 200){
                // 通信成功时的操作
                let json = JSON.parse(xhr.responseText);
                const glod = document.querySelector('#glod')
                glod.innerText = json.gold;
            } else {
                console.error(xhr.statusText);
            }
        }
    };
```



创建一个XMLHttpRequest 对象

```js
let xhr = new XMLHttpRequest();
```

当接收到服务器传回的结果时调用下面的代码。

```js
xhr.onreadystatechange = function(){
    // ...
};
```

更容易让人理解的写法是

```js
xhr.onreadystatechange = handleStateChange;

function handleStateChange() {
  // ...
}
```

当通信状态`readyState`发生变化时，调用`handleStateChange`函数



当发生错误时，调用相应函数

```js
xhr.onerror = function (e) {
    console.error(xhr.statusText);
};
```

使用`open()`方法指定建立 HTTP 连接的一些细节。

```js
xhr.open('GET', 'http://127.0.0.1:5000/gold', true);
```

最后调用`send()`方法才实际发出了请求。

```js
xhr.send();
```

如果发送的是post请求，这里就要带参数。
