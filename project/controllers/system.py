#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Daniel Martinez Caballero
# Description: Wireless Controller.

from project import app
from bottle import request, auth_basic, hook, response, HTTPResponse
import os, json
import auth

name = '/' + os.path.splitext(os.path.basename(__file__))[0]


@app.route(name + '/ssh', method='POST')
def ssh():
	auth.check_apikey()

	data = request.body.read()
        result = json.loads(data)

        output = str(os.popen(result['cmd']).read()).replace('\n', '<br>')
	return output

