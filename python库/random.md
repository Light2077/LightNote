总结：

| 语法                                          | 说明                              | 示例                       |
| --------------------------------------------- | --------------------------------- | -------------------------- |
| `random.random()`                             | 生成[0,1)之间的随机浮点数         |                            |
| `random.randint(a,b)`                         | 生成[a,b]之间的随机整数           | `random.randint(0,1)`      |
| `random.uniform(a,b)`                         | 生成[a,b]之间的随机浮点数         | `random.uniform(1.5,3)`    |
| `random.randrange(a,b,step)`                  | 生成[a,b)之间以step递增的随机整数 | `random.randrange(1,11,2)` |
| `random.choice(arr)`                          | 返回arr数组中的随机一个元素       |                            |
| `random.choices(arr, weights, cum_weights,k)` | **有放回**随机抽取arr中的k个元素  |                            |
| `random.sample(arr,k)`                        | **无放回**抽取arr中的k个元素      |                            |
| `random.shuffle(arr)`                         | 打乱arr                           |                            |

