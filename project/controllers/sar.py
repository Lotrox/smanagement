#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Daniel Martinez Caballero
# Description: Services Controller. 

from project import app
from bottle import request, HTTPResponse, auth_basic
import os
import auth

name = '/' + os.path.splitext(os.path.basename(__file__))[0]


@app.route(name + '/cpu', method='GET')
@auth_basic(auth.check_pass)
def cpu():
	out = str(os.popen('sar -u').read()).replace('\n', '<br />')
	raise HTTPResponse(status=200, body=out)


@app.route(name + '/mem', method='GET')
@auth_basic(auth.check_pass)
def mem():
        out = str(os.popen('sar -r').read()).replace('\n', '<br />')
        raise HTTPResponse(status=200, body=out)
