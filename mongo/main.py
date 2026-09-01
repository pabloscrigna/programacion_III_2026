import os

from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

DB_NAME = "kansai"
DB_COLLECTION = "accesorios"


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

    # Conectarme a una base -- kansai
    db = client[DB_NAME]

    # Listar las colecciones --
    colecciones = db.list_collection_names()
    print("DB: ", DB_NAME)
    print("Colecciones")
    for indice, coleccion in enumerate(colecciones):
        print(f"{indice}. {coleccion}")

    # coleccion accesorios
    db = db[DB_COLLECTION]

    # busca todos los accesorios
    cursor = db.find()

    for accesorio in cursor:
        print(accesorio)

    total_accesorios = db.count_documents({})
    print("total: ", total_accesorios)

    # partNumber = PC1620K00H
    accesorio = db.find_one({"partNumber": "PC1620K00H"})
    print(accesorio)

    # partNumber = PC1870K00Z
    accesorio["partNumber"] = "PC1870K00Z"
    del accesorio["_id"]

    # insert de un documento
    # doc_insert = db.insert_one(accesorio)

    # print("doc_insert: ", doc_insert)

    # update
    new_price = accesorio["price"]
    response = db.update_one(
        {"partNumber": "PC1620K00H"}, {"$set": {"price": new_price}}
    )
    print("update: ", response)

    accesorios = [
        {"partNumber": "A", "accesorio": "dummy"},
        {"partNumber": "B", "accesorio": "dummy"},
    ]

    doc_insert = db.insert_many(accesorios)
    print("doc insert: ", doc_insert)

    response = db.update_many({"partNumber": "A"}, {"$set": {"price": new_price}})
    print("update: ", response)

    doc_deleted = db.delete_one({"partNumber": "A"})
    print("doc deleted: ", doc_deleted)

    doc_deleted = db.delete_many({"partNumber": "B"})
    print("doc deleted: ", doc_deleted)


if __name__ == "__main__":
    main()
