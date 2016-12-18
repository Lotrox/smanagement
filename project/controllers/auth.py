#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Daniel Martinez Caballero
# Description: API Controller. Method referring api-self.

from project import app
from bottle import request, HTTPResponse
import os, json
import hashlib
import logging

def check_pass(username, password):
	'''
	admin/admin
	'''
	hashed = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918" 
	checkP = hashlib.sha256(str(password).encode('utf-8')).hexdigest() == hashed
	checkU = str(username) == "admin"
	return checkP & checkU


