## Ejecución 

1. Carpeta: icegauntlet_auth_server

./auth_server --Ice.Config=auth_server.conf

./add_user <user_name>

2. Directorio raiz

Obtener un nuevo token:

  ./get_new_token < user > < password > < proxy autenticacion >
  
Cambiar de contraseña:

  ./auth_client.py < proxy autenticacion >
  
    - Insertar:
  
      - user
  
      - password
  
      - new_password

Ejecutar el servidor de mapas:

./run_map_server.py < proxy servidor autenticacion >

Subir un mapa:

./upload_map.py < proxy servidor mapas > < token > < archivoMapa.json >

Eliminar un mapa:

./delete_map.py < proxy servidor mapas > < token > < nombre mapa >
