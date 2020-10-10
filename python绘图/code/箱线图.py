import matplotlib.pyplot as plt
import numpy as np

np.random.seed(2020)
x = np.random.normal(size=100)

plt.boxplot(x)
plt.savefig('../img/箱线图.png')