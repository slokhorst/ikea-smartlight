#!/usr/bin/env python3

# file        : tradfri/tradfriStatus.py
# purpose     : getting status from the Ikea tradfri smart lights
#
# author      : harald van der laan
# date        : 2017/11/01
# version     : v1.2.0
#
# changelog   :
# - v1.2.0      update for new gateway 1.1.15 issues                    (harald)
# - v1.1.0      refactor for cleaner code                               (harald)
# - v1.0.0      initial concept                                         (harald)

"""
    tradfriStatus.py - module for getting status of the Ikea tradfri smart lights

    This module requires libcoap with dTLS compiled, at this moment there is no python coap module
    that supports coap with dTLS. see ../bin/README how to compile libcoap with dTLS support
"""

import json
import subprocess

coap = 'coap-client'
timeout = 5

def call_coap(hubip, apiuser, apikey, method, path, timeout):
    tradfriHub = 'coaps://{}:5684{}'.format(hubip, path)
    command = '{} -m {} -u "{}" -k "{}" -B {} "{}"'.format(coap, method, apiuser, apikey, timeout, tradfriHub)
    result_json = subprocess.check_output(command, shell=True)
    return json.loads(result_json.decode().strip('\n').split('\n')[-1])


def tradfri_get_devices(hubip, apiuser, apikey):
    """ function for getting all tradfri device ids """
    path = '/15001'
    return call_coap(hubip, apiuser, apikey, 'get', path, timeout)

def tradfri_get_device(hubip, apiuser, apikey, deviceid):
    """ function for getting tradfri device information """
    path = '/15001/{}'.format(deviceid)
    return call_coap(hubip, apiuser, apikey, 'get', path, timeout)

def tradfri_get_groups(hubip, apiuser, apikey):
    """ function for getting tradfri group ids """
    path = '/15004'
    return call_coap(hubip, apiuser, apikey, 'get', path, timeout)

def tradfri_get_group(hubip, apiuser, apikey, groupid):
    """ function for getting tradfri group information """
    path = '/15004/{}'.format(groupid)
    return call_coap(hubip, apiuser, apikey, 'get', path, timeout)
