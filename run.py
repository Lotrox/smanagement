#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Daniel Martinez Caballero
# Description: API REST Framework Bottle.

from bottle import Bottle, route, run, request, HTTPResponse, response
from gevent import monkey; monkey.patch_all()


run(host='0.0.0.0', port=8081, reloader=False, server='gevent')

