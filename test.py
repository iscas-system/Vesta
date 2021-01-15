import requests

#初始化，获得初始化配置方案
ip = "http://133.133.133.124:10141"
#get init config
init_conf_respon = requests.get(ip)
print(init_conf_respon.content)

#训练阶段，发起put请求,返回新的配置方案
conf={
    "count": "3.0",
    "cpu_count": "2.0",
    "diskType": "0.0",
    "netType": "0.0",
    "ram": "10.0",
    "time": "2123"
}
new_conf_response = requests.put(ip,data=conf)
print(new_conf_response.content)
