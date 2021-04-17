#!/usr/bin/env python3

# file        : tradfri-status.py
# purpose     : getting status from the Ikea tradfri smart lights
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
    tradfri-status.py - getting status of the Ikea Tradfri smart lights

    This module requires libcoap with dTLS compiled, at this moment there is no python coap module
    that supports coap with dTLS. see ../bin/README how to compile libcoap with dTLS support
"""

import os
import sys
import time
import configparser

from tradfri import tradfriStatus

def main():
    """ main function """
    conf = configparser.ConfigParser()
    script_dir = os.path.dirname(os.path.realpath(__file__))
    conf.read(script_dir + '/tradfri.cfg')

    hubip = conf.get('tradfri', 'hubip')
    apiuser = conf.get('tradfri', 'apiuser')
    apikey = conf.get('tradfri', 'apikey')

    print('devices:')
    for deviceid in tradfriStatus.tradfri_get_devices(hubip, apiuser, apikey):
        time.sleep(0.5)
        device = tradfriStatus.tradfri_get_lightbulb(hubip, apiuser, apikey, deviceid)
        id = device["9003"]
        name = device["9001"]

        if "3311" in device:
            bulb = device["3311"][0]
            brightness = bulb["5851"]
            state = bulb["5850"]
            state = {0: 'off', 1: 'on'}[state]
            if "5711" in bulb:
                warmth = float(bulb["5711"])
                warmth = round((warmth-250)/(454-250)*100,1)# reported as a percentage (100% maximum warmth)
            else:
                warmth = "N/A"
            print('ID: {0:<5}, name: {1: <35}, brightness: {2: <3}, warmth: {3: >5}%, state: {4}'.format(id, name, brightness, warmth, state))
        else:
            print('ID: {0:<5}, name: {1: <35}'.format(id, name))
    print('\n')

    print('groups:')
    for groupid in tradfriStatus.tradfri_get_groups(hubip, apiuser, apikey):
        time.sleep(0.5)
        group = tradfriStatus.tradfri_get_group(hubip, apiuser, apikey, groupid)
        id = group["9003"]
        name = group["9001"]
        state = group["5850"]
        state = {0: 'off', 1: 'on'}[state]
        print('ID: {0:<5}, name: {1: <16}, state: {2}'.format(id, name, state))
    print('\n')

if __name__ == "__main__":
    main()
    sys.exit(0)
