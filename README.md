# chameleon
### 客户端：
使用服务的客户端
### 服务端：
提供配置选择的web服务端，以HTTP请求为接口进行交互

-----


##接口说明
**初始化：**
_**GET**_: http://URL/pribo
**_RESPONSE_**:
```
  {
    'count':X,
    'ram':X,
    'cpu_count':X,
    'netType':X,
    'diskType':X
  }
```


**发送运行数据给服务器：**
_**PUT**_: http://URL/pribo/
   _参数：_
```
  {
    'count':X,
    'ram':X,
    'cpu_count':X,
    'netType':X,
    'diskType':X,
    'time':X
  }
```
_**RESPONSE**:_
```
  {
    'count':X,
    'ram':X,
    'cpu_count':X,
    'netType':X,
    'diskType':X
  }
```

---

##请求流程


客户端发起Http请求。流程如下
C:
向服务器URL发起Get请求
S:
Server收到Get请求，判定为新的任务，进行初始化流程，随机根据可选配置方案，Response三个随机配置
C:
收到三个随机配置后，分别在这三种配置下运行任务，获得各种的任务运行时间。将三组数据以PUT形式发给Server
S:
S收到数据后，训练模型，利用AC函数选择新配置方案，返回给Client
C:
收到新配置后，运行，获得时间，再Put给Server
S:
收到数据后，训练模型，利用AC选择新配置方案，返回给Client
……循环
C：
觉得优化够了，发送Delete请求给Server
S：
收到Delete请求，认定结束此任务的配置优化
OVER

> [更多说明](http://pboa.mydoc.io/)