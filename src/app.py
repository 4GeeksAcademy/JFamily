"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)
# create the jackson family object
jackson_family = FamilyStructure("Jackson")

John = {
    "first_name": "John",
    "last_name": jackson_family.last_name,
    "age": 33,
    "lucky_numbers": [7, 13, 22]
}

Jane = {
    "first_name": "Jane",
    "last_name": jackson_family.last_name,
    "age": 35,
    "lucky_numbers": [10, 14, 3]
}

Jimmy = {
    "first_name": "Jimmy",
    "last_name": jackson_family.last_name,
    "age": 5,
    "lucky_numbers": [1]
}

jackson_family.add_member(John)
jackson_family.add_member(Jane)
jackson_family.add_member(Jimmy)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])    #Llama a todos los miembros
def get_all_members():
    return jsonify(jackson_family.get_all_members()), 200

@app.route('/member', methods=['POST'])
def create_member():
    member = request.json
    print("añadido", member)
    jackson_family.add_member(member)
    if member is not None:
        return "miembro creado", 200

@app.route('/member/<int:id>', methods=['GET'])  #Llamar a un miembro según ID
def get_single_member(id):
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    return jsonify({"error": "No se encuentra al miembro"}), 404

@app.route('/add-member', methods=['POST'])
def handle_add_member():
    data = request.get_json()

    # Se exigen los datos básicos
    if not data or "first_name" not in data or "age" not in data or "lucky_numbers" not in data:
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    data["last_name"] = jackson_family.last_name  # Agregar el apellido

    jackson_family.add_member(data)
    return jsonify("Miembro añadido"), 201

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_single_member(id):
    member = jackson_family.get_member(id)

    if member:
        jackson_family.delete_member(id)
        return jsonify({"done": True}), 200  # Devuelve el formato esperado
    return jsonify({"error": "No se ha encontrado al miembro"}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
