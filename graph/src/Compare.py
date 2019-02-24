import numpy as np
import matplotlib.pyplot as plt
size = 5
a = 2.3
b = 3.3
c = 3.5
x = np.arange(size)

total_width, n = 0.8, 3
width = total_width / n
x = x - (total_width - width) / 2

plt.bar(x, a,  width=width, label='a')
plt.bar(x + width, b, width=width, label='b')
plt.bar(x + 2 * width, c, width=width, label='c')
plt.legend()
plt.show()