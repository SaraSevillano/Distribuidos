## How to run

./auth_server --Ice.Config=auth_server.conf

The _proxy_ will be shown in _stdout_. Also you can add users with:

./add_user <user_name>

The last command reload user database stored in *users.json*. Reloading the database is a _long time consuming task_ so this command should not be used in a production environment.

./cliente.py  < proxy >

ChangePassword: Opción 1
  - introducir:
    - user
    - password	
    - new password

GetNewToken: Opción 2
  - introducir:
    - user
    - password
