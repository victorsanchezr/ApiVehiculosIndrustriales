from flask import request, session
import json
import decimal
from __main__ import app
import web.controlador_vehiculos as controlador_vehiculos

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal): return float(obj)

@app.route("/vehiculos",methods=["GET"])
def vehiculos():
    vehiculos,code= controlador_vehiculos.obtener_vehiculos()
    return json.dumps(vehiculos, cls = Encoder),code

@app.route("/vehiculo/<id>",methods=["GET"])
def vehiculo_por_id(id):
    vehiculo,code = controlador_vehiculos.obtener_vehiculo_por_id(id)
    return json.dumps(vehiculo, cls = Encoder),code

@app.route("/vehiculos",methods=["POST"])
def guardar_vehiculo():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        vehiculo_json = request.json
        ret,code=controlador_vehiculos.insertar_vehiculo(vehiculo_json["nombre"], vehiculo_json["descripcion"], float(vehiculo_json["precio"]), vehiculo_json["foto"])
    else:
        ret={"status":"Bad request"}
        code=401
    return json.dumps(ret), code

@app.route("/vehiculos/<id>", methods=["DELETE"])
def eliminar_vehiculo(id):
    ret,code=controlador_vehiculos.eliminar_vehiculo(id)
    return json.dumps(ret), code

@app.route("/vehiculos", methods=["PUT"])
def actualizar_vehiculo():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        vehiculo_json = request.json
        ret,code=controlador_vehiculos.actualizar_vehiculo(vehiculo_json["id"],vehiculo_json["nombre"], vehiculo_json["descripcion"], float(vehiculo_json["precio"]),vehiculo_json["foto"])
    else:
        ret={"status":"Bad request"}
        code=401
    return json.dumps(ret), code