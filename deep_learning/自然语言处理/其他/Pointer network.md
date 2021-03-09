# Pointer network

从输入序列中找到相应的tokens作为输出，利用Attention作为pointer，从输入序列中选择一个位置，并将这个位置所指向的词作为输出。
$$
\begin{aligned}
u_j^i&=v^Ttanh(W_1e_j+W_2d_i) \\
p(C_i|C_1,...,C_{i-1},P)&=softmax(u^i)
\end{aligned}
$$
attention 源自于凸包的概念，有很多歌点，给定一个序列，可以把所有点包起来