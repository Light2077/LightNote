https://blog.csdn.net/qq_44703886/article/details/110110737

```python
import xlwt

workbook = xlwt.Workbook(encoding='gbk')
worksheet = workbook.add_sheet('sheet1', cell_overwrite_ok=True)

# 初始化样式
style = xlwt.XFStyle()
```

