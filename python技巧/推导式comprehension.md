# 列表推导式

```python
nums = [i ** 2 for i in range(5)]
print(nums)
```



if 在后面的情况

```python
nums = [i ** 2for i in range(5) if i % 2 == 0 ]
print(nums)
```

if 在前面时， 必须写else

```python
nums = [i ** 2 if i % 2 == 0 else 0 for i in range(5)]
print(nums)
```

for 循环嵌套

```python
nums = [i * j for i in range(1, 4) for j in range(i, 4)]
print(nums)
```

# 字典推导式

```python
city = ['北京', '上海', '深圳']
nums = [1, 2, 3]

d = {city[i]: nums[i] for i in range(3)}
print(d)
```

# 集合推导式

```python
nums = [1, 2, 2, 2, 3, 3, 4]
s = {i for i in nums}
print(s, type(s))
```



# 生成器表达式

就是用括号写的推导式

```python
g = (i for i in range(2))
print(type(g))
```

