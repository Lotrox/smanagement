#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Daniel Martinez Caballero
# Description: API Controller. Method referring api-self.

from project import app
from bottle import request, HTTPResponse, HTTPError, auth_basic, response
import os, json
import auth

name = '/' + os.path.splitext(os.path.basename(__file__))[0]
temp = '/opt/smanagement/api-rest/temp'

@app.route(name, method='GET')
def check():
	# Método sin control de acceso con el propósito de permitir comprobar el funcionamiento del servicio
	# de esta API. En caso de aceptar la petición, devuelve un mensaje html de éxito.
        return "<a href=\"javascript:window.history.go(-1);\">Running! Click here to go back</a>"


@app.route(name + '/login', method='POST')
def login():
	# Autentifica al usuario comprobando la contraseña que se pasa mediante POST y en caso de realizarse
	# correctamente devuelve un token único el cual es necesario para la comunicación con el resto de
	# llamadas con protección.

	csrf = str(request.environ.get('beaker.session').get('csrf_token'))
	data = request.body.read()
        result = json.loads(data)

	password = os.popen('cat /opt/smanagement/api-rest/sm.conf').read().rstrip().split('\n')[0]
	key      = os.popen('echo "' + result['key'] + '" | md5sum').read().rstrip()

	if key == password:
	        os.system('echo $(date +%Y-%m-%d@%H:%m:%S) "' + request.environ.get('REMOTE_ADDR') + '" OK  >> ' + temp + '/access.log')
		os.system('echo "' + request.environ.get('REMOTE_ADDR') + ' ' + str(csrf) + '" > ' + temp + '/adm.data')
		return csrf
	else:
	        os.system('echo $(date +%Y-%m-%d@%H:%m:%S) "' + request.environ.get('REMOTE_ADDR') + '" DENY  >> ' + temp + '/access.log')
		response.status = 401
                return "Unauthorized"


@app.route(name + '/restart', method='PUT')
def restart():
	# Reinicia el propio servicio ‘smanagement’
	auth.check_apikey()
	os.system('$(sleep 1; sudo service smanagement restart &)')
	raise HTTPResponse(status=202)


@app.route(name + '/update', method='PUT')
def update():
	# Trata de realizar una actualización del servicio ‘smanagement’
	auth.check_apikey()
	raise HTTPResponse(status=202)
	#git pull REPOSITORIO
	restart()


@app.route(name + '/log', method='POST')
def log():
	# Llamada que permite conocer la lista de últimos intentos, fallidos o aceptados,
	# a la llamada principal /api/login.
        auth.check_apikey()

	a = os.popen('cat ' + temp + '/access.log | tail -10').read().rstrip().split('\n')
	newout = {}
	c = 0
	for i in a:
		out = {}
		out["time"] = i.split()[0]
		out["ip"] = i.split()[1]
		out["check"] = i.split()[2]
		newout[c] = out
		c += 1
        return json.dumps(newout, ensure_ascii=False)

