https://tangxing.blog.csdn.net/article/details/108418066

https://blog.csdn.net/jayandchuxu/article/details/107929198

https://blog.csdn.net/weixin_42759134/article/details/81148571





https://zhuanlan.zhihu.com/p/67543981

介绍win32com较好的文章，简单的操作可以用python-docx解决，复杂的操作需要借助这个包

什么是win32com

https://everythingwhat.com/what-is-win32com-client



批量给表格题注样式的文字前插入表格题注

```python
from win32com.client import Dispatch


app = Dispatch("Word.Application")
doc = app.Documents.Open(r"C:\Users\ztn\Desktop\template.docx")
app.visible = True
s = app.Selection

s.Find.Style = doc.Styles("表格题注")

while s.Find.Execute(
    FindText="", 
    Forward=True,
    Wrap=1,
    Format=True,
    MatchCase=False,
    MatchWholeWord=True,
    MatchAllWordForms=False,
    MatchSoundsLike=False,
    MatchWildcards=False,):
    
    s.MoveLeft()  # 光标向左移动一格
    s.InsertCaption(Label='表')  # 插入题注
```

原理就是查找满足指定样式的一段文字，然后把光标移动到这段文字最前面并在此处插入题注

原本

![image-20211009174520845](img/image-20211009174520845.png)

之后

![image-20211009174612530](img/image-20211009174612530.png)

注意：

- 样式表里要有一个”题注“样式，这样插入表格题注以后，该行文字的样式就会由原本的**“表格题注”样式**变成**“题注”样式**。这样重复执行代码就不会发生重复插入题注的问题了，注意如果希望改变前后样式不发生改变，表格题注与题注的样式设置需要完全一致。
- 这里的题注会显示章节号（表1-3中的1表示这是第一章的表格），因此需要事先定义好标题1的样式。



## win32com.client.constants

一些常量



https://stackoverflow.com/questions/28264548/how-to-use-win32com-client-constants-with-ms-word

- wdDoNotSaveChanges：退出时不保存
- wdSaveChanges：退出时保存

