#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Daniel Martinez Caballero
# Description: SAR Controller.

from project import app
from bottle import request, HTTPResponse
import json
from decimal import Decimal
import os
import auth

name = '/' + os.path.splitext(os.path.basename(__file__))[0]


@app.route(name + '/cpu', method='POST')
def cpu():
	auth.check_apikey()
	out = str(os.popen('sar -u').read()).split('\n')
	c = 0
	newout = {}
	for i in range(len(out)-32, len(out)-2):
		d = {}
		if len(out[i].split()) == 8:
			d["time"] = out[i].split()[0]
			d["user"] = out[i].split()[2]
			d["nice"] = out[i].split()[3]
			d["system"] = out[i].split()[4]
			d["iowait"] = out[i].split()[5]
			d["steal"] = out[i].split()[6]
			d["idle"] = out[i].split()[7]
			newout[c] = d
			c += 1
	return json.dumps(newout, ensure_ascii=False)


@app.route(name + '/mem', method='GET')
def mem():
        out = str(os.popen('sar -r').read()).replace('\n', '<br />')
        raise HTTPResponse(status=200, body=out)
