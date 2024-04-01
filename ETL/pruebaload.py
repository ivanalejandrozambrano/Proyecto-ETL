import requests
import json
from flask import Flask, request
from pymongo import MongoClient


def load_data(respuesta, jdata):
    if respuesta.lower() == 'y':
        client2 = MongoClient("mongodb://localhost:27018")
        db2 = client2.destino
        destination_collection = db2.test
        data_to_load = jdata.get_json(force=True)

        # Realiza las operaciones de carga en la base de datos de destino
        for item in data_to_load:
            destination_collection.insert_one(item)

        return item, 201

    else:
        print('No se ejecutará la carga de datos.')


# Ejemplo de uso:
respuesta = input("¿Desea cargar los datos? (y/n): ")
jdata = [
    {'DataSource': 'SEDD; SID', 'DataValue': 916, 'DataValueAlt': 916, 'DataValueType': 'Number', 'DataValueTypeID': 'NMBR', 'Duration': 0, 'Latitude': -92.27449074299966, 'LocationAbbr': 'AR', 'LocationDesc': 'Arkansas', 'LocationID': 5, 'Longitude': 34.74865012400045,
        'Question': 'Hospitalizations for asthma', 'QuestionID': 'AST3_1', 'Stratification1': 'Male', 'StratificationCategory1': 'Gender', 'StratificationCategoryID1': 'GENDER', 'StratificationID1': 'GENM', 'Topic': 'Asthma', 'TopicID': 'AST', '_id': {'$oid': '64974fc459c8912bb9419701'}, 'actualizado_en': 1},
    {'DataSource': 'SEDD; SID', 'DataValue': 2227, 'DataValueAlt': 2227, 'DataValueType': 'Number', 'DataValueTypeID': 'NMBR', 'Duration': 0, 'Latitude': -106.13361092099967, 'LocationAbbr': 'CO', 'LocationDesc': 'Colorado', 'LocationID': 8, 'Longitude': 38.843840757000464,
        'Question': 'Hospitalizations for asthma', 'QuestionID': 'AST3_1', 'Stratification1': 'Overall', 'StratificationCategory1': 'Overall', 'StratificationCategoryID1': 'OVERALL', 'StratificationID1': 'OVR', 'Topic': 'Asthma', 'TopicID': 'AST', '_id': {'$oid': '64974fc459c8912bb9419702'}, 'actualizado_en': 1}
]

load_data(respuesta, jdata)
