```python
    ip_stat = trade.groupby(['IP地址', '收付标志']).agg({
        '交易卡号': [pd.Series.nunique, 'count'],
        '交易金额': [sum],
        '交易户名': [lambda x: ','.join(x.unique())],
        '交易时间': [min, max]
    })
```



```python
    stat = trade.groupby(['收付标志', '交易对手账卡号', '对手户名']).agg(
        卡号数量=pd.NamedAgg('交易卡号', pd.Series.nunique),
        交易总额=pd.NamedAgg('交易金额', sum),
        交易次数=pd.NamedAgg('交易金额', 'count'),
        平均交易额=pd.NamedAgg('交易金额', 'mean'),
        最早交易时间=pd.NamedAgg('交易时间', min),
        最晚交易时间=pd.NamedAgg('交易时间', max)
    ).reset_index()
```

