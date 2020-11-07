import matplotlib.pyplot as plt 
import numpy as np
fig, ax = plt.subplots(1, 2, figsize=(10, 4))

x1 = np.linspace(0, 10, 100)
y1 = np.sin(x1)

ax[0].plot(x1, y1)
ax[0].set_title('模拟信号', fontfamily='STSong')

x2 = np.arange(8)
y2 = [0, 1, 1, 0, 1, 0, 0, 1]

ax[1].step(x2, y2)
ax[1].set_title('数字信号', fontfamily='STSong')
ax[1].set_ylim(-1, 3)
plt.tight_layout()
plt.savefig('模拟信号和数字信号.png')