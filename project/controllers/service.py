#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Daniel Martinez Caballero
# Description: Services Controller. 

from project import app
from bottle import request, HTTPResponse
import os

name = '/' + os.path.splitext(os.path.basename(__file__))[0]


@app.route(name + '/<service>/<command>', method='GET')
def status(service, command):
	os.system('sudo service ' + str(service) + ' ' + str(command))
	raise HTTPResponse(status=200, body='Running')
