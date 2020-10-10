### kfold交叉验证

注意split后迭代，迭代的元素是索引

```python
from sklearn.model_selection import KFold
x = [1, 2, 3, 4, 5, 6]
y = [0, 0, 1, 0, 1, 1]

kfold = KFold(n_splits=3, shuffle=True, random_state=2020)
for train_idx, test_idx in kfold.split(x, y):
    print(train_idx, test_idx)
```

