```python
    ip_stat = trade.groupby(['IP地址', '收付标志']).agg({
        '交易卡号': [pd.Series.nunique, 'count'],
        '交易金额': [sum],
        '交易户名': [lambda x: ','.join(x.unique())],
        '交易时间': [min, max]
    })
```

