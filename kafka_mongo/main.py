from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from config import get_settings
from db import connect_mongo

from routers import items

@asynccontextmanager
async def lifespan(app: FastAPI):
    # lee variables de entorno
    settings = get_settings()
    # conectar con la DB
    await connect_mongo()

    try:
        yield
    finally:
        pass

    # conectar kafka


app = FastAPI(title="Aplicacion Fastapi - Mongo - Confluent kafka",
              lifespan=lifespan)

app.include_router(items.router)



@app.get("/health")
async def health(request: Request):
    status = {"mongo": False, "kafka": False}

    return JSONResponse(status_code=503, content=status)
