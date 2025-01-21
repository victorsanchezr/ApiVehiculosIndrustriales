from __future__ import print_function
from __main__ import app
from flask import request, session
from bd import obtener_conexion
import json
import bcrypt

@app.route("/login", methods=['POST'])
def login():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        juego_json = request.json
        username = juego_json['username']
        password = juego_json['password']
        
        try:
            # Conectar a la base de datos
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                # Buscar el hash de la contraseña en la base de datos
                cursor.execute("SELECT clave, perfil FROM usuarios WHERE usuario = %s", (username,))
                usuario = cursor.fetchone()
            
            conexion.close()

            if usuario is None:
                ret = {"status": "ERROR", "mensaje": "Usuario/clave erróneo"}
                code = 200
            else:
                stored_hash = usuario[0]  # El hash de la contraseña almacenado en la base de datos
                # Verificar si la contraseña ingresada coincide con el hash
                if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                    ret = {"status": "OK"}
                    session["usuario"] = username
                    session["perfil"] = usuario[1]
                    code = 200
                else:
                    ret = {"status": "ERROR", "mensaje": "Usuario/clave erróneo"}
                    code = 200
        except Exception as e:
            print(f"Excepción al validar al usuario: {e}")
            ret = {"status": "ERROR"}
            code = 500
    else:
        ret = {"status": "Bad request"}
        code = 401
    return json.dumps(ret), code

@app.route("/registro", methods=['POST'])
def registro():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        juego_json = request.json
        username = juego_json['username']
        password = juego_json['password']
        perfil = juego_json['profile']
        
        try:
            # Conectar a la base de datos
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                # Verificar si el usuario ya existe
                cursor.execute("SELECT perfil FROM usuarios WHERE usuario = %s", (username,))
                usuario = cursor.fetchone()
                
                if usuario is None:
                    # Crear el hash de la contraseña
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                    
                    # Insertar el nuevo usuario con la contraseña hasheada
                    cursor.execute("INSERT INTO usuarios(usuario, clave, perfil) VALUES(%s, %s, %s)",
                                   (username, hashed_password, perfil))
                    
                    if cursor.rowcount == 1:
                        conexion.commit()
                        ret = {"status": "OK"}
                        code = 200
                    else:
                        ret = {"status": "ERROR"}
                        code = 500
                else:
                    ret = {"status": "ERROR", "mensaje": "Usuario ya existe"}
                    code = 200
            conexion.close()
        except Exception as e:
            print(f"Excepción al registrar al usuario: {e}")
            ret = {"status": "ERROR"}
            code = 500
    else:
        ret = {"status": "Bad request"}
        code = 401
    return json.dumps(ret), code

@app.route("/logout", methods=['GET'])
def logout():
    session.clear()
    return json.dumps({"status": "OK"}), 200
