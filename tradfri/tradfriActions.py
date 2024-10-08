#!/usr/bin/env python3

# file        : tradfri/tradfriActions.py
# purpose     : module for controling status of the Ikea tradfri smart lights
#
# author      : harald van der laan
# date        : 2017/11/01
# version     : v1.2.0
#
# changelog   :
# - v1.2.0      update for gateway 1.1.15 issues                        (harald)
# - v1.1.0      refactor for cleaner code                               (harald)
# - v1.0.0      initial concept                                         (harald)

"""
    tradfri/tradfriActions.py - controlling the Ikea tradfri smart lights

    This module requires libcoap with dTLS compiled, at this moment there is no python coap module
    that supports coap with dTLS. see ../bin/README how to compile libcoap with dTLS support
"""

import sys
import json
import random
import subprocess
from .tradfriStatus import tradfri_get_device

coap = 'coap-client'

def call_coap(hubip, apiuser, apikey, method, path, payload):
    tradfriHub = 'coaps://{}:5684{}'.format(hubip, path)
    command = '{} -m {} -u "{}" -k "{}" -e \'{}\' "{}"'.format(coap, method, apiuser, apikey, payload, tradfriHub)
    return subprocess.check_output(command, shell=True)


def tradfri_power_light(hubip, apiuser, apikey, lightbulbid, value):
    """ function for power on/off tradfri lightbulb """
    path = '/15001/{}'.format(lightbulbid)

    if value == 'on':
        payload = json.dumps({ "3311": [{ "5850": 1 }] })
    else:
        payload = json.dumps({ "3311": [{ "5850": 0 }] })

    return call_coap(hubip, apiuser, apikey, 'put', path, payload)

def tradfri_dim_light(hubip, apiuser, apikey, lightbulbid, value):
    """ function for dimming tradfri lightbulb """
    dim = float(value) * 2.55
    path = '/15001/{}'.format(lightbulbid)
    payload = json.dumps({ "3311" : [{ "5851" : int(dim) }] })

    return call_coap(hubip, apiuser, apikey, 'put', path, payload)

def tradfri_color_light(hubip, apiuser, apikey, lightbulbid, value):
    """ function for color temperature tradfri lightbulb """
    path = '/15001/{}'.format(lightbulbid)
    payload = None
    colors = get_color_dict()
    
    if value in ['warm', 'normal', 'cold']:
        payload = json.dumps({ "3311" : [{ "5706" : colors[value]}] })
    
    if payload is None:
        color_supported = 'CWS' in tradfri_get_device(hubip, apiuser, apikey, lightbulbid)[u'3'][u'1']

        if not color_supported:
            print("Your lamp does not support colors.")
            sys.exit(1)

    payload = json.dumps({ "3311" : [{ "5706" : colors[value]}] })

    return call_coap(hubip, apiuser, apikey, 'put', path, payload)

def tradfri_power_group(hubip, apiuser, apikey, groupid, value):
    """ function for power on/off tradfri lightbulb """
    path = '/15004/{}'.format(groupid)

    if value == 'on':
        payload = json.dumps({ "5850" : 1 })
    else:
        payload = json.dumps({ "5850" : 0 })

    return call_coap(hubip, apiuser, apikey, 'put', path, payload)

def tradfri_dim_group(hubip, apiuser, apikey, groupid, value):
    """ function for dimming tradfri lightbulb """
    path = '/15004/{}'.format(groupid)
    dim = float(value) * 2.55
    payload = json.dumps({ "5851" : int(dim) })

    return call_coap(hubip, apiuser, apikey, 'put', path, payload)

def tradfri_authenticate(hubip, securitycode, apiuser = "TRADFRI_PY_API_{}".format(random.randint(0, 1000)) ):
    """ function for authenticating tradfri and getting apikey """
    path = '/15011/9063'
    payload = json.dumps({"9090": apiuser})

    result = call_coap(hubip, 'Client_identity', securitycode, 'post', path, payload)

    try:
        apikey = json.loads(result.decode().strip('\n').split('\n')[-1])["9091"]
    except ValueError:
        raise Exception("Didn't receive valid apikey. This is because the api isn't reachable or the api user already exists.")

    return apiuser,apikey
    
def get_color_dict():
    return {
    'blue' : '4a418a',
    'light blue' : '6c83ba',
    'saturated purple' : '8f2686',
    'lime' : 'a9d62b',
    'light purple': 'c984bb',
    'yellow' : 'd6e44b',
    'saturated pink' : 'd9337c',
    'dark peach' : 'da5d41',
    'saturated red' : 'dc4b31',
    'cold sky' : 'dcf0f8', 
    'pink' : 'e491af',
    'peach' : 'e57345',
    'warm amber' : 'e78834',
    'light pink' : 'e8bedd',
    'cool daylight' : 'eaf6fb',
    'candlelight' : 'ebb63e',
    'warm' : 'efd275',
    'normal' : 'f1e0b5',
    'sunrise' : 'f2eccf',
    'cold' : 'f5faf6',
    }
