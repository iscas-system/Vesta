#coding=utf-8
import time, os.path, sys
from flask import Flask, request, g, make_response, url_for
from config import GLOBAL
from flask import Flask
from flask_restful import Resource, Api
from pribo.bayesian_optimization import *

app = Flask(__name__)
api = Api(app)

bo = BayesianOptimization(pbounds={'cpu_count':(2,8),'ram':(4,16),'diskType':(0,1),'netType':(0,1),'count':(2,5)})

is_init = False


class PriBO(Resource):

    def get(self,init_points):
        conf=init_pribo(init_points)
        print 'conf is'
        print conf
        return conf

    def delete(self,taskID):
        return None

    def put(self,conf,times):
        run_pribo(times)
        return {conf}



api.add_resource(PriBO, '/<int:init_points>')


def init_pribo(init_points):
    rand_points = bo.space.random_points(init_points)
    #bo.init_points.extend(rand_points)
    conflist=[]
    for data in rand_points:
        conflist.append(bo.conf_diction(data))
    return conflist

def run_pribo(conf,times):
    global is_init
    if  is_init == False :
        for x,y in times:
            conf = bo.space.dic_to_conf(x)
            bo.init(conf,y)
        is_init = True
        return bo.nex_max()
    else:
        return bo.compute(conf,time)








if __name__ == '__main__':
    app.run(host=GLOBAL.get('HOST'), port=int(GLOBAL.get('Port')), debug=True)
