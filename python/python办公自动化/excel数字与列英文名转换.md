

```python
def number_to_excel_column(n):
    if n <= 0:
        return ""
    result = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)  # 减1是为了适应Excel的从1开始的列索引
        result = chr(65 + remainder) + result  # 65对应字符'A'
    return result

def excel_column_to_number(column):
    result = 0
    for char in column:
        result = result * 26 + (ord(char) - 64)  # 64对应字符'A'
    return result
```

使用示例：

```python
# 数字到Excel列
print(number_to_excel_column(1))  # 输出: "A"
print(number_to_excel_column(18))  # 输出: "R"
print(number_to_excel_column(52))  # 输出: "AZ"

# Excel列到数字
print(excel_column_to_number("A"))  # 输出: 1
print(excel_column_to_number("R"))  # 输出: 18
print(excel_column_to_number("AZ"))  # 输出: 52
```

