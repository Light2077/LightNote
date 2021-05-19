# selenium配置

https://selenium-python-zh.readthedocs.io/en/latest/		

**安装selenium**

```
pip install selenium
```

**安装chromedriver**

chromedriver的版本要与chrome的版本一致

下载地址：

- http://chromedriver.storage.googleapis.com/index.html
- https://npm.taobao.org/mirrors/chromedriver/

查看chrome版本：在浏览器输入：

```
chrome://version
```

```
# 我查到的是
88.0.4324.146
```

谷歌浏览器驱动程序和浏览器的映射关系：

https://blog.csdn.net/huilan_same/article/details/51896672

解压缩，把`chromedriver.exe`复制到chrome的安装目录（复制到任意目录都行）

我是放到了：`C:\Program Files\Google\Chrome\Application\chromedriver.exe`

可以把这个文件所在的文件夹加到环境变量，就不需要每次都写一遍

**测试**

```python
from selenium import webdriver

driver = webdriver.Chrome('C:\Program Files\Google\Chrome\Application\chromedriver.exe')
driver.get('http://www.baidu.com')
# 关闭流量器
# dri
```

# 操作

## 元素定位

### 获取页面源码

```
html = driver.page_source
```



### 根据id

```
driver.find_element_by_id()
```

### 根据名称

```
driver.find_element_by_name()
```

### 根据xpath

```
driver.find_element_by_xpath()
```

### 根据tag name

```
driver.find_element_by_tag_name()
```

### 根据class

```
driver.find_element_by_class_name()
```

如果类名有空格，比如`<p class="show para">`

```
driver.find_element_by_class_name('.show.para')
```



### 根据CSS选择器

```
driver.find_element_by_css_selector()
```

### 根据link text

```
driver.find_element_by_link_text()
```

## 访问元素信息

### 获取元素属性

```
.get_attribute('class')
```

### 获取元素文本

```
.text
```

### 获取id

```
.id
```

### 获取标签名

```
.tag_name
```

## 交互

### 点击

```
click()
```

### 输入

```
send_keys()
```

### 模拟JS滚动

获取当前页面滚动条纵坐标的位置：

```
document.documentElement.scrollTop
```

获取当前页面滚动条横坐标的位置：

```
document.documentElement.scrollLeft
```

编写JS代码

```	
var q = window.document.documentElement.scrollTop=10000
```

执行js代码

```python
js = 'var q = document.documentElement.scrollTop=10000'

driver.execute_script(js)

time.sleep(3)
```

模拟今日头条滚动例子

```python
# 滚动自动加载信息

from selenium import webdriver
import time

path = 'phantomjs.exe'
driver = webdriver.PhantomJS(path)
url = 'https://www.toutiao.com/'
driver.get(url)
time.sleep(2)
driver.save_screenshot('1.png')
js = 'document.body.scrollTop=10000'
driver.execute_script(js)
time.sleep(2)
driver.save_screenshot('2.png')
driver.quit()
```

## 获取网页源代码

```
driver.page_source
```

## 退出

```python
driver.quit()
```



# 其他

## class name 有空格怎么处理

将空格用 `.` 来代替即可

## 页面异步ajax的解决方法

原因： 由于网页中有ajax的异步执行的js代码,

执行driver.get()时，可能有些ajax还没加载完

导致driver.get()查找元素报 NoSuchElementException异常

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC
```

解决：等待某一个Element出现为止，否则一直阻塞下去，不过可以设置一个超时时间

```python
 ui.WebDriverWait(driver, 60).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, 'soupager')))
```

等待这个元素出现，get()才结束

## switch的用法

原因：

- 页面中出现对话框 alert或内嵌窗口 iframe
- 使得爬虫过程中无法拿到需要的元素
- 如果查找的元素节点在alert 或 iframe中的话，则需要切入到alert或iframe中

解决：

```python
# 1. 查找iframe标签对象
iframe = driver.find_element_by_id('login_frame')

# 2. 切换到iframe中
driver.switch_to.frame(iframe)
```

## 获取浏览器的页签

```python
# 第一个页签，一般都存在
driver.window_handlers[0]

# 如果不存在第二个页签会报错
driver.window_handlers[1]
```

# 例子

- http://www.baidu.com
- 股票信息提取：http://quote.stockstar.com/
- 腾讯公司招聘需求：https://hr.tencent.com/index.php

## 第一个例子

```python
import time
from selenium import webdriver

driver = webdriver.Chrome('C:\Program Files\Google\Chrome\Application\chromedriver.exe')
driver.get('https://www.baidu.com')
```

### 查找输入框输入内容

接着第一个例子输入

```python
input_search = driver.find_element_by_class_name('s_ipt')
input_search.send_keys('python')
```

### 查找并点击按钮

```python
btn = driver.find_element_by_css_selector('.bg.s_btn')
btn.click()
```

### 等待所需元素出现

（非必须）

有时候网络原因，可能你点了搜索按钮，结果一时半会没那么快出来。这时候需要等待搜索结果的出现

PS: 如果类名有空格，建议不要用`By.CLASS_NAME`

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions

ui.WebDriverWait(driver, 10).until(
    expected_conditions.visibility_of_element_located(
        (By.CSS_SELECTOR, '.result.c-container.new-pmd')
    ),
    "查找的元素一直没有出现"
)
```

### 提取搜索信息

```python

```



### 滚动

（非必须：遇到那种滚动加载新内容的页面时可以用）

这个5000表示移动到从顶部开始的第5000这个位置

```python
script = 'var q = document.documentElement.scrollTop=5000;'
driver.execute_script(script)
```

### 完整代码

```python
import time
from selenium import webdriver

driver = webdriver.Chrome('C:\Program Files\Google\Chrome\Application\chromedriver.exe')
driver.get('https://www.baidu.com')

time.sleep(2)
# 给搜索框填东西
input_search = driver.find_element_by_class_name('s_ipt')
input_search.send_keys('python')

time.sleep(2)
# 点击搜索按钮
btn = driver.find_element_by_css_selector('.bg.s_btn')
btn.click()

time.sleep(2)
# 提取搜索内容
divs = driver.find_elements_by_css_selector('.result.c-container.new-pmd')

res = list()
for d in divs:
    a = d.find_element_by_tag_name('a')
    title = a.text
    url = a.get_attribute('href')
    abstract = d.find_element_by_class_name('c-abstract').text
    res.append((title, url, abstract))

```

## 模拟淘宝搜索

- 打开淘宝网
- 在搜索框中输入“python”
- 点击搜索

研究流程：F12打开抓包工具

找到搜索框，发现搜索框的两个属性

- class: search-combobox-input
- id: q

```python
import time
from selenium import webdriver

driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')

driver.get("https://www.taobao.com")
time.sleep(1)
search_input = driver.find_element_by_id("q")
# 文本框输入内容
search_input.send_keys("python")
# 点击搜索按钮

time.sleep(1)
search_btn = driver.find_element_by_class_name("btn-search.tb-bg")
search_btn.click()
```



## 爬取百度招聘网

学到的知识点：

- 利用xpath找到父节点
  - `'./..'`
- 利用xpath找到兄弟结点
  - `'./following-sibling::div[1]'` 下一个结点
  - `'./preceding-sibling::div[1]'` 前一个结点

爬取多次以后，需要登录才能继续进行

```python
import json
import time
from selenium import webdriver

# 如果将driver的路径配置到环境变量则无需传参
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome(
    'C:\Program Files\Google\Chrome\Application\chromedriver.exe')
driver.get('http://zhaopin.baidu.com/?query=&city=%E5%8C%97%E4%BA%AC')

time.sleep(2)
# 给搜索框填东西
# input_search = driver.find_element_by_css_selector('.ipt-search.search-form-ele')
input_search = driver.find_element_by_css_selector('input[name="query"]')
input_search.send_keys('python')

time.sleep(2)
input_search.send_keys(Keys.ENTER)

time.sleep(2)
script = 'var q = document.documentElement.scrollTop=5000;'
driver.execute_script(script)

time.sleep(2)
divs = driver.find_elements_by_css_selector('.inlineblock.percent47')

res = list()
for d in divs:
    # d 的下一个结点
    d2 = d.find_element_by_xpath('./following-sibling::div[1]')

    # d 的父节点
    parent = d.find_element_by_xpath('./..')
    info = json.loads(parent.get_attribute('data-click'))
    url = info['url']

    title = d.find_element_by_class_name('title').text
    salary = d.find_element_by_css_selector('.inlineblock.num').text

    company = d2.find_element_by_css_selector('.inlineblock.companyname').text
    res.append((url, title, salary, company))
```



