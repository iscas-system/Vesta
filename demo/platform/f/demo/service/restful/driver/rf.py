import os
import numpy as np
from sklearn import neighbors,svm,tree
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error,mean_absolute_error
import joblib
import pandas as pd
import pydotplus

def train(d):
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

    ####
    filename = os.path.join(dir_path,"data.txt")
    file = open(filename,'r')

    x_data = []
    y_data = []
    num = 0
    _min = 100000
    _max = 0


    for eachline in file:
        eachline = eachline.split(os.linesep)[0]
        data = eachline.split(',')
        y_data.append(float(data[0]))
        if float(data[0])>_max:
            _max = float(float(data[0]))
        if float(data[0])<_min:
            _min = float(float(data[0]))
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

    x_raw = x_data
    y_raw = y_data

    x_wl = []
    x_fw = []
    x_dz = []
    x_vt = []

    for i in range(len(y_data)):
        x_wl.append(x_data[i][0])
        x_fw.append(x_data[i][1])
        x_dz.append(x_data[i][2])
        x_vt.append(x_data[i][3])

    y_data = np.array(y_data,dtype=np.float32)
    xmeans = np.mean(x_data,0)
    xvar = np.var(x_data,0)
    x_data = (x_data - xmeans) / xvar
    ymean = np.mean(y_data)
    y_data = (y_data - _min)/(_max - _min)
    std_data = np.concatenate((xmeans,xvar),axis=0)
    dir_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(dir_path,"std.npy")
    np.save(filename,std_data)

    validation_rate = 0.8
    x_train = x_data[0:int(validation_rate*num)]
    y_train = y_data[0:int(validation_rate*num)]
    x_test = x_data[int(validation_rate*num):]
    y_test = y_data[int(validation_rate*num):]

    '''
    x_train = []
    x_test = []
    y_train = []
    y_test = []



    for i in range(len(y_data)):
        if x_fw[i] == 2.0:
            x_test.append(x_data[i])
            y_test.append(y_data[i])
        if x_fw[i] == 0.0:
            x_train.append(x_data[i])
            y_train.append(y_data[i])
    '''

    x_train = np.array(x_train,dtype=np.float32)
    x_test = np.array(x_test,dtype=np.float32)
    y_train = np.array(y_train,dtype=np.float32)
    y_test = np.array(y_test,dtype=np.float32)

    clf = RandomForestRegressor(n_estimators=5,max_leaf_nodes=30)
    clf.fit(x_train,y_train)
    y_predict = clf.predict(x_test)
    joblib.dump(clf, os.path.join(dir_path,"train_model.m"))
    Estimators = clf.estimators_
    for index, model in enumerate(Estimators):
        filename = os.path.join(dir_path,'randomforest_' + str(index) + '.png')
        dot_data = tree.export_graphviz(model , out_file=None,feature_names=["workload","framework","datasize","vmtype","cpu_num","memory","average_cpu","average_memory","average_disk"],filled=True,rounded=True,special_characters=True)
        graph = pydotplus.graph_from_dot_data(dot_data)
        graph.write_png(filename)
        g = list()
        edges_done = set()
        edge_obj_dicts = list()
        for e in graph.obj_dict['edges'].values():
            edge_obj_dicts.extend(e)
        if edge_obj_dicts:
            edge_src_set, edge_dst_set = list(zip(*[obj['points'] for obj in edge_obj_dicts]))
            edge_src_set, edge_dst_set = set(edge_src_set), set(edge_dst_set)
        else:
            edge_src_set, edge_dst_set = set(), set()
        node_obj_dicts = list()
        for e in graph.obj_dict['nodes'].values():
            node_obj_dicts.extend(e)
        sgraph_obj_dicts = list()
        for sg in graph.obj_dict['subgraphs'].values():
            sgraph_obj_dicts.extend(sg)
        obj_list = sorted([(obj['sequence'], obj)for obj in (edge_obj_dicts + node_obj_dicts + sgraph_obj_dicts)])
        
        for idx, obj in obj_list:
            if obj['type'] == 'node':
                node = pydotplus.graphviz.Node(obj_dict=obj)
                if graph.obj_dict.get('suppress_disconnected', False):
                    if (node.get_name() not in edge_src_set and node.get_name() not in edge_dst_set):
                        continue
                if 'label' in node.obj_dict['attributes'].keys():
                    g.append(node.obj_dict['name']+node.obj_dict['attributes']['fillcolor']+node.obj_dict['attributes']['label'] + '\n')
            elif obj['type'] == 'edge':
                edge = pydotplus.graphviz.Edge(obj_dict=obj)
                
                if graph.obj_dict.get('simplify', False) and edge in edges_done:
                    continue
                
                g.append(edge.to_string() + '\n')
                edges_done.add(edge)
            else:
                pass
                #sgraph = pydotplus.graphviz.Subgraph(obj_dict=obj)
                #g.append(sgraph.to_string() + '\n')
        with open(os.path.join(dir_path,'randomforest_'+ str(index) + '.txt'),'w') as f:
            f.write(''.join(g))


    print ( 'mae:%.4f' %(mean_absolute_error(y_predict,y_test) ) )
    print ( 'rmse:%.4f' %(np.sqrt(mean_squared_error(y_predict,y_test)) ) )
