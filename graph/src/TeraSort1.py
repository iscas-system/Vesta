# -*- coding: UTF-8 -*-
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

x_axix, y_axix = ([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95], \
                  [2.21920467634, 5.23184404513, 78.8317498816, 95.6000555238, 95.4316520708, \
                   94.8626614414, 91.7916594579, 83.3021292287, 63.1938662903, 38.1201758195, \
                   17.3430512678, 13.9526679426, 10.1035629741, 6.77735045293, 37.276866942, \
                   62.3035169354, 13.2706149128, 3.92855102504, 3.6345708781, 4.3882742157])

# plt.title('TeraSort1')
plt.plot(x_axix, y_axix, color='blue', label='CPU usage')

ax = plt.gca()
ax.set_ylim(0,100)
plt.xlabel('time(sec)', fontsize=20)
plt.ylabel('CPU usage(%)', fontsize=20)
plt.show()