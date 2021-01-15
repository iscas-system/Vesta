"""from pribo import BayesianOptimization
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import gridspec
import sqlite3


class tools:


    __run_time__ =0
    bo = BayesianOptimization(queryTarget, {'cpu_count':(2,8),'ram':(4,16),'diskType':(0,1),'netType':(0,1),'count':(2,5)})

    def queryTarget(cpu_count,ram,diskType,netType,count):
        #con=sqlite3.connect("/Users/renjie/Desktop/priordb.sqlite")
        #cursor = con.cursor()
        #ram需要比较ram／cpu
        #cursor.execute("select total_cost from querytime where cpu_count=? and cpu_type=? and ram=? and diskType=? and count=?",(cpu_count,cpu_type,ram,diskType,count))
        #values = cursor.fetchall()
        #con.close()
        #if len(values)==0:
        #    return -1000000
        #return values[0]
        print("当前推荐配置为下所示，请反馈运行时间：\n")
        print("cpu核数: ")
        print(cpu_count)
        print(" 内存大小:")
        print(ram)
        print(" 磁盘速度:")
        print(diskType)
        print(" 网络速度:")
        print(netType)
        print(" 主机个数:")
        print(count)
        conf={
            "cpu_count":cpu_count ,
            "ram":ram,
            "diskType":diskType,
            "netType":netType,
            "count":count
        }
        response(conf)
        while(run_time==0){
            sleep(3000)
        }
        return run_time


    def set_runtime(taskID,time):
        this.__run_time__=time


    def get_new_conf(taskID,time):

        bo.maximize(init_points=3, n_iter=0, acq='ei', kappa=5)
        bo.maximize(init_points=0, n_iter=10, acq='ei', kappa=5)
        return
"""