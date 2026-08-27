import os

from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

DB_NAME = "iades-2026"
DB_COLLECTION = "sociedades"


def db_connect(mongo_uri):

    try:
        client = MongoClient(mongo_uri)

        _ = client.server_info()

    except Exception as e:
        raise Exception("Unable to find the document due to the following error: ", e)

    return client


def list_db(client):

    db_list = client.list_database_names()

    return db_list


def main():
    # Conexión
    mongo_uri = os.getenv("MONGO_URI")
    client = db_connect(mongo_uri)

    # Liste las DBs
    lista_db = list_db(client)
    print("DB")

    for indice, db in enumerate(lista_db):
        print(f"{indice}. {db}")

    # Conectarme a una base
    db = client[DB_NAME]

    # Listar las colecciones
    colecciones = db.list_collection_names()
    print("DB: ", DB_NAME)
    print("Colecciones")
    for indice, coleccion in enumerate(colecciones):
        print(f"{indice}. {coleccion}")

    db_index = int(input("ingrese la DB a consultar: "))
    print("El usuario quiere consultar la DB: ", lista_db[db_index])
    db = client[lista_db[db_index]]

    colecciones = db.list_collection_names()
    print("Colecciones")
    for indice, coleccion in enumerate(colecciones):
        print(f"{indice}. {coleccion}")


if __name__ == "__main__":
    main()
