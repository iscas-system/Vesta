'''
Created on 2017

@author: Frankee
'''

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import  MultipleLocator
  
def sgn(value):
    if value < 5:
        return 11.5  
    if value > 5 and value <= 14:
        return 13
    elif value > 14:
        return 15
    
def sgn1(value):
    if value < 2:
        return 10.2  
    if value > 2 and value <= 6:
        return 10.6
    elif value > 6 and value <= 9:
        return 12.2
    elif value > 9 and value <= 15:
        return 13.2
    elif value > 15:
        return 14.6

plt.figure(figsize=(6,4))  
x = np.linspace(0, 20, 100)  
y = np.array([]) 
y1 = np.array([]) 
for a in x:  
    y = np.append(y,np.linspace(sgn(a),sgn(a),1))  
    y1 = np.append(y1,np.linspace(sgn1(a),sgn1(a),1))
l=plt.plot(x,y,'b',label='Optimal')  
l1=plt.plot(x,y1,'r',label='CherryPick') 

ax = plt.gca()
ax.spines['right'].set_color('none')  
ax.spines['top'].set_color('none') 
# ax.spines['bottom'].set_position(('data', 9))  
# ax.spines['left'].set_position(('data',3)) 
xLocator = MultipleLocator(5)
yLocator = MultipleLocator(0.5)
ax.set_xlim(0,20)  
ax.set_ylim(10,16)
ax.xaxis.set_major_locator(xLocator)
ax.yaxis.set_major_locator(yLocator)

ax.set_xlabel('Generation')
ax.set_ylabel('Optimum')
ax.xaxis.set_ticks_position('bottom')  
ax.yaxis.set_ticks_position('left')  

plt.legend()

plt.show()