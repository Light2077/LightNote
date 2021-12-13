# lambda 表达式

函数式编程要求：只使用表达式，不使用语句，也就是说，每一步都是单纯的运算，且**要有返回值**

```python
func = lambda x: x + 1
print(func(10))

func = lambda x,y: x + y
print(func(2, 10))

func = lambda *args: sum(args)
print(func(1, 2, 3, 4, 5))

func = lambda **kwargs: f'{kwargs}'
print(func(id=1, city='北京'))

func = lambda *args, **kwargs: f'{args}--{kwargs}'
print(func(1, 2, 3, 4, id=1, city='北京'))
```

无参数lambda表达式

```python
func = lambda : print('hello')

func()
```

