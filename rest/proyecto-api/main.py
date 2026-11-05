import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from pymongo import AsyncMongoClient, ReturnDocument

# nivel configurable desde el .env (DEBUG, INFO, WARNING, ERROR); por defecto INFO
logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
)
logger = logging.getLogger("proyecto-api")


class AccesorioCreate(BaseModel):
    partNumber: str
    name: str
    description: str
    currency: str
    price: float


class Accesorio(AccesorioCreate):
    id: str


class AccesorioResponse(BaseModel):
    accesorio: Accesorio


class AccesoriosResponse(BaseModel):
    accesorios: list[Accesorio]
    total: int


def serializar_accesorio(documento: dict) -> Accesorio:
    # convierte el ObjectId de mongo a str; los campos que no estan
    # en el modelo (applicationId, collectionId) se descartan solos
    return Accesorio.model_validate({**documento, "id": str(documento["_id"])})


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Iniciando servidor")
    client_mongo = AsyncMongoClient(os.environ["MONGO_URI"])
    app.state.db = client_mongo["kansai"]
    logger.info("Base de datos: %s", app.state.db.name)

    yield

    logger.info("Apagando servidor")
    await client_mongo.close()

app = FastAPI(lifespan=lifespan)

# Accesorios
# listar accesorios --


@app.get("/accesorios/", response_model=AccesoriosResponse)
async def listar_accesorios(limit: int = 10, skip: int = 0):

    accesorios = await app.state.db["accesorios"].find().skip(skip).limit(limit).to_list()
    # total de documentos en la coleccion, no solo los de esta pagina
    total = await app.state.db["accesorios"].count_documents({})
    logger.debug("Listado: skip=%d limit=%d devueltos=%d total=%d", skip, limit, len(accesorios), total)

    return AccesoriosResponse(
        accesorios=[serializar_accesorio(accesorio) for accesorio in accesorios],
        total=total
    )


@app.get("/accesorios/{part_number}/", response_model=AccesorioResponse)
async def read_item(part_number: str):

    accesorio = await app.state.db["accesorios"].find_one({"partNumber": part_number})

    if accesorio is None:
        raise HTTPException(
            status_code=404,
            detail=f"Accesorio con partNumber {part_number} no encontrado"
        )

    return AccesorioResponse(accesorio=serializar_accesorio(accesorio))


@app.post("/accesorios/", response_model=AccesorioResponse, status_code=201)
async def crear_accesorio(accesorio: AccesorioCreate, x_api_key: str = Header()):

    # FastAPI lee el header X-API-Key a partir del nombre del parametro
    if x_api_key != os.environ["API_KEY"]:
        # no se loguea la clave recibida, para no dejar secretos en los logs
        logger.warning("POST rechazado: API key invalida")
        raise HTTPException(status_code=401, detail="API key invalida")

    existente = await app.state.db["accesorios"].find_one({"partNumber": accesorio.partNumber})
    if existente is not None:
        logger.warning("POST rechazado: partNumber %s ya existe", accesorio.partNumber)
        raise HTTPException(
            status_code=409,
            detail=f"Ya existe un accesorio con partNumber {accesorio.partNumber}"
        )

    documento = accesorio.model_dump()
    # insert_one agrega el _id generado por mongo al dict
    await app.state.db["accesorios"].insert_one(documento)
    logger.info("Accesorio creado: %s (id %s)", accesorio.partNumber, documento["_id"])

    return AccesorioResponse(accesorio=serializar_accesorio(documento))


@app.put("/accesorios/{part_number}/", response_model=AccesorioResponse)
async def actualizar_accesorio(part_number: str, accesorio: AccesorioCreate):

    # si cambia el partNumber, no puede chocar con otro accesorio existente
    if accesorio.partNumber != part_number:
        existente = await app.state.db["accesorios"].find_one({"partNumber": accesorio.partNumber})
        if existente is not None:
            logger.warning("PUT rechazado: partNumber %s ya existe", accesorio.partNumber)
            raise HTTPException(
                status_code=409,
                detail=f"Ya existe un accesorio con partNumber {accesorio.partNumber}"
            )

    # $set pisa solo los campos del modelo; applicationId y collectionId se conservan
    actualizado = await app.state.db["accesorios"].find_one_and_update(
        {"partNumber": part_number},
        {"$set": accesorio.model_dump()},
        return_document=ReturnDocument.AFTER
    )

    if actualizado is None:
        raise HTTPException(
            status_code=404,
            detail=f"Accesorio con partNumber {part_number} no encontrado"
        )

    logger.info("Accesorio actualizado: %s", part_number)
    return AccesorioResponse(accesorio=serializar_accesorio(actualizado))


@app.delete("/accesorios/{part_number}/", response_model=AccesorioResponse)
async def delete_item(part_number: str):

    # borra y devuelve el documento borrado, o None si no existia
    accesorio = await app.state.db["accesorios"].find_one_and_delete({"partNumber": part_number})

    if accesorio is None:
        raise HTTPException(
            status_code=404,
            detail=f"Accesorio con partNumber {part_number} no encontrado"
        )

    logger.info("Accesorio borrado: %s", part_number)
    return AccesorioResponse(accesorio=serializar_accesorio(accesorio))


# health-check
@app.get("/")
def read_root():
    return {"ping": "pong"}
