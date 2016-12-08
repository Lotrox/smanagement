#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Daniel Martinez Caballero
# Description: API REST Framework Bottle.

from project import app
from bottle import run, request, debug
from gevent import monkey; monkey.patch_all()


if __name__ == '__main__':
	run(app, reloader=True, host='0.0.0.0', port=8081, server='gevent')



