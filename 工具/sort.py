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

for i in range(len(y_data)-1):
    for j in range(len(y_data)-i-1):
        if x_data[i][0]>x_data[j+i+1][0]:
            tmp = x_data[i]
            x_data[i]= x_data[j+i+1]
            x_data[j+i+1] = tmp
            ytmp = y_data[i]
            y_data[i] = y_data[j+i+1]
            y_data[j+i+1] = ytmp

for i in range(len(y_data)-1):
    for j in range(len(y_data)-i-1):
        if x_data[i][0] == x_data[j+i+1][0] and y_data[i] > y_data[j+i+1]:
            tmp = x_data[i]
            x_data[i]= x_data[j+i+1]
            x_data[j+i+1] = tmp
            ytmp = y_data[i]
            y_data[i] = y_data[j+i+1]
            y_data[j+i+1] = ytmp

with open("data-sorted.txt","w") as fo:
    for i in range(len(y_data)):
        fo.write(str(y_data[i]))
        fo.write(" : ")
        fo.write(str(x_data[i]))
        fo.write("\n")
