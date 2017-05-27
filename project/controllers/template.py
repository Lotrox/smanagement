#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: **Daniel Martinez Caballero**
# Description: **Plantilla de controlador**

from project import app
from bottle import request, HTTPResponse, HTTPError, auth_basic, response
import os, json
import auth

name = '/' + os.path.splitext(os.path.basename(__file__))[0]


@app.route(name, method='GET')
def root():
	# Este método se llamará con https://ip:puerto/template
        return "I am a here!"


@app.route(name + '/new', method='POST')
def new():
	# Este método se llamará con https://ip:puerto/template/new
	return "I am a POST method!"
