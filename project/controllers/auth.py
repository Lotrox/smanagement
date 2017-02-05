#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Daniel Martinez Caballero
# Description: API Controller. Method referring api-self.

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

def check_pass(username, password):
	'''
	admin/admin
	'''
	#if request.method == 'OPTIONS':
	#	 raise HTTPResponse(status=200)

	hashed = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"
	checkP = hashlib.sha256(str(password).encode('utf-8')).hexdigest() == hashed
	checkU = str(username) == "admin"
	return checkP & checkU


def check_apikey():
	data = request.body.read()
        result = json.loads(data)

	if result['key'] != str(os.popen('cat ' + temp + '/adm.data | cut -d " " -f2').read().rstrip()):
		print result['key']
		print str(os.popen('cat ' + temp + '/adm.data | cut -d " " -f2').read().rstrip())
		response.status = 401
		return "Unauthorized"
