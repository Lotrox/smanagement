#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Daniel Martinez Caballero
# Description: API REST Framework Bottle.

from project import app
from bottle import run, request, debug
from gevent import monkey; monkey.patch_all()
import signal, sys

# Manejador necesario para realizar la parada del servicio mediante señal de apagado.
def signal_handler(signal, frame):
        print('Stopping Signal_Handler')
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
	run(app, reloader=True, host='0.0.0.0', port=8081, server='gevent')



