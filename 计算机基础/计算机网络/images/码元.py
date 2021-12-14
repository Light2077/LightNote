import matplotlib.pyplot as plt 
import numpy as np

x = [0, 1, 2, 3 ,4, 5, 6, 7, 8]
y1 = [0, 0, 1, 1, 0, 1, 0, 1, 1]
y2 = [0, 1, 2, 3, 1, 0, 2, 1, 0]

fig, ax = plt.subplots(1, 2, figsize=(10, 4), sharey=True)

ax[0].set_ylim(-1, 4)
ax[0].step(x, y1, where='pre')
for i in range(1, len(x)):
	ax[0].text(x[i]-0.5, y1[i], y1[i], ha='center', va='bottom')
	ax[1].text(x[i]-0.5, y2[i], y2[i], ha='center', va='bottom')
ax[1].step(x, y2, where='pre')

ax[0].set_title('2进制码元(1bit)', fontfamily='STSong')
ax[1].set_title('4进制码元(1bit)', fontfamily='STSong')
plt.savefig("码元.png")
plt.show()