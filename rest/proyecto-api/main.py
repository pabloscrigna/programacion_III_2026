import asyncio
import json

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException

from pydantic import BaseModel
from pymongo import AsyncMongoClient

class AccesorioCreate(BaseModel):
    partNumber: str
    name: str
    description: str
    currency: str
    price: float


@asynccontextmanager
async def lifespam(app: FastAPI):
    print("Iniciando servidor.....")
    client_mongo = AsyncMongoClient("mongodb+srv://pscrigna:xD9MfSmciUV7b2nf@cluster0.xlccdc8.mongodb.net/")
    app.db = client_mongo["kansai"]


    yield

    print("Apagando servidor....")
    client_mongo.close()

app = FastAPI(lifespan=lifespam)

# Accesorios
# listar accesorios --


@app.get("/accesorios/")
async def listar_accesorios(limit: int = 10, skip: int = 0):

    accesorios = await app.db["accesorios"].find().skip(skip).limit(limit).to_list()

    json_accesorio = []
    for accesorio in accesorios:
        accesorio["_id"] = str(accesorio["_id"])
        accesorio.pop("applicationId")
        accesorio.pop("collectionId")
        json_accesorio.append(accesorio)

    return {
        "accesorios": json_accesorio,
        "total": len(accesorios)
    }


@app.get("/accesorios/{part_number}/")
async def read_item(part_number: str):

    accesorio = await app.db["accesorios"].find_one({"partNumber": part_number})

    if accesorio is None:
        raise HTTPException(
            status_code=404,
            detail=f"Accesorio on partNumber {part_number} no encontrado"
        )

    accesorio["_id"] = str(accesorio["_id"])
    accesorio.pop("applicationId")
    accesorio.pop("collectionId")

    return {"accesorio": accesorio}


@app.post("/accesorios/")
async def crear_accesorio(accesorio: AccesorioCreate):

    app.db.append(accesorio.model_dump())

    return {"accesorio": accesorio}


@app.delete("/accesorios/{part_number}/")
async def delete_item(part_number: str):

    print("part Numeber: ", part_number)
    response = await app.db["accesorios"].delete_one({"partNumber": part_number})
    print(response)

    return { "status": "under construction"}


# health-check
@app.get("/")
def read_root():
    return {"ping": "pong"}
