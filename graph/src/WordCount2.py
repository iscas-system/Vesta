# -*- coding: UTF-8 -*-
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

x_axix, y_axix = ([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85], \
                  [4.02221641992, 21.7108930804, 94.5883810123, 95.8777321803, 97.0039559388, \
                   98.8167784599, 98.8414481094, 98.621969605, 97.8381439017, 97.5728525132, \
                   96.1475861253, 95.2805617844, 94.7021281828, 93.9564399797, 91.9431861004, \
                   88.2343862583, 63.5286092895, 25.6417162963])

# plt.title('WordCount2')
plt.plot(x_axix, y_axix, linewidth = '1', label = "CPU usage", color='#000000', marker='x')

ax = plt.gca()
ax.set_ylim(0,100)
plt.xlabel('time(sec)', fontsize=20)
plt.ylabel('CPU usage(%)', fontsize=20)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.show()