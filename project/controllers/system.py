#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Daniel Martinez Caballero
# Description: Wireless Controller.

from project import app
from bottle import request, hook, response, HTTPResponse
import os, json
import auth

name = '/' + os.path.splitext(os.path.basename(__file__))[0]


@app.route(name + '/ssh', method='POST')
def ssh():
	auth.check_apikey()

	data = request.body.read()
        result = json.loads(data)
        output = str(os.popen(result['cmd']).read()).replace('\n', '<br>')
	return output


@app.route(name + '/temperature', method='POST')
def temperature():
        auth.check_apikey()

	out = os.popen('sensors | grep \"temp1\" | cut -d \"+\" -f2').read()
	t1 = float(out.split('\n')[0].split('°C')[0])
	t2 = float(out.split('\n')[1].split('°C')[0])
        return str(float( (t1 + t2) / 2 ))


@app.route(name + '/status', method='POST')
def status():
        auth.check_apikey()

	out = {}
	out["host"]   = os.popen('hostnamectl | grep \"Static hostname\"').read().rstrip().split()[-1]
	out["so"]     = os.popen('hostnamectl | grep \"Operating System\"').read().rstrip().split(':')[-1]
	out["kernel"] = os.popen('hostnamectl | grep \"Kernel\"').read().rstrip().split(':')[-1]
	out["arch"]   = os.popen('hostnamectl | grep \"Architecture\"').read().rstrip().split(':')[-1]
	out["ramGb"]  = round(float(os.popen('grep MemTotal /proc/meminfo').read().rstrip().split(':')[1].split()[0])/1024/1024*100)/100
	out["model"]  = os.popen('lscpu | grep \"Model name\"').read().rstrip().split(':')[1].strip()
	out["numCPU"] = os.popen('lscpu | grep \"CPU(s)\"').read().split('\n')[0].split(':')[1].strip()
	out["mhzCPU"] = os.popen('lscpu | grep \"CPU MHz\"').read().split()[-1]
	out["uptime"] = os.popen("awk '{print int($1/3600)\"h \"int(($1%3600)/60)\"m \"int($1%60)\"s\"}' /proc/uptime").read().rstrip()
	out["cuCPU"]  = round(float(os.popen('grep \'cpu \' /proc/stat | awk \'{usage=($2+$4)*100/($2+$4+$5)} END {print usage}\'').read().rstrip())*100)/100
	return json.dumps(out, ensure_ascii=False)
