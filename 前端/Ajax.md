https://www.runoob.com/ajax/ajax-tutorial.html

Asynchronous JavaScript and XML

异步更新页面，就是点击一个按钮，不需要重新打开另一个页面，直接在这个页面上请求数据库，然后渲染新的页面。

https://www.tianapi.com/注册个这个。然后可以获取上面的api



```js
<!DOCTYPE html>
<html>
<head>
    <title>Ajax请求</title>
</head>
<body>
    <button id="load">加载更多</button>
    <div id="photos"></div>
    <script src="jquery.min.js"></script>
    <script>
        // (()=>{})() 这个变态的语法表示立即执行
        function reloadImg(page) {
            // 创建异步请求对象
            let xhr = new XMLHttpRequest()
            // true表示是否发送异步请求
            xhr.open('get', url, true)
            // 绑定回调函数，当收到服务器给你的东西以后，要对页面进行局部刷新
            xhr.addEventListener('readystatechange', () => {
                // 1 表示刚刚给你发数据 2 表示正在发 4 表示发完了
                if (xhr.readyState == 4 && xhr.status==200) {
                    // 将返回的JSON字符串解析成JavaScript的对象
                    let json = JSON.parse(xhr.responseText)
                    json.newslist.forEach((element) => {
                        $('#photos').prepend()
                        let img = document.createElement('img')
                        img.src = element.picUrl
                        img.width = 300
                        const photos = document.querySelector('#photos')
                        photos.insertBefore(img, photos.firstElementChild)
                        
                    })
                } 
            })
            xhr.send()  // 发送异步请求
        }
        (() => {
            const photos = document.querySelector('#photos')
            const loadBtn = document.querySelector('#load')
            var page = 1
            loadBtn.addEventListener('click', (evt) => {
                page += 1
                url = 'http://api.tianapi.com/meinv/index?key=9654c8fc5acf0eaf8fefc7f536aaa6f1&num=5&page=' + page
                reloadImg(url)
            })
        })()

    </script>
</body>
</html>
```



jQuery版的ajax

`$.getJSON(url, () => {})`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Ajax请求</title>
</head>
<body>
    <button id="load">加载更多</button>
    <div id="photos"></div>
    <script src="jquery.min.js"></script>
    <script>
        // (()=>{})() 这个变态的语法表示立即执行
        $(() => {
            const url = 'http://api.tianapi.com/meinv/'
            var page = 0
            $('#load').on('click', (evt) => {
                page += 1
                let data = {"key":'9654c8fc5acf0eaf8fefc7f536aaa6f1', 
                            "num":4, 
                            "page":page}

                $.getJSON(url, data, (json) => {
                    json.newslist.forEach((element) => {
                        $('#photos').prepend(
                            $('<img>').attr('src', element.picUrl).attr('width', 300))
                    })
                })
            })
        })
    </script>
</body>
</html>
```

`$.ajax`这个方法是最全能的，可以处理任意请求(get post ...)。也可以接受任何类型的数据。基本上会这一个就够了

```js
$.ajax({
    // 注释表示是默认的
    // "type": "get",
    // "dataType": "json",
    // "headers": {},  // 请求头
    "url": url,
    "data": data,  // 跟在网页后面的属性
    "success": (json) => {
        json.newslist.forEach((element) => {
            $('#photos').prepend(
                $('<img>').attr('src', element.picUrl).attr('width', 300))
        })
    },
    // "error": (error) => {}
})
```

