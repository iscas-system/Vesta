#=================================================================
# Copyright(c) Institute of Software, Chinese Academy of Sciences
#=================================================================
# Author : wuyuewen@otcaix.iscas.ac.cn
# Date   : 2016/05/25

from flask_restful.representations.json import output_json
from flask import request
from flask_restful import Resource, abort
import json
import service.restful.driver.backend as backend
import service.restful.driver.dealt as dealt
import service.restful.driver.rf as rf

from service import app

log = app.logger

__all__ = [
        "Config_rec",
        "Hello",
        "Showpath",
        "Train",
        "Create",
           ]

class Config_rec(Resource):
    def post(self):
        try:
            data =json.loads(request.get_data(as_text=True))
            return backend.clf_rec(data)
        except ValueError:
            abort(400, message="bad parameter")

class Showpath(Resource):
    def post(self):
        try:
            data =json.loads(request.get_data(as_text=True))
            return dealt.show(data)
        except ValueError:
            abort(400, message="bad parameter")

class Train(Resource):
    def post(self):
        try:
            data =json.loads(request.get_data(as_text=True))
            return rf.train(data)
        except ValueError:
            abort(400, message="bad parameter")

class Create(Resource):
    def post(self):
        try:
            data =json.loads(request.get_data(as_text=True))
            return backend.create(data)
        except ValueError:
            abort(400, message="bad parameter")

class Hello(Resource):
    def get(self):
        try:
            return 'Hello,World!'
        except ValueError:
            abort(400, message="bad parameter")
