#=================================================================
# Copyright(c) Institute of Software, Chinese Academy of Sciences
#=================================================================
# Author : wuyuewen@otcaix.iscas.ac.cn
# Date   : 2016/05/25

from service import restful_api
from service.restful.driver.libvirt_driver_ext import *

#restful_api.add_resource(LibvirtNodesList, '/libvirt/<string:driver>/nodes/json')
restful_api.add_resource(Config_rec, '/source/json')
restful_api.add_resource(Showpath, '/showpath')
restful_api.add_resource(Hello, '/')
restful_api.add_resource(Train, '/train')
restful_api.add_resource(Create, '/create')


