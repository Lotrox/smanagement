#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Daniel Martinez Caballero
# Description: API Controller. Method referring api-self.

from project import app
from bottle import request, HTTPResponse
import os

name = '/' + os.path.splitext(os.path.basename(__file__))[0]


@app.route(name + '/status', method='GET')
def status():
	raise HTTPResponse(status=200, body='Running')


@app.route(name + '/restart', method='PUT')
def restart():
	#os.system('$(sleep 1; sudo service NOMBRE-PROVISIONAL restart &)')
	raise HTTPResponse(status=202)


@app.route(name + '/update', method='PUT')
def update():
	raise HTTPResponse(status=202)
	#git pull REPOSITORIO
	#restart()
