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


if __name__ == "__main__":
    # lo leo de un archivo
    accesorio = {
        "partNumber": "ZC64102030",
        "name": "Bandeja Baúl",
        "description": "Bandeja Baúl",
        "notCompatibleWith": "",
        "requires": "",
        "currency": "ARS",
        "price": 820300,
    }

    mongo_uri = os.getenv("MONGO_URI")
    client = db_connect(mongo_uri)

    # Conectarme a una base -- kansai
    db = client[DB_NAME]

    # coleccion accesorios
    db = db[DB_COLLECTION]

    # acc = db.find_one({"partNumber": accesorio["partNumber"]})

    # lo crea
    # if not acc:
    #     acc_new = db.insert_one(accesorio)
    #     print(acc_new)
    # # actualizarlo
    # else:
    #     print("Objeto existente")
    #     acc = db.update_one(
    #         {"partNumber": accesorio["partNumber"]}, {"$set": accesorio}
    #     )
    #     print(acc)

    acc = db.update_one(
        {"partNumber": accesorio["partNumber"]}, {"$set": accesorio}, upsert=True
    )
