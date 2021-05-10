```python
import random
random.seed(2020)
class BoxHMM:
    def __init__(self):
        # 初始概率
        self.pi = [0.2, 0.4, 0.4]
        
        # 盒子之间转移概率
        self.a = [[0.5, 0.2, 0.3], 
                  [0.3, 0.5, 0.2], 
                  [0.2, 0.3, 0.5]]
        
        # 红球白球
        self.b = [[0.5, 0.5],
                  [0.4, 0.6],
                  [0.7, 0.2]]
        
        self.boxes = list(range(len(self.a)))  # 3个盒子 [0, 1, 2]
        self.bolls = ["红", "白"]
        
    def generate(self, t):
        """
        根据观测长度t，获取观测序列
        """
        ans = []
        for i in range(t):
            if i == 0:
                box_id = self.box_init()
            else:
                box_id = self.box_transfer(box_id)
            boll = self.get_boll(box_id)
            ans.append(boll)
        return ans
    
    # 获得初始的盒子
    def box_init(self):
        return random.choices(self.boxes, weights=self.pi)[0]
    
    # 盒子转移
    def box_transfer(self, box_id):
        return random.choices(self.boxes, weights=self.a[box_id])[0]
    
    # 根据盒子选小球
    def get_boll(self, box_id):
        return random.choices(self.bolls, weights=self.b[box_id])[0]
    
    
hmm = BoxHMM()
hmm.generate(5)
```

```
['red', 'white', 'white', 'red', 'red']
```

小球生成器，观测序列的生成过程

隐马尔科夫模型的3个基本问题：

- 给定模型$\lambda =(A, B,\pi)$如何计算观测序列O出现的概率$P(O| \lambda )$
- 已知观测序列$O=(o_1,...,o_T)$，估计模型$\lambda =(A, B,\pi)$的参数，使得该模型下观测序列概率$P(O| \lambda )$最大
- 预测问题，也称为解码问题，已知模型$\lambda =(A, B,\pi)$和观测序列$O=(o_1,...,o_T)$，求对给定观测序列条件概率$P(I|O)$最大的状态序列$I=(i_1,...,i_T)$。**就是已知观测，倒推求状态**

# 概率计算方法

## 前向概率计算

输入，HMM模型$\lambda =(A, B,\pi)$，观测序列$O=(o_1,...,o_T)$

输出：$P(O| \lambda )$

### 计算步骤

**初值**

对于$i=1,2,...,N$
$$
\alpha_1(i)=\pi_ib_i(o_1)
$$


**递推**，对$t=1,2,...,T-1$
$$
\alpha_{t+1}(i)=[\sum_{j=1}^N\alpha_t(j)a_{ji}]b_i(o_{t+1})
$$
**终止**
$$
P(O| \lambda )=\sum_{i=1}^N\alpha_T(i)
$$

### 推导

关键是理解递推公式是怎么来的。

首先定义前向概率
$$
\alpha_t(i)=P(o_1,...,o_t,i_t=q_i| \lambda)
$$
t，表示第t个时刻，i表示状态为第i个取值。则
$$
\alpha_1(i)=P(o_1,i_1=q_i|\lambda)
$$
现在想求$\alpha_2(i)=P(o_1,o_2,i_2=q_i|\lambda)$，比较两个式子的不同之处。构造成一样的。

思路是，先全部整出来，也就是构建$P(o_1,o_2,i_1, i_2=q_i|\lambda)$，然后可以通过对$i_1$求和的方式消去它，也就是
$$
P(o_1,o_2, i_2=q_i|\lambda)=\sum_{i_1}P(o_1,o_2,i_1, i_2=q_i|\lambda)
$$


首先想办法把$o_2$整出来，想到状态转移概率$P(o_2|i_2,\lambda)=b_j(k)$
$$
P(o_1,o_2,i_1, i_2=q_i|\lambda) = P(o_2|o_1,i_1,i_2,\lambda)P(o_1,i_1,i_2|\lambda)
$$
然后根据hmm的假设，**当前时刻的观测值，只与当前时刻的状态有关**，即
$$
P(o_2|o_1,i_1,i_2,\lambda)=P(o_2|i_2,\lambda)
$$
这样就可以简化一下。

然后想办法把$i_2$整出来，想到状态转移概率$P(i_2|i_1,\lambda)=a_{ij}$
$$
P(o_1,i_1,i_2|\lambda) = P(i_2|o_1,i_1,\lambda)P(o_1,i_1|\lambda)
$$
然后根据hmm的假设，**当前时刻的状态，只与上一时刻的状态有关**，即
$$
P(i_2|o_1,i_1,\lambda)=P(i_2|i_1,\lambda)
$$
综合一下上面的推理过程


$$
\begin{aligned}
\alpha_{t}(i)&=P(o_1,...,o_t, i_t=q_i|\lambda) \\
\alpha_{t+1}(i)&=P(o_1,...,o_t,o_{t+1},i_{t+1}=q_i|\lambda) \\

&=\sum_{j=1}^N P(o_1,...,o_t,o_{t+1},i_{t}=q_j,i_{t+1}=q_i|\lambda) \\

&=\sum_{j=1}^N P(o_1,...,o_t,i_{t}=q_j|\lambda)
               P(o_{t+1},i_{t+1}=q_i|o_1,...,o_t,i_{t}=q_j,\lambda)\\
               
&=\sum_{j=1}^N P(o_1,...,o_t,i_{t}=q_j|\lambda)
               P(i_{t+1}=q_i|o_1,...,o_t,i_{t}=q_j,\lambda)
               P(o_{t+1}|o_1,...,o_t,i_{t}=q_j,i_{t+1}=q_i,\lambda)\\
               
&=\sum_{j=1}^N P(o_1,...,o_t,i_{t}=q_j|\lambda)
               P(i_{t+1}=q_i|i_{t}=q_j,\lambda)
               P(o_{t+1}|i_{t+1}=q_i,\lambda)\\

\alpha_{t+1}(i)&=\sum_{j=1}^N \alpha_t(j)a_{ji}b_i(o_{t+1})
\end{aligned}
$$
注意这里可能会忘记$a_{ji}$是啥，这个是状态转移概率，即状态$q_i$转移到状态$q_j$的概率。原始公式如下：
$$
a_{ij}=P(i_{t+1}=q_j|i_t=q_i)
$$
注意这里还可能会忘记$b_i(o_2)$是啥，这个是观测概率，即状态值为$q_i$时生成观测值$o_2$的概率。原始公式如下
$$
b_j(k)=P(o_t=v_k|i_t=q_j)
$$
这里$o_2$相当于一个已知的值。

### 例题

考虑盒子和球模型$\lambda =(A, B,\pi)$，状态集合$Q={1,2,3}$，观测集合$V=\{红,白\}$
$$

A=\left[\begin{array}{l}
0.5 & 0.2 & 0.3\\
0.3 & 0.5 & 0.2\\
0.2 & 0.3 & 0.5
\end{array}\right],

B=\left[\begin{array}{l}
0.5 & 0.5\\
0.4 & 0.6\\
0.7 & 0.3
\end{array}\right],
\pi=(0.2,0.4,0.4)^{\mathbf{T}}
$$
设$T=3$,$O=(红,白,红)$，计算$P(O|\lambda)$



用代码来计算把

```python
import random
random.seed(2020)
class BoxHMM:
    def __init__(self):
        # 初始概率
        self.pi = [0.2, 0.4, 0.4]
        
        # 盒子之间转移概率
        self.a = [[0.5, 0.2, 0.3], 
                  [0.3, 0.5, 0.2], 
                  [0.2, 0.3, 0.5]]
        
        # 红球白球
        self.b = [[0.5, 0.5],
                  [0.4, 0.6],
                  [0.7, 0.3]]
        
        self.num_state = len(self.a)  # 状态个数
        self.boxes = list(range(self.num_state))  # 3个盒子 [0, 1, 2]
        self.bolls = {"红":0, "白":1}
        
    def generate(self, t):
        """
        根据观测长度t，获取观测序列
        """
        ans = []
        for i in range(t):
            if i == 0:
                box_id = self.box_init()
            else:
                box_id = self.box_transfer(box_id)
            boll = self.get_boll(box_id)
            ans.append(boll)
        return ans
    
    # 获得初始的盒子
    def box_init(self):
        return random.choices(self.boxes, weights=self.pi)[0]
    
    # 盒子转移
    def box_transfer(self, box_id):
        return random.choices(self.boxes, weights=self.a[box_id])[0]
    
    # 根据盒子选小球
    def get_boll(self, box_id):
        return random.choices(list(self.bolls.keys()), weights=self.b[box_id])[0]
    
    
    def cal_init_alpha(self, obs_label):
        alpha = [0] * self.num_state
        
        obs_idx = self.bolls[obs_label]
        for i in range(self.num_state):
            alpha[i] = self.pi[i] * self.b[i][obs_idx]
        
        return alpha
            
    def get_observation_sequence_probability(self, obs_seq):
        
        
        # 计算初始值
        alpha = self.cal_init_alpha(obs_seq[0])
        
        # 递推
        for t in range(1, len(obs_seq)):
            
            # 获得t时刻的标签和索引
            obs_label = obs_seq[t]
            obs_idx = self.bolls[obs_label]
            
            # 新的alpha
            new_alpha = [0] * len(alpha)
            
            # 对于每个状态
            for i in range(self.num_state):
                for j in range(self.num_state):
                    new_alpha[i] += alpha[j] * self.a[j][i]
                new_alpha[i] *= self.b[i][obs_idx]

            alpha = new_alpha
            print(t, alpha)
            
        # 终止
        return sum(alpha)
    
    
hmm = BoxHMM()
print(hmm.generate(5))
print(hmm.cal_init_alpha("红"))
hmm.get_observation_sequence_probability(["红", "白", "红"])
```

```
['红', '白', '白', '白', '红']
[0.1, 0.16000000000000003, 0.27999999999999997]
1 [0.077, 0.1104, 0.060599999999999994]
2 [0.04186999999999999, 0.035512, 0.052835999999999994]

0.130218
```

前向算法
$$
P(o_1,...,o_t,i_t=q_i|\lambda)
$$

## 后向算法

### 计算步骤

（1）对于i=1,...,N
$$
\beta_T(i)=1
$$
（2）递推，对于t=T-1, T-2, ..., 1
$$
\beta_t(i)=\sum_{j=1}^{N}a_{ij}b_j(o_{t+1})\beta_{t+1}(j)
$$
（3）终止
$$
P(O| \lambda )=\sum_{i=1}^N \pi_ib_i(o_1)\beta_T(i)
$$

### 推导

$$
\beta_t(i)=P(o_{t+1},o_{t+2},...,o_T|i_t=q_i,\lambda)
$$

则，起始状态可以令成1，主要是为了方便？本来还需要看看时刻T后面有什么东西，但因为最后一个时刻T 后面已经没有时刻，即不需要再观测某个东西，所以你随便给个什么都行，我不在乎
$$
\beta_T(i)=P(o_T|i_T=q_i,\lambda)=1
$$
核心是根据$\beta_{t+1}(i)$求解$\beta_{t}(i)$

其中：
$$
\beta_{t+1}(i)=P(o_{t+2},o_{t+3},...,o_T|i_{t+1}=q_i,\lambda)
$$
在上一步的基础上，解
$$
\begin{aligned}
\beta_{t}(i) &= P(o_{t+1},...,o_T|i_t=q_i,\lambda) \\

&= \sum_{j=1}^N  P(o_{t+1},o_{t+2},...,o_T,i_{t+1}=q_j|i_t=q_i,\lambda) \\

&= \sum_{j=1}^N  P(i_{t+1}=q_j|i_t=q_i,\lambda)
                 P(o_{t+1},o_{t+2},...,o_T|i_t=q_i,i_{t+1}=q_j\lambda)\\

&= \sum_{j=1}^N  P(i_{t+1}=q_j|i_t=q_i,\lambda)
                 P(o_{t+1}|i_t=q_i,i_{t+1}=q_j,\lambda)
                 P(o_{t+2},...,o_T|i_t=q_i,i_{t+1}=q_j,o_{t+1},\lambda)\\

&= \sum_{j=1}^N  P(i_{t+1}=q_j|i_t=q_i,\lambda)
                 P(o_{t+1}|i_{t+1}=q_j,\lambda)
                 P(o_{t+2},...,o_T|i_{t+1}=q_j,\lambda)\\

\beta_{t}(i) &= \sum_{j=1}^N  a_{ij}
                 b_{j}(o_{t+1})
                 \beta_{t+1}(j)\\
                 
\end{aligned}
$$
