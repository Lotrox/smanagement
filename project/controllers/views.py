#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Daniel Martinez Caballero
# Description: API Controller. Method referring api-self.

from project import app
from bottle import request, HTTPResponse, auth_basic
import os, json
import auth

name = '/' + os.path.splitext(os.path.basename(__file__))[0]

