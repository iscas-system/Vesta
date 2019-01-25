import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.figure()
ax = plt.gca()
y = np.random.randn(9)

# row_labels = ['CPU mean(%)', 'CPU standard deviation(%)', 'RAM mean(%)', 'RAM standard deviation(%)', 'Disk read mean(Mbps)', 'Disk read standard deviation(Mbps)', 'Disk write mean(%)', 'Disk write standard deviation(Mbps)', 'Network receive mean(Mbps)', 'Network receive standard deviation(Mbps)', 'Network send mean(Mbps)', 'Network send standard deviation(Mbps)']
# col_labels = ['5G5U-4', '8G8U-4']
# table_vals = [[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1]]
# row_colors = ['red','gold']
# my_table = plt.table(cellText=table_vals, colWidths=[0.1]*2,
#                      rowLabels=row_labels, colLabels=col_labels,
#                      loc='best')
# 
# plt.show()

a = [1,2,3,4,5]
b = ['a','b','c','d','e']
c = []
for i in range(0,len(a)):
    c.append([a[i],b[i]])
print(c)
              

