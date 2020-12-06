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
_COMMAND_ = './cliente.py "%(proxyMapas)s" "%(proxyAuth)s"'

# Get required arguments
try:
    proxyMapas, token, archivoMapa, proxyAuth = sys.argv[1:]
except ValueError:
    print('Command arguments: {} <proxy servidor mapas> <token> <archivoMapa> <proxy servidor autenticacion> '.format(
        os.path.basename(sys.argv[0]))
    )
    sys.exit(1)

# Compose command
final_command = _COMMAND_ % {
    'proxyMapas': proxyMapas,
    'proxyAuth': proxyAuth
}

# Run command
old_pwd=os.getcwd()
os.chdir("icegauntlet_map_server")
proc = pexpect.spawn(final_command, echo=False)
os.chdir(old_pwd)

found = proc.expect(["opcion"])
if found == 0:
    proc.sendline('1')
else:
    print('ERROR: opcion no encontrada')
    sys.exit(1)

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
