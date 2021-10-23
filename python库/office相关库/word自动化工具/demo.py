from word import Word

w = Word(template_path="./template.docx", save_path="demo.docx")

# 插入标题1
w.add_heading("测试", 1)
w.add_heading("小标题", 2)

# 插入正文
w.add_paragraph("正文文本，自动使用正文文本格式")

# 插入图片
import matplotlib.pyplot as plt
plt.plot([1, 2, 3], [1, 2, 3])
plt.savefig("demo.png")
w.add_picture("demo.png", title="测试图片")

# 插入表格
import pandas as pd
df = pd.DataFrame([[1, 2, 3], [4, 5 ,6]])
w.add_table(df, title="测试表格")


w.save()

# 自动给表格、图片题注添加word的引用功能（可以不用这行代码，这个功能还在完善中）
# 最后才能使用这个功能，使用后无须再次保存（会自动保存word文档）
w.add_caption()