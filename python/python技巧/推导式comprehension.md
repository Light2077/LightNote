# 列表推导式

```python
nums = [i ** 2 for i in range(6)]
print(nums)
```

```
[0, 1, 4, 9, 16, 25]
```



if 在后面的情况

```python
nums = [i + 1 for i in range(6) if i % 2 == 0 ]
print(nums)
```

```
[1, 3, 5]
```



if 在前面时， 必须写else

```python
nums = [0 if i % 2 == 0 else i+1 for i in range(6)]
print(nums)
```

```
[0, 2, 0, 4, 0, 6]
```



for 循环嵌套

```python
nums = [i * j for i in range(1, 4) 
              for j in range(i, 4)]
print(nums)
```

```
[1, 2, 3, 4, 6, 9]
```



# 字典推导式

```python
cities = ['北京', '上海', '深圳']
nums = [1, 2, 3]

d = {city: n for city, n in zip(cities, nums)}
print(d)
```

```
{'北京': 1, '上海': 2, '深圳': 3}
```



# 集合推导式

```python
nums = [1, 2, 2, 2, 3, 3, 4]
s = {i for i in nums}
print(s)
print(type(s))
```

```
{1, 2, 3, 4}
<class 'set'>
```



# 生成器表达式

就是用括号写的推导式

```python
g = (i for i in range(5))
print(type(g))
print(list(g))
```

```
<class 'generator'>
[0, 1, 2, 3, 4]
```

