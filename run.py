#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Daniel Martinez Caballero
# Description: API REST Framework Bottle.

from project import app
from bottle import run, request, debug, ServerAdapter
from gevent import monkey; monkey.patch_all()
import signal, sys, os


# Manejador necesario para realizar la parada del servicio mediante señal de apagado.
def signal_handler(signal, frame):
        print('Stopping Signal_Handler')
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


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

	port = int(os.environ.get("PORT", 8091))
	run(app, host='0.0.0.0', port=port, server=SecureGeventServer)


