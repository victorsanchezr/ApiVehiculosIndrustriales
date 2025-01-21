from __future__ import print_function
from bd import obtener_conexion
import sys

def insertar_vehiculo(nombre, descripcion, precio,foto):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO vehiculos(nombre, descripcion, precio,foto) VALUES (%s, %s, %s,%s)",
                       (nombre, descripcion, precio,foto))
            if cursor.rowcount == 1:
                ret={"status": "OK" }
            else:
                ret = {"status": "Failure" }
        code=200
        conexion.commit()
        conexion.close()
    except:
        print("Excepcion al insertar un vehículo", file=sys.stdout)
        ret = {"status": "Failure" }
        code=500
    return ret,code

def convertir_vehiculo_a_json(vehiculo):
    d = {}
    d['id'] = vehiculo[0]
    d['nombre'] = vehiculo[1]
    d['descripcion'] = vehiculo[2]
    d['precio'] = vehiculo[3]
    d['foto'] = vehiculo[4]
    return d

def obtener_vehiculos():
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre, descripcion, precio,foto FROM vehiculos")
            vehiculos = cursor.fetchall()
            vehiculosjson=[]
            if vehiculos:
                for vehiculo in vehiculos:
                    vehiculosjson.append(convertir_vehiculo_a_json(vehiculo))
        conexion.close()
        code=200
    except:
        print("Excepcion al obtener los vehiculos", file=sys.stdout)
        vehiculosjson=[]
        code=500
    return vehiculosjson,code

def obtener_vehiculo_por_id(id):
    vehiculojson = {}
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            #cursor.execute("SELECT id, nombre, descripcion, precio,foto FROM vehiculos WHERE id = %s", (id,))
            cursor.execute("SELECT id, nombre, descripcion, precio,foto FROM vehiculos WHERE id =" + id)
            vehiculo = cursor.fetchone()
            if vehiculo is not None:
                vehiculojson = convertir_vehiculo_a_json(vehiculo)
        conexion.close()
        code=200
    except:
        print("Excepcion al recuperar un vehículo", file=sys.stdout)
        code=500
    return vehiculojson,code


def eliminar_vehiculo(id):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM vehiculos WHERE id = %s", (id,))
            if cursor.rowcount == 1:
                ret={"status": "OK" }
            else:
                ret={"status": "Failure" }
        conexion.commit()
        conexion.close()
        code=200
    except:
        print("Excepcion al eliminar un vehiculo", file=sys.stdout)
        ret = {"status": "Failure" }
        code=500
    return ret,code

def actualizar_vehiculo(id, nombre, descripcion, precio, foto):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE vehiculos SET nombre = %s, descripcion = %s, precio = %s, foto=%s WHERE id = %s",
                       (nombre, descripcion, precio, foto,id))
            if cursor.rowcount == 1:
                ret={"status": "OK" }
            else:
                ret={"status": "Failure" }
        conexion.commit()
        conexion.close()
        code=200
    except:
        print("Excepcion al eliminar un vehiculo", file=sys.stdout)
        ret = {"status": "Failure" }
        code=500
    return ret,code
