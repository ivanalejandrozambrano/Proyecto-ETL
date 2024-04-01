import csv
import pymysql
from flask import Flask, request, jsonify
from pymongo import MongoClient
import os


mysql_conn = pymysql.connect(
    host="localhost",
    port=3306,
    database="cursoespe1",
    user="root",
    password=""
)


def insert_data_mysql(data):
    cursor = mysql_conn.cursor()

    # data es un solo diccionario, no necesitas iterar sobre él
    sql = "INSERT INTO test (YearStart, YearEnd, LocationDesc, Topic) VALUES (%s, %s, %s,%s)"
    values = (
        data['YearStart'],
        data['YearEnd'],
        data['LocationDesc'],
        data['Topic'],
    )
    try:
        cursor.execute(sql, values)
    except pymysql.err.InterfaceError as e:
        print("Error de interfaz en la consulta SQL:")
        print(e)

    mysql_conn.commit()
    cursor.close()

def insert_data_mysqlT(data):
    cursor = mysql_conn.cursor()

    for item in data:
        # Realizar las operaciones de inserción en MySQL
        sql = "INSERT INTO test (YearStart, YearEnd, LocationDesc, Topic) VALUES (%s, %s, %s,%s)"
        values = (
            item['YearStart'],
            item['YearEnd'],
            item['LocationDesc'],
            item['Topic'],
        )
        cursor.execute(sql, values)

    mysql_conn.commit()
    cursor.close()

def delete_data_mysql():
    cursor = mysql_conn.cursor()

    # Realizar la operación para eliminar todos los datos de la tabla
    sql = "DELETE FROM test"
    cursor.execute(sql)

    mysql_conn.commit()
    cursor.close()


def save_data_csv(data):
    csv_filename = "data.csv"

    # Verifica si el archivo ya existe
    file_exists = os.path.isfile(csv_filename)

    with open(csv_filename, mode='a' if file_exists else 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())

        if not file_exists:
            writer.writeheader()

        writer.writerows(data)


def transform_data(item):
    # transformed_item = {}  # Crea un nuevo diccionario para almacenar el resultado transformado

    # Realiza la transformación del item
    #
    # transformed_item['edad'] = 2023 - item['birth_year']  # Ejemplo: Calcula la edad a partir del año de nacimiento

    return item
