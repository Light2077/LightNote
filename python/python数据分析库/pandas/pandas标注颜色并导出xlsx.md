https://pandas.pydata.org/docs/user_guide/style.html

```python
def func(s, names):
    if s.name == '账户开户名称':
        return np.where(s.isin(names), 'color:#9C0006;background-color:#FFC7CE', '')
    elif s.name == '对手户名':
        return np.where(s.isin(names), 'color:#006100;background-color:#C6EFCE', '')
    elif s.name == '是否调单':
        return np.where(s == '否', 'color:#9C5700;background-color:#FFEB9C', '')
    
trade_group.sample(30).style.apply(func, subset=['账户开户名称', '对手户名', '是否调单'], names=names)
```



```
color:#9C0006;background-color:#FFC7CE
```

假设现在有一个DataFrame，有两列， 预测值: [1, 2, 3, 3, 3, 4] 实际值: [1, 2, 3, 4, 3, 4] 我想用dataframe的style功能，把两列不同的值找出来，并在预测值这一列标记一下单元格的颜色为粉色，该怎么做？

```python
import pandas as pd

# 假设你的DataFrame如下：
df = pd.DataFrame({
    '预测值': [1, 2, 3, 3, 3, 4],
    '实际值': [1, 2, 3, 4, 3, 3]
})

# 定义一个函数，用于应用样式
def highlight_diffs(data, color='pink'):
    attr = 'background-color: {}'.format(color)
    result = []
    for name in data.index:
        if data['预测值'] != data['实际值'] and name == "预测值":
            result.append(attr)
        else:
            result.append("")
    return result

# 应用样式
df.style.apply(highlight_diffs, axis=1)

```

