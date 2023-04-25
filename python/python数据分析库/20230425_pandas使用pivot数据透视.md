```python
import pandas as pd

data = {
    "group": [1, 1, 1, 2, 2, 2, 3, 3, 3],
    "name": ["a", "b", "c", "a", "b", "c", "a", "b", "c"],
    "value": [1, 200, "hello", 2, 850, "good", 3, 1205, "hi"]
}

df = pd.DataFrame(data)
print(df)
"""
   group name  value
0      1    a      1
1      1    b    200
2      1    c  hello
3      2    a      2
4      2    b    850
5      2    c   good
6      3    a      3
7      3    b   1205
8      3    c     hi
"""
result = df.pivot(index="group", columns="name", values="value")
result.reset_index(drop=True, inplace=True)

print(result)
"""
name  a     b      c
0     1   200  hello
1     2   850   good
2     3  1205     hi
"""
```

