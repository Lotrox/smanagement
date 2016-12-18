#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Daniel Martinez Caballero
# Description: Services Controller. 

from project import app
from bottle import request, HTTPResponse, auth_basic
import os
import auth

name = '/' + os.path.splitext(os.path.basename(__file__))[0]


@app.route(name + '/<service>/<command>', method='GET')
@auth_basic(auth.check_pass)
def service(service, command):
	output = str(os.popen('sudo service ' + str(service) + ' ' + str(command)).read()).replace('\n', '<br />')
	raise HTTPResponse(status=200, body=output)
