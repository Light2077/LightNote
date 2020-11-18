# map

把函数当成参数传递的函数就是高阶函数

```python
map(function, iterable, ..)
```

## 使用内置函数

```python
nums = ['1', '2', '3', '4']
print(nums)
res = map(int, nums)  # map object
print(res)

for i in res:
    print(i)
```

## 使用匿名函数

```python
nums = [1, 2, 3, 4]
res = map(lambda x: x + 2, nums)
print(list(res))
```

## 使用自定义函数

```python
nums = [1, 2, 3, 4]
def add(x):
    return x + 10
res = map(add, nums)
print(list(res))
```



## 多个参数的情况

```python
nums1 = [1, 2, 3, 4]
nums2 = [10, 20, 30, 40]
res = map(lambda x,y: x + y, nums1, nums2)
print(list(res))
```

自定义函数版

```python
nums1 = [1, 2, 3, 4]
nums2 = [10, 20, 30, 40]
def add(x, y):
    return x + y
res = map(add, nums1, nums2)
print(list(res))
```

## 应用案例，字典进行键值对互换

```python
d = {'北京':1, '上海':2, '深圳':3}
def swap(item):
    return (item[1], item[0])
res = map(swap, d.items())
print(dict(res))
```

解释：

可以用强制类型转换，把2维元组转换成字典。转换3维及以上会报错

```python
a = [(1, 2), (2, 4)]
# a = ((1, 2), (2, 4))
# a = {(1, 2), (2, 4)}
print(dict(a))
```

匿名函数版本

```python
d = {'北京': 1, '上海': 2, '深圳': 3}
res = map(lambda x: (x[1], x[0]), d.items())
print(dict(res))

```

# reduce

```python
reduce(function, sequence[, initial])
```

给定一个序列，依次取出1个元素作为参数，与前一次函数的结果进行运算，最后返回运算结果。注意返回值，返回的是计算结果

```python
from functools import reduce

nums = [1, 2, 3, 4]
res = reduce(lambda x, y: x * y, nums, 1)
print(res)

strs = ['a', 'b', 'c', 'd']
res = reduce(lambda x, y: x + y, strs, '')
print(res)
```

上面两个例子中，初始值设置不设置结果一样，可以根据具体情况设定初始值。

# sorted

```
sorted(iterable, reverse=False, key=function)
return Iterator
```

给一个可迭代对象排序，并返回一个可迭代对象。默认是从小到大排序

```python
nums = [-7, 3, 6, -2, 5]
print(sorted(nums))
# [-7, -2, 3, 5, 6]

print(sorted(nums, reverse=True))
# [6, 5, 3, -2, -7]

print(sorted(nums, key=abs))
# [-2, 3, 5, 6, -7]
```

字典排序，默认以字典的key来排序

```python
d = {2:'a', 1:'b', 3:'c'}

# 相当于sorted(d.keys())
print(sorted(d))
# [1, 2, 3]
```

例子：

按照出现次数来排序

```python
arr = ['a', 'b', 'b', 'b', 'c', 'c']
print(sorted(arr, key=arr.count))
# ['a', 'c', 'c', 'b', 'b', 'b']
```

与sort的区别

sort改变原有的对象，sorted返回排序后的结果。

# filter

**保留为True的元素**

```
filter(func, iterable) -> iterable
```

比如：只保留偶数

```python
nums = [1, 2, 3, 4, 5, 6]
res = filter(lambda x: x % 2 == 0, nums)
print(list(res))
# [2, 4, 6]
```

也可传入自定义函数

```python
nums = [1, 2, 3, 4, 5, 6]
def get_even(x):
    if x % 2 == 0:
        return True
    else:
        return False
res = filter(get_even, nums)
print(list(res))
# [2, 4, 6]
```

# 总结

map, reduce, filter

- 第一个参数都是function
- 第二个函数都是可迭代对象

sorted

- 可迭代对象
- 排序的顺序
- function