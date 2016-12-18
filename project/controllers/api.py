#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Daniel Martinez Caballero
# Description: API Controller. Method referring api-self.

from project import app
from bottle import request, HTTPResponse, auth_basic
import os, json
import auth

name = '/' + os.path.splitext(os.path.basename(__file__))[0]

@app.route(name + '/status', method='GET')
@auth_basic(auth.check_pass)
def status():
	raise HTTPResponse(status=200, body='Running')

@app.route(name + '/login', method='POST')
@auth_basic(auth.check_pass)
def login():
	csrf = str(request.environ.get('beaker.session').get('csrf_token'))
	raise HTTPResponse(status=200, body = csrf)


@app.route(name + '/status', method='POST')
@auth_basic(auth.check_pass)
def statusPost():
        #os.system('$(sleep 1; sudo service NOMBRE-PROVISIONAL restart &)')
        raise HTTPResponse(status=202, body="Running POST")


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
