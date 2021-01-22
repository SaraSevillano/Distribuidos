#!/usr/bin/env python3

'''
Script to run map server
'''

import os
import sys

# Define command to request new token
_COMMAND_ = './map_server.py --Ice.Config=map_server.conf "%(proxyAuth)s"'

# Get required arguments
try:
    proxyAuth = sys.argv[1]
except:
    print('Command arguments: {} <proxy servidor autenticacion> '.format(
        os.path.basename(sys.argv[0]))
    )
    sys.exit(1)

# Compose command
final_command = _COMMAND_ % {
    'proxyAuth': proxyAuth
}

# Run command
old_pwd=os.getcwd()
os.chdir("icegauntlet_map_server")
os.system(final_command)
os.chdir(old_pwd)

sys.exit(0)

