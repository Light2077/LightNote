# Vim

![img](images/vi-vim-cheat-sheet-sch.gif)

## 命令模式

默认进入vim后就是这个模式

| 命令            | 说明                             |
| --------------- | -------------------------------- |
| `shift + z + z` | 保存并退出                       |
| `dd`            | 删除一行                         |
| `ndd`           | 删除n行（依次按下4dd)就是删除4行 |
| `u`             | 撤销                             |
| `yy`            | 复制一行                         |
| 数字+`yy`       | 复制n行                          |
| `p`             | 粘贴                             |
| `G`             | 定位到最后一行                   |
| `gg`            | 定位到第一行                     |
| 数字+`gg`       | 定位到第n行                      |
| `x`             | 删除光标右边第一个字符           |
| 数字+`x`        | 删除光标右边第n个字符            |
| `X`             | 删除光标左边第一个字符           |
| 数字+`X`        | 删除光标右边第n个字符            |
| `$`             | 定位到行尾                       |
| `0`或`^`        | 定位到行首                       |
| `ctrl + f`      | 往下翻页                         |
| `ctrl + b`      | 往上翻页                         |
| `ctrl + d`      | 往下翻半页                       |
| `ctrl + u`      | 往上翻半页                       |
| `ctrl + r`      | 反撤销                           |
| n               | 查找时，查找下一个               |
| N               | 查找时，查找上一个               |

v + 上下左右可以选中单词

## 插入模式

在命令模式的情况下，按某个键进入插入模式

| 命令 | 说明                   |
| ---- | ---------------------- |
| `i`  | 在当前光标进入         |
| `I`  | 在第一个非空字符进入   |
| `o`  | 在下一行插入           |
| `O`  | 在上一行               |
| `s`  | 删除光标所在文件，插入 |
| `S`  | 删除整行，插入         |
| `a`  | 在光标下一个字符前插入 |
| `A`  | 在行尾插入             |

## 编辑模式

按esc返回命令模式

| 命令                   | 说明                           |
| ---------------------- | ------------------------------ |
| `:wq`                  | 保存退出                       |
| `:q!`                  | 不保存退出                     |
| `:e!`                  | 放弃之前的修改                 |
| `:set nu`              | 显示行号                       |
| `:set nonu`            | 不显示行号                     |
| `:120`                 | 跳转到第120行                  |
| `:/student`            | 搜索，按`n`搜索下一个          |
| `:w <new file name>`   | 另存为                         |
| `:set tabstop=4`       | 设置tab键缩进                  |
| `:set mouse=a`         | 打开鼠标模式                   |
| `:%s/student/学生`     | 默认一行只替换第一个匹配的内容 |
| `:%s/student/学生/g`   | 全部替换                       |
| `:m.ns/student/学生/g` | 替换第m-n行的字符串            |



`vim test.txt +20` 光标在第20行，打开
`vim test2.txt` 如果`test2.txt`不存在，则会新建

正在编辑文件时，另一个终端打开该文件。会出现交换文件比如:

`.test.py.swp`。关闭vim时，该文件自动删除



## 其他

**vim 中批量添加注释**

方法一 ：块选择模式

批量注释：

Ctrl + v 进入块选择模式，然后移动光标选中你要注释的行，再按大写的 **I** 进入行首插入模式输入注释符号如 **//** 或 **#**，输入完毕之后，按两下 **ESC**，**Vim** 会自动将你选中的所有行首都加上注释，保存退出完成注释。

取消注释：

Ctrl + v  进入块选择模式，选中你要删除的行首的注释符号，注意 **//** 要选中两个，选好之后按 **d** 即可删除注释，**ESC** 保存退出。

[复制粘贴剪切](https://blog.csdn.net/qidi_huang/article/details/52179279)

### 常用复制

【复制】

  \1. 常用复制命令：

​    **yy**   复制游标所在行整行 
​    **2yy**或**y2y**   复制 2 行
​    **y^**   复制至行首，或y0
​    **y$**   复制至行尾
​    **yw**   复制一个word
​    **y2w**   复制两个word 
​    **yG**   复制至文件尾
​    **y1G**   复制至文件首

  \2. 选中文本进行复制：

​    要选中内容进行复制，先在命令模式下按 v 进入 Visual Mode，然后用方向键 或 hjkl 选择文本，再按 y 进行复制。

【剪切】

  \1. 常用剪切命令： 

​    **dd**   剪切游标所在行整行 
​    **d^**   剪切至行首，或d0
​    **d$**   剪切至行尾 
​    **dw**   剪切一个word 
​    **dG**   剪切至文件尾 

  \2. 选中文本进行剪切：

​    要选中内容进行复制，先在命令模式下按 v 进入 Visual Mode，然后用 方向键 或 hjkl 选择文本，再按 d 进行剪切。



【粘贴】

  \1. 常用粘贴命令：

​    **p**   粘贴至游标后（下） 
​    **P**  粘贴至游标前（上）

  \2. 要使用 系统粘贴板 的内容，也可以直接在命令模式按 Shift + Inset 进行粘贴。

## 复习

跳转至行首/行尾

上下翻页，上下翻半页

在当前光标插入，在当前光标下一个字符插入，在下一行插入，在上一行插入

查找，查找下一个，查找上一个

替换一行的第一个匹配到的字符串，替换n到m行，替换全部

删除1行、删除n行

复制1行、复制n行

粘贴1行、粘贴n行

