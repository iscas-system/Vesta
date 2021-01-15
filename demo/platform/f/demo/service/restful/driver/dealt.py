#0<average_memory &le; 0.037<br/>mse = 0.014<br/>samples = 5002<br/>value = 0.078>
#0 -> 1  [headlabel="True", labelangle=45, labeldistance="2.5"];
import os
import json
from flask import jsonify

tree_num = 5
dir_path = os.path.dirname(os.path.abspath(__file__))

def partition(arr,low,high):
    i = ( low-1 )         # 最小元素索引
    pivot = arr[high]['name']
    
    for j in range(low , high):
        
        # 当前元素小于或等于 pivot
        if   arr[j]['name'] < pivot:
            
            i = i+1
            arr[i],arr[j] = arr[j],arr[i]

    arr[i+1],arr[high] = arr[high],arr[i+1]
    return ( i+1 )


# arr[] --> 排序数组
# low  --> 起始索引
# high  --> 结束索引

# 快速排序函数
def quickSort(arr,low,high):
    if low < high:
        
        pi = partition(arr,low,high)
        
        quickSort(arr, low, pi-1)
        quickSort(arr, pi+1, high)

def draw(tree,node,i,tag):
    tree.append({})
    l = len(tree)
    tree[l-1]['paramter'] = {}
    if node[i]['kind'] == 1:
        tree[l-1]['children'] = []
        tree[l-1]['paramter']['line'] = node[i]['judge'] + ' <= ' + str(node[i]['judgenum'])
        draw(tree[l-1]['children'],node,node[i]['lson'],1)
        draw(tree[l-1]['children'],node,node[i]['rson'],2)
    tree[l-1]['name'] = str(i)
    tree[l-1]['paramter']['samples'] = str(node[i]['samples'])
    tree[l-1]['paramter']['mse'] = str(node[i]['mse'])
    tree[l-1]['paramter']['value'] = str(node[i]['value'])
    tree[l-1]['tag'] = tag
    tree[l-1]['color'] = node[i]['color']


def f(nn,x):
    filename=os.path.join(dir_path,"randomforest_" + str(nn) + ".txt")
    fi = open(filename)
    line = fi.readlines()
    node = []
    num = 0
    edge = []
    cnt = 0
    f = -1
    root = 0
    for eachline in line:
        eachline = eachline.split('\n')[0]
        if eachline[0] == 'n' or eachline[0] == 'e':
            pass
        else:
            if eachline.find('->') != -1:
                edge.append([])
                if eachline.find("True") != -1 :
                    f = 1
                    eachline = eachline.split('  [')[0]
                elif eachline.find("False") != -1 :
                    f = 0
                    eachline = eachline.split('  [')[0]
                else:
                    eachline = eachline.split(';')[0]
                edge[cnt].append(int(eachline.split( ' -> ' )[0]))
                edge[cnt].append(int(eachline.split( ' -> ' )[1]))
                edge[cnt].append(f)
                cnt += 1
            else:
                node.append({})
                eachline = eachline.split('<br/>')
                if len(eachline) == 4:
                    tt = ((eachline[0].split('<'))[0])
                    node[num]['name'] = int(tt.split('"')[0])
                    node[num]['color'] = tt.split('"')[1]
                    tmp = (eachline[0].split('<'))[1]
                    node[num]['judgenum'] = float(tmp.split(' &le; ')[1])
                    node[num][(eachline[1].split(' = '))[0]] = float((eachline[1].split(' = '))[1])
                    node[num][(eachline[2].split(' = '))[0]] = float((eachline[2].split(' = '))[1])
                    node[num][(eachline[3].split(' = '))[0]] = float((eachline[3].split(' = '))[1][:-1])
                    node[num]['judge'] = tmp.split(' &le; ')[0]
                    node[num]['kind'] = 1
                else:
                    tt = ((eachline[0].split('<'))[0])
                    node[num]['name'] = int(tt.split('"')[0])
                    node[num]['color'] = tt.split('"')[1]
                    tmp = (eachline[0].split('<'))[1]
                    node[num][tmp.split(' = ')[0]] = float(tmp.split(' = ')[1])
                    node[num][(eachline[1].split(' = '))[0]] = float((eachline[1].split(' = '))[1])
                    node[num][(eachline[2].split(' = '))[0]] = float((eachline[2].split(' = '))[1][:-1])
                    node[num]['kind'] = 0
                num += 1
    fi.close()

    features =["workload","framework","datasize","vmtype","cpu_num","memory","average_cpu","average_memory","average_disk"]
    quickSort(node,0,num-1)
    for i in range(cnt):
        father = edge[i][0]
        son = edge[i][1]
        if 'lson' not in node[father].keys():
            node[father]['lson'] = son
        else:
            node[father]['rson'] = son
    path = []
    path.append(0)
    while(True):
        cur = path[len(path)-1]
        if node[cur]['kind'] == 0:
            break
        judge = node[cur]['judge']
        judgenum = node[cur]['judgenum']
        if x[features.index(judge)] <= judgenum:
            path.append(node[cur]['lson'])
        else:
            path.append(node[cur]['rson'])
    tree = []
    draw(tree,node,0,0)
    plen = len(path)
    linkpath = {}
    for i in range(plen):
        linkpath[str(i)] = path[i]
    return tree[0],linkpath


def show(input):
    filename = os.path.join(dir_path,"tag.txt")
    file = open(filename,'r')
    digit = {}
    for eachline in file:
        eachline = eachline.split(os.linesep)[0]
        eachline = eachline.split(":")
        digit[eachline[0]]=eachline[1]
    
    file.close()
    x = []
    x.append(float(digit[input[0]]))
    x.append(float(digit[input[1]]))
    x.append(float(digit[input[2]]))
    x.append(float(digit[input[3]]))
    for i in range(4,9):
        x.append(float(input[i]))
    data = [[],[]]
    for i in range(tree_num):
        t,p = f(i,x)
        data[0].append(t)
        data[1].append(p)
    dict = {}
    dict['code'] = 20000
    dict['data'] = data
    json_str =jsonify(dict)
    return json_str


