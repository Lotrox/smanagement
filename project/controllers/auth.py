#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Daniel Martinez Caballero
# Description: Controlador de control de accesos y autentificación de la API.

from project import app
from bottle import request, HTTPResponse, abort, HTTPError, response
import os, json
import hashlib
import logging

temp = '/opt/smanagement/api-rest/temp'

# Soporte para llamadas CORS con peticion OPTIONS.
@app.route('/', method = 'OPTIONS')
@app.route('/<path:path>', method = 'OPTIONS')
def options_handler(path = None):
	return {}

def check_apikey():
	data = request.body.read()
        result = json.loads(data)

	if result['key'] != str(os.popen('cat ' + temp + '/adm.data | cut -d " " -f2').read().rstrip()):
		print result['key']
		print str(os.popen('cat ' + temp + '/adm.data | cut -d " " -f2').read().rstrip())
		response.status = 401
		return "Unauthorized"
