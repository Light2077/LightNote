https://numpy.org/doc/stable/reference/index.html

https://numpy.org/doc/stable/reference/generated/numpy.argpartition.html?highlight=argpartition#numpy.argpartition

```
numpy.argpartition(a, kth, axis=-1, kind='introselect', order=None)
```

简而言之：**前小后大**

返回的是一个索引，类似快速排序里找主元的过程，但略微有点区别

比如说下面这个例子

```python
x = np.array([6, 5, 4, 3, 2, 1, 0])
idxs = np.argpartition([6, 5, 4, 3, 2, 1, 0], kth=4)

print(x[idxs])
```

```
array([2, 0, 1, 3, 4, 5, 6])
```

这里`kth=4`，那返回的排序结果就是，注意这里返回的是排序结果的索引`idxs`，通过`x[idxs]`得到排序结果。

- 第4个位置之**前**的数（`x[:4]`）都**小于**等于`x[4]`
- 第4个位置之**后**的数`x[4:]`都**大于**等于`x[4]`

如果提供多个kth，那么就会保证这些索引都会被放到正确排序后的位置，比如

```python
x = np.array([9, 8, 7, 6, 5, 4, 3, 2, 1, 0])
idxs = np.argpartition(x,[2, 6])
x[idxs]
```

```
array([0, 1, 2, 5, 3, 4, 6, 7, 8, 9])
```

`x[2]`和`x[6]`都被放到了正确的位置，即之前的数都小于等于自身，之后的数都大于等于自身

