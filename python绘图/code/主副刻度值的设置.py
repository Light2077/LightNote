import matplotlib.pyplot as plt
import numpy as np
fig, ax = plt.subplots()

x = np.linspace(-10, 10, 100)
y = np.sin(x)

ax.plot(x, y)

ax.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)

plt.show()