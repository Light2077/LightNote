https://python-docx.readthedocs.io/en/latest/index.html

https://gitchat.csdn.net/activity/5eae400be90db13e2ff6f56e

查看所有的样式

```python
from docx.enum.style import WD_STYLE_TYPE
styles = document.styles
paragraph_styles = [
     s for s in styles if s.type == WD_STYLE_TYPE.PARAGRAPH
]
for style in paragraph_styles:
    print(style.name)
```

将DataFrame数据输出到word

```python
from docx import Document

# 将dataframe格式的文件转换为word
def df_to_word(df, template_path=config.word_template, file_path='tmp.docx'):
    document = Document(template_path)
    table = document.add_table(rows=1, cols=df.shape[1])

    for header_cell, header in zip(table.rows[0].cells, df.columns):
        header_cell.text = header
        header_cell.paragraphs[0].style = 'No Spacing'

    for _, row in df.iterrows():
        row_cells = table.add_row().cells
        for i, (_, value) in enumerate(row.iteritems()):
            row_cells[i].text = str(value)
            row_cells[i].paragraphs[0].style = 'No Spacing'

    table.style = "三线表"
    document.save(file_path)


def test_df_to_word():
    import pandas as pd
    import os
    df = pd.DataFrame([[1, 2, 3, 4],
                       [2, 3, 4, 5],
                       [3, 4, 5, 6]], columns=['apple', 'pear', 'banana', 'orange'])

    df_to_word(df, template_path=config.word_template, file_path='tmp.docx')
    assert os.path.isfile('tmp.docx')
    os.remove('tmp.docx')


if __name__ == '__main__':
    test_df_to_word()
```

图片插入

```python
from docx.shared import Cm
document.add_picture('demo.png', width=Inches(5.76))
```

若想插入最大不超过页边距的宽度，则需要额外设置一些东西

首先要获得最大页面宽度

页面宽度 - 左边距 - 右边距

如果纸张大小是A4 21cm × 29.7cm，左右边距都是3.18。

最大宽度就是：

```python
from docx.shared import Cm
max_width = Cm(14.64)
```

插入一张图片，如果图片宽度大于最大宽度，自动缩放

```python
def add_picture(pic_path, max_width=Cm(14.64)):
    pic = document.add_picture(pic_path)
    
    # 自动缩放
    if pic.width > max_width:
        ratio = max_width / pic.width  # 缩放比例
        pic.width = int(pic.width * ratio)
        pic.height = int(pic.height * ratio)
    # 居中
    
```

顺便自动居中、再插入一个图片名称在下方

```python
def add_picture(pic_path, max_width=Cm(14.64), title=None):
    pic = document.add_picture(pic_path)
    if pic.width > max_width:
        ratio = max_width / pic.width  # 缩放比例
        pic.width = int(pic.width * ratio)
        pic.height = int(pic.height * ratio)
        
    # 居中刚刚插入的图片
    last_paragraph = document.paragraphs[-1]
    last_paragraph.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER
    
    # 插入标题
    if title:
        document.add_paragraph(title, style='表图题')
```

