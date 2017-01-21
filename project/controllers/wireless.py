#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Daniel Martinez Caballero
# Description: Wireless Controller.

from project import app
from bottle import request, auth_basic, hook, response, HTTPResponse
import os, json
import auth

name = '/' + os.path.splitext(os.path.basename(__file__))[0]


@app.route(name + '/clients', method='POST')
def clients():
	"""
        Obtener la lista de dispositivos conectados al punto de acceso WiFi.
        Se realiza una intersección de MAC entre los servicios de dnsmasq y hostapd,
        de este modo conseguimos además la dirección IP asignada y el nombre del dispositivo.
        """
	auth.check_apikey()

        cmd = "echo \"$(journalctl -eu dnsmasq | grep \"$(sudo hostapd_cli all_sta | grep dot11RSNAStatsSTAAddress | cut -d \"=\" -f2 | cut -d \" \" -f1)\" | grep DHCPACK | cut -c61-)\" > /tmp/ap-clients"
        os.system(cmd)
        output = str(os.popen("awk '!a[$0]++' /tmp/ap-clients").read()).strip().split('\n')
	return json.dumps(output)
	raise HTTPResponse(status=200, body=json.dumps(output))

