#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Daniel Martinez Caballero
# Description: API Controller. Method referring api-self.

from project import app
from bottle import request, HTTPResponse, HTTPError, auth_basic, response
import os, json
import auth

name = '/' + os.path.splitext(os.path.basename(__file__))[0]


@app.route(name, method='GET')
def check():
        return "<a href=\"javascript:window.history.go(-1);\">Running! Click here to go back</a>"



@app.route(name + '/login', method='POST')
def login():
	csrf = str(request.environ.get('beaker.session').get('csrf_token'))
	data = request.body.read()
        result = json.loads(data)
	print result['key']
	if str(result['key']) == "admin":
		return csrf
	else:
		return HTTPError(401, "Unauthorized")



@app.route(name + '/restart', method='PUT')
@auth_basic(auth.check_pass)
def restart():
	#os.system('$(sleep 1; sudo service NOMBRE-PROVISIONAL restart &)')
	raise HTTPResponse(status=202)


@app.route(name + '/update', method='PUT')
@auth_basic(auth.check_pass)
def update():
	raise HTTPResponse(status=202)
	#git pull REPOSITORIO
	#restart()


