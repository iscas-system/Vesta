# Apollo
## Introduction
CloudZond - a tool for picking the best cloud configuration for big data analytics jobs running on clouds. Cloud configuration cotains the VM type (for example ec2.a1.large in Amazon EC2) and the number VM instances. The models we support for picking the best cloud configuration include Bayesian Optimizaion (BO) and Random Forest (RF).

**Copyright: Institute of Software, Chinese Academy of Sciences**

**Contact: wuyuewen@otcaix.iscas.ac.cn**

## Paper

- Yuewen Wu, Heng Wu, Wenbo Zhang, Yuanjia Xu, Jun Wei, Hua Zhong: HW3C: A Heuristic based Workload Classification and Cloud Configuration Approach for Big Data Analytics. Internetware 2018: 8:1-8:10
- Yuewen WU, Yuanjia XU, Heng WU, Lingang SU, Wenbo ZHANG, Hua ZHONG, Apollo: Rapidly Picking the Optimal Cloud Configurations for Big Data Analytics using a Data-Driven Approach. journal of computer science and technology. Accepted

## How to run
1. Download the project to local environment. Require python 2.7 at least.
2. Execute ```python run.py``` to run the server.
3. Use RESTful API to select the next cloud configuration.

## Interfaces

**Initialization**

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


**Set a configuration**

_**PUT**_: http://URL/pribo/

   _parameters：_
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

## Quick start


Do following steps to select the best cloud configuration.
```
Client:
Send Initialization request to server.
Server:
Randomly selecting 3 different cloud configurations to initialize the process, reture the details of configurations.
Client:
Running the job using those 3 cloud configurations, put the job running time to server.
Server:
Training the model using BO or RF model, then return the next cloud configuration which will achieve optimal job running time.
Client:
Apply the new cloud configuration, and feedback the job running time to server.
Server:
Keep on training the model with new data, until the result is confidence enough to be the best.
End.
```
