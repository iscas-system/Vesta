# -*- coding: UTF-8 -*-
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

x_axix, y_axix = ([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60], \
                  [0.420370614796, 0.48085765216, 5.79479907351, 71.2058056378, 92.033746404, \
                   97.5063411517, 97.2034118036, 80.5533931194, 87.8963686356, 55.5401329676, \
                   30.1996298922, 83.9703292259, 36.5689244815])

# plt.title('SQL Aggregation2')
plt.plot(x_axix, y_axix, color='blue', label='CPU usage')

ax = plt.gca()
ax.set_ylim(0,100)
plt.xlabel('time(sec)', fontsize=20)
plt.ylabel('CPU usage(%)', fontsize=20)
plt.show()