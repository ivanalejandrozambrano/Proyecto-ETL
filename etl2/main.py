import requests
import json
from datetime import datetime


def update_data(document_id, updated_data):
    url3 = f"http://localhost:5000/api/data/{document_id}"
    headers = {'Content-Type': 'application/json'}
    data1 = json.dumps(updated_data)
    print(data1)
    print(type(data1))
    response = requests.put(url3, data1, headers=headers)
    return response.text


# URL de la API que deseas llamar
url = "http://127.0.0.1:5000/api/data"

# Realiza la solicitud GET a la API
response = requests.get(url)

# Verifica el código de estado de la respuesta
if response.status_code == 200:
    # La solicitud fue exitosa
    data = response.json()  # Obtiene los datos de la respuesta en formato JSON

    for datau in data:
        # Extracción de características de fecha
        datau['YearStart'] = datetime.strptime(str(datau['YearStart']), '%Y')

        datau['YearEnd'] = datetime.strptime(str(datau['YearEnd']), '%Y')

        datau['Duration'] = (datau['YearEnd'] - datau['YearStart']).days

        # Procesamiento de ubicación
        geo_location = datau['GeoLocation']
        latitude, longitude = map(
            float, geo_location.strip('POINT ()').split())

        datau['Latitude'] = latitude
        datau['Longitude'] = longitude

        datau['seguir'] = datau["_id"]["$oid"]

        # Puedes eliminar las claves originales que ya no necesitas
        datau.pop('YearStart')
        datau.pop('YearEnd')
        datau.pop('GeoLocation')

        # Reemplaza "your_document_id" con el ID real del documento
        document_id = datau['seguir']
        updated_data = {
            "actualizado_en": 2
        }

        response = update_data(document_id, updated_data)
        print(response)

        datau.pop("_id", None)

    keys = datau.keys()
    print(datau['seguir'])
    """ print(type(data))
    print(type(response))
    print(keys)
    print(data) """
    jdata = json.dumps(data)
    """ json_data = json.loads(jdata)
    print(type(jdata)) """
    print(keys)
    print(jdata)

else:
    # La solicitud no fue exitosa
    print("Error en la solicitud:", response.status_code)

respuesta = input('¿Desea ejecutar la carga de datos? (y/n): ')
if respuesta.lower() == 'y':
    url2 = "http://localhost:5000/api/load"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url2, jdata, headers=headers)

    if response.status_code == 201:
        print('Datos cargados exitosamente.')
        # print(response.json())
    else:
        # La solicitud no fue exitosa
        print("Algo salio mal:", response.status_code)
else:
    print('No se ejecutará la carga de datos.')
