from flask import Flask, request, jsonify
from pymongo import MongoClient, errors
from bson import json_util
import requests
import json
from bson.objectid import ObjectId
from flask_cors import CORS
from time import sleep
import carga


app = Flask(__name__)
# Conexión a la base de datos MongoDB
connection_strings = [
    "mongodb://localhost:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.10.1",
    "mongodb://localhost:27020/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.10.1",
    "mongodb://localhost:27021/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.10.1",
]

client = None

for conn_str in connection_strings:
    try:
        temp_client = MongoClient(conn_str)
        if temp_client.is_primary:
            client = temp_client
            break
    except errors.ServerSelectionTimeoutError:
        pass
CORS(app)
# Ruta para obtener todos los documentos


@app.route('/api/data', methods=['GET'])
def get_all_data():
    db = client.test  # Nombre de la base de datos
    collection = db.test  # Nombre de la colección
    # Obtener los primeros 5 documentos
    data = list(collection.find())
    serialized_data = json_util.dumps(data)

    return serialized_data, 200
    # data = list(collection.find().limit(5))  # Obtener todos los documentos
    # return jsonify(data), 200

# Ruta para obtener un documento por su ID


@app.route('/api/data/<id>', methods=['GET'])
def get_data(id):
    db = client.test
    collection = db.test
    data = collection.find_one({'_id': ObjectId(id)})
    return jsonify({
      '_id': str(ObjectId(data['_id'])),
      'YearStart': data['YearStart'],
      'YearEnd': data['YearEnd'],
      'LocationDesc': data['LocationDesc'],
        'Topic': data['Topic']
  })

# Ruta para crear un nuevo documento


@app.route('/api/data', methods=['POST'])
def create_data():
    db = client.test
    collection = db.test
    new_data = request.json
    print(new_data)
    result = collection.insert_one(new_data)
    try:
        # Aquí puedes realizar cualquier procesamiento o limpieza necesaria
        # antes de insertar en MySQL
        carga.insert_data_mysql(new_data)
    except json.JSONDecodeError as e:
        print(f"Error de formato JSON en el documento: {new_data}")
   
    #carga.insert_data_mysql(cleaned_data)
    return str(result.inserted_id), 201

# Ruta para actualizar un documento existente


@app.route('/api/data/<id>', methods=['PUT'])
def update_data(id):
    db = client.test
    collection = db.test
    updated_data = request.json

    result = collection.update_one(
        {"_id": ObjectId(id)}, {'$set': updated_data})
    print(result)

    try:
        # Cargar todos los datos nuevamente
        all_data = list(collection.find())
        # Convertir los datos a formato JSON
        serialized_data = json_util.dumps(all_data)
        # Convertir los datos nuevamente a lista de diccionarios
        data = json_util.loads(serialized_data)
        # Borrar los datos existentes en la tabla de MySQL
        carga.delete_data_mysql()
        # Insertar los nuevos registros en la tabla de MySQL
        carga.insert_data_mysqlT(data)
    except json.JSONDecodeError as e:
        print(f"Error de formato JSON en los documentos: {all_data}")

    return jsonify({'message': 'User Updated'})

# Ruta para eliminar un documento por su ID


@app.route('/api/data/<id>', methods=['DELETE'])
def delete_data(id):
    db = client.test
    collection = db.test
    result = collection.delete_one({'_id': ObjectId(id)})
    try:
        # Cargar todos los datos nuevamente
        all_data = list(collection.find())
        # Convertir los datos a formato JSON
        serialized_data = json_util.dumps(all_data)
        # Convertir los datos nuevamente a lista de diccionarios
        data = json_util.loads(serialized_data)
        # Borrar los datos existentes en la tabla de MySQL
        carga.delete_data_mysql()
        # Insertar los nuevos registros en la tabla de MySQL
        carga.insert_data_mysqlT(data)
    except json.JSONDecodeError as e:
        print(f"Error de formato JSON en los documentos: {all_data}")
    return jsonify({'message': 'User Deleted'})


@app.route('/api/load', methods=['POST'])
def load_data():
    client2 = MongoClient("mongodb://172.21.0.3:27018")
    db2 = client2.destino
    destination_collection = db2.test

    # data_to_load = request.get_json(force=True)
    # Realiza las operaciones de carga en la base de datos de destino
    data_to_load = request.get_json(force=True)

    cleaned_data = []
    for item in data_to_load:
        try:
            item['_id'] = str(ObjectId())  # Convertir ObjectId a cadena
            cleaned_data.append(item)
        except json.JSONDecodeError as e:
            print(f"Error de formato JSON en el documento: {item}")
            continue

    print(data_to_load)

    # Realiza las operaciones de carga en la base de datos de destino
    for item in cleaned_data:
        destination_collection.insert_one(item)

    """ for item in data_to_load:
        transformed_item = carga.transform_data(item)
        transformed_data.append(transformed_item) """

    # Carga los datos en PostgreSQL
    carga.insert_data_mysql(cleaned_data)

    # Guarda los datos en un archivo CSV
    carga.save_data_csv(cleaned_data)

    # return 'Datos cargados en la base de datos de destino', 201
    return item, 201


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response


@app.route('/')
def hello():

    return 'El servidor está en funcionamiento'


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5000)
