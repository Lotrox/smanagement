#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Daniel Martinez Caballero
# Description: SAR Controller.

from project import app
from bottle import request, HTTPResponse
import json
import os
import auth

name = '/' + os.path.splitext(os.path.basename(__file__))[0]


@app.route(name + '/cpu', method='POST')
def cpu():
	auth.check_apikey()
	out = str(os.popen('sar -u').read()).split('\n')
	c = 0
	newout = {}
	for i in range(len(out)-2):
		d = {}
		if len(out[i].split()) == 8:
			d["time"] = out[i].split()[0]
			d["user"] = out[i].split()[2].replace(',','.')
			d["nice"] = out[i].split()[3].replace(',','.')
			d["system"] = out[i].split()[4].replace(',','.')
			d["iowait"] = out[i].split()[5].replace(',','.')
			d["steal"] = out[i].split()[6].replace(',','.')
			d["idle"] = out[i].split()[7].replace(',','.')
			if (d["idle"] != "%idle") and (d["time"] != "Average:"):
				newout[c] = d
				c += 1
	return json.dumps(newout, ensure_ascii=False)


@app.route(name + '/mem', method='GET')
def mem():
        out = str(os.popen('sar -r').read()).replace('\n', '<br />')
        raise HTTPResponse(status=200, body=out)
