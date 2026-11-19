import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.items.router import router as items_router

logger = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---------- STARTUP ----------
    # Se ejecuta una sola vez, antes de que la app empiece a recibir requests.
    # Acá va la inicialización de recursos compartidos, por ejemplo:
    #   app.state.db = await crear_pool_db(settings.database_url)
    #   app.state.kafka_producer = await iniciar_producer_kafka()
    logger.info("Iniciando aplicación...")

    yield  # la app atiende requests mientras está "pausada" acá

    # ---------- SHUTDOWN ----------
    # Se ejecuta al apagar el servidor (Ctrl+C, SIGTERM, etc.).
    # Acá se liberan los recursos creados en el startup, por ejemplo:
    #   await app.state.db.close()
    #   await app.state.kafka_producer.stop()
    logger.info("Apagando aplicación...")


app = FastAPI(title="API de Items", version="0.2.0", lifespan=lifespan)

app.include_router(items_router)


@app.get("/")
def root():
    return {"mensaje": "Hola desde FastAPI"}


@app.get("/health")
def health():
    return {"status": "ok"}
