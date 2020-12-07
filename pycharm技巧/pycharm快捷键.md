https://www.cnblogs.com/liangmingshen/p/9297381.html

http://pycharm.iswbm.com/zh_CN/latest/c02/c02_03.html

使用Run -> profile '`<filename>`' 可以在运行完毕后得到相关的时间等信息。

静态代码分析检查：自动查出你的代码有没有问题。右键项目文件夹，选Inspect Code

恢复误删除文件：右键项目目录，查看local history 找到delete，右键删除的文件，可以选revert恢复。

列选择模式：右键选择column selection mode。这个可以方便地删除像下面这样的注释

```python
a = 4  # asdfasdf
b = 3  # ferett
c = 2  # davfere
```

pycharm 右下角的小锁可以锁定代码不让编辑。

ctrl+alt+space 代码补全提示

ctrl+q 快速查看文档

**ctrl+shift+i** 以内嵌代码块的形式查看源代码。

ctrl+p 快速查看函数的输入

shift+f1 打开外部文档

ctrl+alt+ ← 在按ctrl+左键查看函数调用时特别有用，可以返回到来源

alt+shift+E 执行一段代码。（这个非常有用）

ctrl+o 快速重写父类方法

ctrl+backspace 删除一个单词

ctrl+shift+v 历史剪贴板

ctrl+shift+enter 自动补全if，try 等的冒号，就是写完主要功能，不需要补上冒号就可以换行啦。

右键terminal可以查看以json格式查看输出

**alt+q** 查看上下文，就是在函数内就查看现在是在哪个函数名下，在类内就查看是属于哪个类下面的。

ctrl+alt+T 快速使用try if 等包裹当前选中的代码块



**快速封装代码**:选中要封装的代码，按ctrl+alt+M

使用 Live Template自定义自己需要的模板，已有的模板比如`main`就非常常用。

已经烂熟与心的：

ctrl+alt+L 快速调整格式(**还可以快速调整json格式**)

ctrl+b 效果等同于ctrl+鼠标左键。



显示当前类的继承树 **ctrl+H**

显示当前方法调用树 **ctrl+alt+H**

在子类方法中快速进入父类方法 ctrl+U

显示最近打开过的文件 ctrl+E

不使用鼠标，操作目录打开文件 alt+home

快速定位到错误行 F2 

跳到上一个有错误的行 shift+F2 

在函数之间上下跳转 alt+↓ / alt+↑

左右切换标签页 alt+→/ alt+← 

快速打开文件可用的工具栏 alt+f1 （可以使用这个方法，在文件夹里打开相关文件。）

跨级别跳转代码块 **ctrl+[ / ctrl+]**

FIXME 与 TODO 标记代码代办事项，查看全局TODO

快速查看最近修改的内容 alt+shift+c 

只要安装了jupyter，就能用pycharm跑：pip install jupyter

扩大/缩小选中的区域：ctrl+w / ctrl+shift+w

# 搜索技巧

## 搜索函数调用情况

alt+F7 选中函数名，然后按alt+F7，在左下角以层级的方式显示函数的调用情况。

ctrl+alt+F7 同理，但是不分层，鼠标中键也可以达到同样的效果。

ctrl+shift+F7 在当前文件中搜索，而且可以同时叠加多个搜索词。

## 使用书签

F11 打上或清除普通书签，然后使用alt+enter，选择Edit bookmark description

shift+F11 查看所有书签

ctrl+F11 可以打上数字标签，下次使用ctrl+1这样的形式就能跳转到书签所在位置。

## 精确搜索

**ctrl+F12** 打开当前文件结构

**ctrl+shift+N** 精确搜索文件

**ctrl+N** 精确搜索类名

ctrl+alt+shift+N 精确搜索符号（类的所有成员、函数、变量等）

ctrl+shift+A 精确搜索action？这个是什么意思

直接在项目树的指定文件夹打字即可搜索对应文件

ctrl+g 输入100:4 表示定位到第100行第4个字符处

## 过滤测试文件

在使用ctrl+shift+F搜索时，只要在 `File mask` 里填写 `!test*` 可以将这些test文件过滤掉。搜索结果一下子清晰很多。

# 实用插件

正则表达式测试：Regex Tester 

HTTP接口调试：Test RESTful Web Service

