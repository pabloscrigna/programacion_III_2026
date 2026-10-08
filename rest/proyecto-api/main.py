from contextlib import asynccontextmanager
from fastapi import FastAPI

from pydantic import BaseModel


class Usuario(BaseModel):
    userid: str
    product: list


@asynccontextmanager
async def lifespam(app: FastAPI):
    print("Iniciando servidor.....")
    
    yield

    print("Apagando servidor....")


app = FastAPI(lifespan=lifespam)


productos = [x**2 for x in range(20)]
productos1 = list(range(5000))  # [ 0, 1, 2, 3, 4 ...]
productos2 = list(range(20))
productos3 = list(range(30))

usuarios = {
    "1": productos1,
    "2": productos2,
    "3": productos3
}


# health-check
@app.get("/")
def read_root():
    return {"ping": "pong"}


# endpoint 3 - path -- path con type
@app.get("/productos/{producto_id}/")
def read_item(producto_id: int):
    return {"producto": {"id": productos[producto_id]}}


# endpoint listar productos -- falta paginacion  
@app.get("/productos/")
def read_product(limit: int = 10, skip: int = 0):

    prod_list = []

    for i in range(skip, limit+skip):
        prod_list.append({"id": productos[i]})

    count = len(productos)

    return {
        "productos": prod_list,
        "total": count
    }


@app.get("/usuario/{user_id}/productos/{product_id}")
def get_user_1_products(user_id: str, product_id: int):

    return {
        "producto": usuarios[user_id][product_id]
    }


# Vamos a generar un usuario nuevo
@app.post("/usuarios")
def crear_usuario(body: Usuario):
    print(body)
    usuarios[body.userid] = body.product

    return {"status": "OK "}
