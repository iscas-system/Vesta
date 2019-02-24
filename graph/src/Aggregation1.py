# -*- coding: UTF-8 -*-
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

x_axix, y_axix = ([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60], \
                  [0.58176863976, 0.52295142987, 5.29972582907, 45.2583357809, 94.9551447501, \
                   97.2922307133, 86.1594183546, 83.9437328666, 88.4811088028, 63.2328891243, \
                   50.7499801132, 77.7526164099, 31.9677509236])

# plt.title('SQL Aggregation1')
plt.plot(x_axix, y_axix, color='blue', label='CPU usage')

ax = plt.gca()
ax.set_ylim(0,100)
plt.xlabel('time(sec)', fontsize=20)
plt.ylabel('CPU usage(%)', fontsize=20)
plt.show()