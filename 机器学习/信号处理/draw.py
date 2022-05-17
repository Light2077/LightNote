# 绘图脚本


import matplotlib.pyplot as plt 
import numpy as np


plt.figure(figsize=(10, 1))
x = np.linspace(0, 10 * np.pi, 100)
y = np.sin(x)
plt.plot(y, lw=5, alpha=.3, color='g')
plt.xticks([])
plt.yticks([])
plt.savefig('./images/原始信号.png')

# 帧1 2 3
for i, start in enumerate([0, 25, 50]):
	plt.figure(figsize=(5, 1))
	plt.plot(y[start:start+50], lw=5, alpha=.3, color='g')
	plt.xticks([])
	plt.yticks([])
	plt.savefig(f'./images/帧{i+1}.png')