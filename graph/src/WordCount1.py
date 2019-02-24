# -*- coding: UTF-8 -*-
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

x_axix, y_axix = ([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115], \
                  [3.70075450712, 12.4189788614, 82.6159518155, 92.2524815805, 96.2176988313, \
                   98.339527149, 98.5521948009, 98.3639293412, 98.0092589479, 96.9282231501, \
                   97.1735113233, 97.1976707546, 98.2333817868, 97.4457436596, 97.8212781127, \
                   95.3601444449, 94.2421471087, 92.1548280072, 74.6895519298, 60.2358534182, \
                   39.3640758677, 30.071745413, 20.5946219628, 25.1616941979])

# plt.title('WordCount1')
plt.plot(x_axix, y_axix, linewidth = '1', label = "CPU usage", color='black', marker='x')

ax = plt.gca()
ax.set_ylim(0,100)
plt.xlabel('time(sec)', fontsize=20)
plt.ylabel('CPU usage(%)', fontsize=20)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.show()