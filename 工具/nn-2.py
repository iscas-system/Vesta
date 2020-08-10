import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn import neighbors,svm,tree
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense,Dropout


filename = "vminfo.txt"
file = open(filename,'r')

vminfo = []
cnt = 0

for eachline in file:
    eachline = eachline.split(os.linesep)[0]
    eachline = eachline.split(": ")[1]
    eachline = eachline.split(",")
    vminfo.append([])
    for j in range(len(eachline)):
        vminfo[cnt].append(eachline[j])
    cnt =cnt + 1
file.close()


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
        if i != 3:
            x_data[num].append(float(data[i+1]))
        else:
            x_data[num].append(float(data[i+1]))
            for j in range(len(vminfo)):
                if vminfo[j][0] == data[i+1]:
                    for k in range(len(vminfo[j])-1):
                        x_data[num].append(float(vminfo[j][k+1]))
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

model = Sequential()
model.add(Dense(10,input_shape=(9,)))
model.add(Dense(20))
model.add(Dropout(0.4))
model.add(Dense(20))
model.add(Dense(20))
model.add(Dense(20))
model.add(Dense(20))
model.add(Dense(20))
model.add(Dense(20))
model.add(Dense(20))
model.add(Dense(20))
model.add(Dense(10))
model.add(Dropout(0.4))
model.add(Dense(1))

model.compile(loss='mse', optimizer='adam')


model.fit(x_train,y_train,batch_size=64,epochs=30,validation_split=0.1)
y_predict = model.predict(x_test)

plt.plot(y_test, color='darkorange', label='data')
plt.plot(y_predict,color='navy', label='prediction')
plt.axis('tight')
plt.legend()
plt.tight_layout()
plt.show()

print (model.evaluate(x_test,y_test))
