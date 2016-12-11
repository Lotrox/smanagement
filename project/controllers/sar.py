#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Daniel Martinez Caballero
# Description: Services Controller. 

from project import app
from bottle import request, HTTPResponse
import os

name = '/' + os.path.splitext(os.path.basename(__file__))[0]


@app.route(name + '/cpu', method='GET')
def status():
	out = str(os.popen('sar -u').read()).replace('\n', '<br />')
	raise HTTPResponse(status=200, body=out)


@app.route(name + '/mem', method='GET')
def status():
        out = str(os.popen('sar -r').read()).replace('\n', '<br />')
        raise HTTPResponse(status=200, body=out)
