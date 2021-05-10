$$
\text{Attention}(Q,K,V)=\text{softmax}(\frac{QK^T}{\sqrt{d_k}})V
$$

其中$\mathbf{Q} \in \mathbf{R}^{n \times d_k}$、$\mathbf{K} \in \mathbf{R}^{m \times d_k}$、$\mathbf{V} \in \mathbf{R}^{m \times d_v}$


$$
\text{MultiHead}(Q,K,V)=\text{Concat}(\text{head}_1,...,\text{head}_h)W^O
$$
其中
$$
\text{head}_i=\text{Attention}(QW_i^Q,KW_i^K,VW_i^V)
$$
