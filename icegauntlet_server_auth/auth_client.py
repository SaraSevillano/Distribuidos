#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

'''
Add new user to authorization database
'''

import os
import sys
import json
import signal

import psutil

import sys
import Ice

Ice.loadSlice('icegauntlet.ice')

import IceGauntlet
import auth_server 


class auth_client(Ice.Application):
    try:
        auth = auth_server.AuthenticationI()
        auth.changePassword(sys.argv[1], sys.argv[2], sys.argv[3])
    except OSError:
        print('ERROR: JSON file with user data not found!')
    