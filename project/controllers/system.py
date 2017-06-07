#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Daniel Martinez Caballero
# Description: Controlador del sistema. Utilidades del sistema.

from project import app
from bottle import request, hook, response, HTTPResponse
import os, json
import auth

name = '/' + os.path.splitext(os.path.basename(__file__))[0]


@app.route(name + '/ssh', method='POST')
def ssh():
	# Esta petición permite pasar como argumento POST una cadena el cual será interpretado por BASH
	# y la salida del comando es devuelto en el propio cuerpo de la respuesta.
	auth.check_apikey()

	data = request.body.read()
        result = json.loads(data)
        output = str(os.popen(result['cmd']).read()).replace('\n', '<br>')
	return output


@app.route(name + '/temperature', method='POST')
def temperature():
	# Usando el paquete lm-sensors, esta llamada devuelve una media de dos sensores del equipo.
        auth.check_apikey()

	out = os.popen('sensors | grep \"temp1\" | cut -d \"+\" -f2').read()
	t1 = float(out.split('\n')[0].split('°C')[0])
	t2 = float(out.split('\n')[1].split('°C')[0])
        return str(float( (t1 + t2) / 2 ))


@app.route(name + '/status', method='POST')
def status():
	# Llamada encargada de devolver un resumen de información del propio equipo.
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
	mem = os.popen('free -m | grep Mem').read().split()
	out["cuMEM"]  = round(float(mem[2])/float(mem[1])*10000)/100
	load = os.popen('cat /proc/loadavg').read()
        newout = {}
        newout[0] = load.split()[0]
        newout[1] = load.split()[1]
        newout[2] = load.split()[2]
	out["loadAVG"] = newout

	return json.dumps(out, ensure_ascii=False)


@app.route(name + '/disk', method='POST')
def diskSize():
	# Información acerca de la ocupación del disco principal del sistema operativo.
        auth.check_apikey()

	out = {}
	df = os.popen('df -k "/" | tail -n1 | xargs').read().split()
	out['folder'] = df[0] # Directorio principal usado por el sistema.
	out['blocks'] = df[1] # Número total de bloques de tamaño 1KB.
	out['used']   = df[2] # Bloques usados.
	out['avail']  = df[3] # Bloques disponibles.
	out['use']    = df[4] # % Usado.
	out['mount']  = df[5] # Directorio de montaje.
	return json.dumps(out, ensure_ascii=False)


@app.route(name + '/firewall', method='POST')
def firewall():
	# Usando la utilidad de iptables del equipo, devuelve la lista de reglas actualmente aplicadas en el sistema.
        auth.check_apikey()

        return os.popen('sudo iptables -L').read().replace('\n', '<br>')



