# -*- coding: UTF-8 -*-
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

x_axix, y_axix = ([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80], \
                  [2.60197878712, 7.13890584287, 37.5842768761, 93.5980674622, 95.1562012795, \
                   94.4834934721, 94.868690743, 88.753104265, 71.4403334794, 61.0003937966, \
                   22.2607707641, 16.6554335691, 12.4846791859, 13.5963716609, 55.3415794682, \
                   52.8844591847, 8.78261366371])

# plt.title('TeraSort2')
plt.plot(x_axix, y_axix, color='blue', label='CPU usage')

ax = plt.gca()
ax.set_ylim(0,100)
plt.xlabel('time(sec)', fontsize=20)
plt.ylabel('CPU usage(%)', fontsize=20)
plt.show()