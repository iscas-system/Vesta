import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

x = np.arange()
y = np.arange()
x,y = np.meshgrid(x,y)

f = np.abs(x) + np.abs(y) - 1
plt.figure()
