#coding=utf-8
import time, os.path, sys
from flask import Flask, request, g, make_response, url_for
from config import GLOBAL
from flask import Flask
from flask_restful import Resource, Api,reqparse
from pribo.bayesian_optimization import *

app = Flask(__name__)
api = Api(app)

#BOA算法
bo = BayesianOptimization(pbounds={'cpu_count':(2,8),'ram':(4,16),'diskType':(0,1),'netType':(0,1),'count':(2,5)})
#初始化点的个数选择
init_point_size= GLOBAL.get('INIT_POINT')

init_flag=False

parser = reqparse.RequestParser()
parser.add_argument('count')
parser.add_argument('ram')
parser.add_argument('cpu_count')
parser.add_argument('time')
parser.add_argument('netType')
parser.add_argument('diskType')

class PriBO(Resource):
    #初始化步骤调用get方法
    def get(self):
        conf=init_pribo(GLOBAL.get('INIT_POINT'))
        print 'conf is'
        print conf
        return conf

    def delete(self,init_points):
        return None
    #训练阶段调用Put方法，接收配置方案以及对应的运行时间
    def put(self):
        args = parser.parse_args()
        print("put recived")
        conf={}
        conf['count']=args['count']
        conf['ram']=args['ram']
        conf['cpu_count']=args['cpu_count']
        time=int(args['time'])
        conf['netType']=args['netType']
        conf['diskType']=args['diskType']
        if conf==None:
            return "No recive"
        return run_pribo(conf,time)

def init_pribo(init_points):
    #随机产生初始化点。如果需要对初始选点做一些先验判断之类的操作，可以在此函数中处理
    rand_points = bo.space.random_points(init_points)
    #bo.init_points.extend(rand_points)
    conflist=[]
    for data in rand_points:
        conflist.append(bo.conf_diction(data))
    return conflist

def run_pribo(conf_with_time,time):
    conf= bo.space.dic_to_conf(conf_with_time)
    global init_point_size
    global init_flag
    if   init_point_size != 0 and init_flag == False:
        app.logger.info("--Init --")
        bo.init(conf,time)
        init_point_size -= 1
    else:
        if init_point_size==0 or init_flag:
            app.logger.info("--Begin Training --")
            if init_flag == False:
                init_flag = True
            init_point_size -=1
            newconf=bo.newMax()
            return bo.conf_diction(newconf)
        return bo.conf_diction(bo.compute(conf,time).tolist())


api.add_resource(PriBO, '/pribo')



if __name__ == '__main__':
    app.run(host=GLOBAL.get('HOST'), port=int(GLOBAL.get('Port')), debug=True)
