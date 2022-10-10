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

