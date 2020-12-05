#!/usr/bin/env python3

'''
Script to run authentication user
'''

import os
import sys

try:
    import pexpect
except ImportError:
    print('Required library "pexpect" not exists. Install with pip and try again')
    sys.exit(1)

# Define command to request new token
_COMMAND_ = './cliente.py "%(proxy)s"'

# Get required arguments
try:
    proxy, token, archivoMapa = sys.argv[1:]
except ValueError:
    print('Command arguments: {} <proxy> <token> <archivoMapa>'.format(
        os.path.basename(sys.argv[0]))
    )
    sys.exit(1)


# Run command
proc = pexpect.spawn(_COMMAND_%{"proxy": proxy}, echo=False)

found = proc.expect(["map"])
if found == 0:
    proc.sendline(archivoMapa)
else:
    print('ERROR: mapa no encontrado')
    sys.exit(1)

found = proc.expect(["token"])
if found == 0:
    proc.sendline(token)
else:
    print('ERROR: token no encontrada')
    sys.exit(1)

proc.expect([pexpect.EOF])
# Show command output and exit
print(proc.before.decode().strip())
sys.exit(0)
