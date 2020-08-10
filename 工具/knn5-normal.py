import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn import neighbors
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

x_raw = x_data
y_raw = y_data

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

n_neighbors = 5

for i, weights in enumerate(['uniform', 'distance']):
    knn = neighbors.KNeighborsRegressor(n_neighbors, weights=weights)
    y_predict = knn.fit(x_train, y_train).predict(x_test)
    
    '''
    plt.subplot(2, 1, i + 1)
    plt.plot(x_test, y_test, color='darkorange', label='data')
    plt.plot(x_test, y_predict, color='navy', label='prediction')
    plt.axis('tight')
    plt.legend()
    plt.title("KNeighborsRegressor (k = %i, weights = '%s')" % (n_neighbors,
                                                                weights))
    '''
    plt.subplot(2,1,i+1)
    plt.plot(y_test, color='darkorange', label='data')
    plt.plot(y_predict,color='navy', label='prediction')
    plt.axis('tight')
    plt.legend()
    plt.title("KNeighborsRegressor (k = %i, weights = '%s')" % (n_neighbors,
                                                                weights))
plt.tight_layout()
plt.show()

with open("example.txt","w") as fo:
    for i in range(len(y_predict)):
        if abs(y_predict[i]-y_test[i]) > 100:
            fo.write("y_predict : " + str(y_predict[i]))
            fo.write("  y_true : " + str(y_test[i]))
            fo.write("  y_raw : " + str(y_raw[int(validation_rate*num)+i]))
            fo.write("  " + str(x_raw[int(validation_rate*num)+i]))
            fo.write("\n")

print (knn.score(x_test,y_test))
