import matplotlib.pyplot as plt
import numpy as np

x = np.array([0, 1, 2])
y1 = np.array([1, 2, 3])
y2 = np.array([3, 2, 1])

plt.bar(x, y1)
plt.bar(x, y2, bottom=y1, color='c')
plt.savefig('../img/堆积柱状图.png')