#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Daniel Martinez Caballero
# Description: Services Controller. 

from project import app
from bottle import request, HTTPResponse, auth_basic
import os, json
import auth

name = '/' + os.path.splitext(os.path.basename(__file__))[0]


@app.route(name + '/<service>/<command>', method='POST')
def service(service, command):
	auth.check_apikey()

	output = str(os.popen('sudo service ' + str(service) + ' ' + str(command)).read()).replace('\n', '<br />')
	return output


@app.route(name + '/<service>', method='POST')
def service(service):
	out = os.popen('sudo service ' + service + ' status').read()
	d = {}

	d['name']   = out.split('Loaded: ')[0].rstrip() # Nombre y descripcion del servicio.
	d['loaded'] = out.split('Loaded: ')[1].split('Active: ')[0].rstrip() # Carga del servicio.
	d['status'] = out.split('Loaded: ')[1].split('Active: ')[1].split('\n')[0] # Estado actual del servicio.

	return json.dumps(d, ensure_ascii=False)


@app.route(name + '/list', method='POST')
def list():
        auth.check_apikey()
	out = str(os.popen('sudo systemctl -r --type service --all').read()).strip().split('\n')

	c = 0
        newout = {}
        for i in range(1, len(out)-9):
                d = {}
		t = 0
		if out[i].split()[0] == "\xe2\x97\x8f":
			t = 1
                d["name"] = out[i].split()[0+t]
                d["status"] = out[i].split()[3+t]
               	newout[c] = d
                c += 1
        return json.dumps(newout, ensure_ascii=False)

