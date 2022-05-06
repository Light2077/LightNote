https://www.geeksforgeeks.org/regression-analysis-and-the-best-fitting-line-using-c/

```python
class Correlation:
    """ 存储分块读取数据的中间变量 """
    def __init__(
            self, n=0, sum_x=0, sum_y=0, sum_xy=0, square_sum_x=0, square_sum_y=0
        ):
        self.n = n
        self.sum_x = sum_x
        self.sum_y = sum_y
        self.sum_xy = sum_xy
        self.square_sum_x = square_sum_x
        self.square_sum_y = square_sum_y

    @classmethod
    def create_by_xy(cls, x, y):
        assert len(x) == len(y)
        return cls(
            n = len(x),
            sum_x = np.sum(x),
            sum_y = np.sum(y),
            sum_xy = x @ y,
            square_sum_x = x @ x,
            square_sum_y = y @ y,
        )

    def __add__(self, o):
        return Correlation(
            self.n + o.n,
            self.sum_x + o.sum_x,
            self.sum_y + o.sum_y,
            self.sum_xy + o.sum_xy,
            self.square_sum_x + o.square_sum_x,
            self.square_sum_y + o.square_sum_y,
        )

    def __eq__(self, o) -> bool:
        if self.n != o.n:
            return False

        if not np.allclose(
            [self.sum_x, self.sum_y, self.sum_xy, self.square_sum_x, self.square_sum_y],
            [o.sum_x, o.sum_y, o.sum_xy, o.square_sum_x, o.square_sum_y],
        ):
            return False
        return True

    # 由中间变量计算得出相关性
    def corr(self):
        return (self.n * self.sum_xy - self.sum_x * self.sum_y) / \
            np.sqrt(
                (
                    (self.n * self.square_sum_x - self.sum_x * self.sum_x) * \
                    (self.n * self.square_sum_y - self.sum_y * self.sum_y)
                )
            )

    @property
    def slope(self):
        """ 计算斜率 """
        # 计算方式1: 使用相关系数换算
        # return self.corr() * \
        #            np.sqrt(
        #                (self.n * self.square_sum_y - self.sum_y * self.sum_y) / \
        #                (self.n * self.square_sum_x - self.sum_x * self.sum_x)
        #            )

        # 计算方式2: 直接计算
        return (self.n * self.sum_xy - self.sum_x * self.sum_y) / \
               (self.n * self.square_sum_x - self.sum_x * self.sum_x)

    @property
    def intercept(self):
        """ 计算截距 """
        return (self.sum_y * self.square_sum_x - self.sum_x * self.sum_xy) /\
               (self.n * self.square_sum_x - self.sum_x * self.sum_x)
```

相关系数
$$
corr = \frac{n\sum{x_iy_i}-\sum{x_i}\sum{y_i}}{\sqrt{(n\sum{x_i^2}-(\sum{x_i})^2)(n\sum{y_i^2}-(\sum{y_i})^2)}}
$$


