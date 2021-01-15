import os
import numpy as np
from sklearn import neighbors,svm,tree
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error,mean_absolute_error
import joblib
import pandas as pd
import json
from flask import jsonify
import time
import service.restful.driver.detect as detect
import service.restful.driver.prom_csv as pc


vm_type ={
    'r3.2xlarge':14,
    'm3.2xlarge':10,
    'r3.xlarge':8,
    'c3.2xlarge':1,
    'm3.xlarge':2,
    'r4.large':0,
    'c4.xlarge':3,
    'c4.large':15,
    'm4.large':5,
    'c3.xlarge':11,
    'r4.xlarge':17,
    'm3.large':13,
    'r3.large':16,
    'm4.2xlarge':7,
    'm4.xlarge':12,
    'c4.2xlarge':4,
    'r4.2xlarge':6,
    'c3.large':9
}

def create(data):
    dir_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(dir_path,"tag.txt")
    file = open(filename,'r')
    digit = {}
    input_v = []
    for eachline in file:
        eachline = eachline.split(os.linesep)[0]
        eachline = eachline.split(":")
        digit[eachline[0]]=eachline[1]
    
    file.close()
    for i in range(4):
        input_v.append( digit[ data[i] ] )
    for i in range(4,6):
        input_v.append( data[i] )
    name = data[0]
    os.system("kubectl apply -f /home/test/" + name + ".yaml")
    t = time.time()
    endt = detect.main(name)
    
    pc.main( input_v,t,endt)
    os.system( "kubectl delete sparkapplication " + name )


def yamlmaker(data,index,pred):
    dict = {}
    dict['code'] = 20000
    dict['data'] = []
    for i in range(len(index)):
        dict['data'].append({})
        vm = data[index[i]][3]
        for key in vm_type.keys():
            if vm_type[key] == vm:
                dict['data'][i]['workload'] = key
                dict['data'][i]['sort'] = i
                dict['data'][i]['pred'] = pred[index[i]]
    #os.system("kubectl apply -f /home/test/node.yaml")
    json_str =jsonify(dict)
    return json_str

def clf_rec(input):
    dir_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(dir_path,"vminfo.txt")
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

    filename = os.path.join(dir_path,"tag.txt")
    file = open(filename,'r')
    digit = {}
    for eachline in file:
        eachline = eachline.split(os.linesep)[0]
        eachline = eachline.split(":")
        digit[eachline[0]]=eachline[1]

    file.close()
    
    filename = os.path.join(dir_path,"std.npy")
    std_data = np.load(filename)
    x_test = []
    num = 0
    for key in vm_type.keys():
        x_test.append([])
        x_test[num].append(digit[input['workload']])
        x_test[num].append(digit[input['framework']])
        x_test[num].append(digit[input['datasize']])
        x_test[num].append(digit[key])
        for j in range(len(vminfo)):
            if vminfo[j][0] == x_test[num][3]:
                for k in range(len(vminfo[j])-1):
                    x_test[num].append(float(vminfo[j][k+1]))
        for i in range(3):
            x_test[num].append(0)
        num += 1

    x_test = np.array(x_test,dtype=np.float32)
    #xmeans = np.mean(x_test,0)
    xmeans = std_data[0]
    xvar = std_data[1]
    #xvar = np.var(x_test,0)
    x_test = (x_test - xmeans) / xvar

    filename = os.path.join(dir_path,"train_model.m")
    clf = joblib.load(filename)
    y_predict = clf.predict(x_test)
    best_cfg = np.argsort(y_predict)
    return yamlmaker(x_test+xmeans,best_cfg,y_predict)
