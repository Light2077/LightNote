# pandas.merge用法
用于按照某列列值来合并两个数据集

主要介绍`pandas.merge`的几个常见参数的用法
- `on`: 默认为`None`，选择按照两数据集的某个或几个**共有列**来合并数据集
- `suffixes`: 默认为`('_x', '_y')`，合并时，若数据集存在多个共有列，但on只选择了部分共有列来合并，其余共有列在合并时会被添加上后缀。
- `left_on`和`right_on`:默认为`None`，若两数据集用于合并的列列名不同，则分别指定。
- `how`: 默认为`'inner'`，按照合并列列值的并集合并。有(`'left'`, `'right'`, `'outer'`, `'inner'`) 四种取值。
  - `inner`： 两数据集的共有列取交集
  - `outer`： 取并集
  - `left`: 保证左边的数据集的共有列的值全部出现
  - `right`： 保证右边数据集的共有列值全部出现



构造两个DataFrame

```python
left = pd.DataFrame({'key': ['K0', 'K1', 'K1', 'K3'],
                      'A': ['A0', 'A1', 'A2', 'A3'],
                     'B': ['B0', 'B1', 'B2', 'B3']})

right = pd.DataFrame({'key': ['K0', 'K1', 'K2', 'K3'],
                     'C': ['C0', 'C1', 'C2', 'C3'],
                     'D': ['D0', 'D1', 'D2', 'D3']})
```



```
# left

	key A 	B
0 	K0 	A0 	B0
1 	K1 	A1 	B1
2 	K1 	A2 	B2
3 	K3 	A3 	B3

# right

	key C 	D
0 	K0 	C0 	D0
1 	K1 	C1 	D1
2 	K2 	C2 	D2
3 	K3 	C3 	D3
```

### 直接合并

```python
pd.merge(left, right)

"""

	key A 	B 	C 	D
0 	K0 	A0 	B0 	C0 	D0
1 	K1 	A1 	B1 	C1 	D1
2 	K1 	A2 	B2 	C1 	D1
3 	K3 	A3 	B3 	C3 	D3
"""
```

