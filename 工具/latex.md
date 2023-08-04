## 常用latex

[typora官方文档](https://support.typora.io/Math/)

[katex参考网址](<https://katex.org/docs/supported.html>)

[基本Latex语法](https://www.zybuluo.com/codeep/note/163962#mjx-eqn-eqsample)

[关于Typora数学公式自动编号](https://www.cnblogs.com/nowgood/p/Latexstart.html#_nav_8)

[在线公式编辑器](<http://latex.codecogs.com/eqneditor/editor.php>)

| 效果      | 代码      | 效果          | 代码          | 效果   | 代码   |
| --------- | --------- | ------------- | ------------- | ------ | ------ |
| $\bar{a}$ | `\bar{a}` | $\mathcal{L}$ | `\mathbb{L}`  | $\rho$ | `\rho` |
| $\hat{a}$ | `\hat{a}` | $\mathscr{L}$ | `\mathscr{L}` |        |        |
| $\cdot$   | `\cdot`   | $\mathbb{L}$  | `\mathbb{L}`  |        |        |
|           |           |               |               |        |        |
|           |           |               |               |        |        |

### 公式对齐

使用`&`确定对齐的位置

[公式对齐](https://blog.csdn.net/bendanban/article/details/77336206)

```
$$
\begin{align}
f(x) =& x^2 + 2x + 1 \\
g(x) =& 2x + 2
\end{align}
$$
```

$$
\begin{align}
f(x) =& x^2 + 2x + 1 \\
g(x) =& 2x + 2
\end{align}
$$

### 带大括号的公式

$$
a_{i}=
\left\{ 
    \begin{aligned}
        0 & & {a>p}\\ 
        1 & & {a \leq p} \\
    \end{aligned} 
\right.
$$

### 数组

$$
\mathbf{x}=[x_1, x_2,...,x_n]
$$


$r_i \in \{0, 1\}$

### 矩阵

[如何用latex编写矩阵（包括各类复杂、大型矩阵）？ - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/266267223)
$$
P = 
\begin{bmatrix}
p_{00} & p_{01} & p_{02} & p_{03} \\
p_{10} & p_{11} & p_{12} & p_{13} \\
p_{20} & p_{21} & p_{22} & p_{23} \\
p_{30} & p_{31} & p_{32} & p_{33} \\
\end{bmatrix}
$$

求和符号的单行形式
$$
\textstyle\sum_{i=1}^n
$$
箭头带说明
$$
\xrightarrow[under]{over}
$$
