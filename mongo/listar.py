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
    mongo_uri = os.getenv("MONGO_URI")
    client = db_connect(mongo_uri)

    # Conectarme a una base -- kansai
    db = client[DB_NAME]

    # coleccion accesorios
    db = db[DB_COLLECTION]

    accesorios_list = db.find({}).sort("partNumber", 1).limit(2).skip(0)

    # for accesorio in accesorios_list:
    #     print(accesorio)

    print(accesorios_list)
    print(list(accesorios_list))
