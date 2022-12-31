用python写一段代码，把pdf里的每一页转换为图片

安装相应的库

```
pip install pypdf2
pip install Pill
```



代码

```python
import os
import pypdf2
from PIL import Image

# 打开PDF文件
pdf_file = open('example.pdf', 'rb')

# 创建一个 PDF 读取器对象
pdf_reader = pypdf2.PdfFileReader(pdf_file)

# 获取PDF文件中的页数
num_pages = pdf_reader.getNumPages()

# 循环遍历每一页
for i in range(num_pages):
  # 获取每一页
  page = pdf_reader.getPage(i)
  # 解码每一页中的内容
  page_content = page.extractText()

  # 使用 Pillow 库将内容转换为图片
  img = Image.frombytes('RGB', (page.mediaBox.getWidth(), page.mediaBox.getHeight()), page_content.encode('utf-8'))
  # 保存图片
  img.save('page_{}.jpg'.format(i))

# 关闭PDF文件
pdf_file.close()

```

