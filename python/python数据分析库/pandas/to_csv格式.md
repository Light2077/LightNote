会在每个数据前加双引号

```python
df = pd.DataFrame([['lily', 4], 
                   ['tom', 5]], columns=['name', 'age'])
df.to_csv('tmp123.csv', index=None, quoting=1)
```

```
"name","age"
"lily","4"
"tom","5"
```

