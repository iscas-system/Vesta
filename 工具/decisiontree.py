import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn import neighbors,svm,tree
import pandas as pd

filename = "data.txt"
file = open(filename,'r')

x_data = []
y_data = []
num = 0

for eachline in file:
    eachline = eachline.split(os.linesep)[0]
    data = eachline.split(',')
    y_data.append(float(data[0]))
    x_data.append([])
    for i in range(len(data)-1):
        x_data[num].append(float(data[i+1]))
    num = num + 1
file.close()

xmeans = np.mean(x_data,0)
xvar = np.var(x_data,0)
x_data = (x_data - xmeans) / xvar
ymean = np.mean(y_data)
y_data = y_data - ymean

validation_rate = 0.8
x_train = x_data[0:int(validation_rate*num)]
y_train = y_data[0:int(validation_rate*num)]
x_test = x_data[int(validation_rate*num):]
y_test = y_data[int(validation_rate*num):]

x_train = np.array(x_train,dtype=np.float32)
x_test = np.array(x_test,dtype=np.float32)
y_train = np.array(y_train,dtype=np.float32)
y_test = np.array(y_test,dtype=np.float32)

clf = tree.DecisionTreeRegressor()
clf.fit(x_train,y_train)
y_predict = clf.predict(x_test)

plt.plot(y_test, color='darkorange', label='data')
plt.plot(y_predict,color='navy', label='prediction')
plt.axis('tight')
plt.legend()
plt.tight_layout()
plt.show()

print (clf.score(x_test,y_test))
