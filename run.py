#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Daniel Martinez Caballero
# Description: API REST Framework Bottle.

from project import app
from bottle import run, request, debug, ServerAdapter, Bottle, abort, hook, response
from gevent import monkey; monkey.patch_all()
import signal, sys, os
import logging
from beaker.middleware import SessionMiddleware
import bottle
from random import choice
from string import ascii_letters, digits

def signal_handler(signal, frame):
	# Manejador necesario para realizar la parada del servicio mediante señal de apagado.
        print('Stopping Signal_Handler')
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def str_random(length):
    '''Generate a random string using range [a-zA-Z0-9].'''
    chars = ascii_letters + digits
    return ''.join([choice(chars) for i in range(length)])


def gen_token():
    '''Put a generated token in session if none exist and return it.'''
    sess = request.environ
    if 'csrf_token' not in sess:
        sess['csrf_token'] = str_random(32)
    return sess['csrf_token']


def require_csrf(callback):
    def wrapper(*args, **kwargs):
        session = request.environ.get('beaker.session')
        if "/view/" in str(request['bottle.route']):
		csrf = request.headers.get('X-CSRF-Token')
		logging.critical("body: " + str(request.body.read()))
		logging.critical("CSRF: " + str(csrf) + " SESISION CSRF: " + str(session.get('csrf_token')))
        	if not csrf or csrf != session.get('csrf_token'):
        		abort(400)
	elif "/api/login" in str(request['bottle.route']):
	        session['csrf_token'] = gen_token()
       	body = callback(*args, **kwargs)
       	return body

    return wrapper


# Disparador encargado de habilitar el acceso a origenes distintos en todas las llamadas.
@app.hook('after_request')
def enable_cors():
        response.headers['Access-Control-Allow-Origin']  =  '*'
        response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token, Set-cookie, Content-Length'


if __name__ == '__main__':
	# Soporte de SSL junto con servidor Gevent. Ref: https://github.com/bottlepy/bottle/issues/436
	class SecureGeventServer(ServerAdapter):
		def run(self, handler):
       			from gevent import wsgi, pywsgi, local
		        import threading
		        _lcth = threading.local()
		        if not isinstance(_lcth, local.local):
				msg = "Bottle requires gevent.monkey.patch_all() (before import)"
		                raise RuntimeError(msg)
		        if not self.options.get('fast'): wsgi = pywsgi
		        log = None if self.quiet else 'default'
		        wsgi.WSGIServer((self.host, self.port), handler, log=log, keyfile='/opt/smanagement/api-rest/key.pem', certfile='/opt/smanagement/api-rest/cert.pem').serve_forever()

	session_opts = {
        	'session.type': 'file',
	        'session.cookie_expires': 300,
        	'session.data_dir': './data',
	        'session.auto': True
	}

	app.install(require_csrf)
	app = SessionMiddleware(app, session_opts)

	port = os.popen('cat /opt/smanagement/api-rest/sm.conf').read().rstrip().split('\n')[1]
	portEnv = int(os.environ.get("PORT", port))
	run(app, host='0.0.0.0', port=portEnv, server=SecureGeventServer)


