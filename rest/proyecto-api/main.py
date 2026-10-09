import json

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException

from pydantic import BaseModel


class AccesorioCreate(BaseModel):
    partNumber: str
    name: str
    description: str
    currency: str
    price: float


@asynccontextmanager
async def lifespam(app: FastAPI):
    print("Iniciando servidor.....")
    with open("accesorios.json") as file:
        app.db = json.load(file)

    yield

    print("Apagando servidor....")
    with open("accesorios.json", "w") as file:
        json.dump(app.db, file)


app = FastAPI(lifespan=lifespam)

# Accesorios
# listar accesorios --


@app.get("/accesorios/")
def listar_accesorios(limit: int = 10, skip: int = 0):

    accesorios_list = app.db[skip:skip+limit]

    return {
        "accesorios": accesorios_list,
        "total": len(app.db)
    }


@app.get("/accesorios/{part_number}/")
def read_item(part_number: str):

    for accesorio in app.db:
        if accesorio["partNumber"] == part_number:
            accesorio_obj = accesorio
            return {"accesorio": accesorio_obj}

    raise HTTPException(
        status_code=404,
        detail=f"Accesorio on partNumber {part_number} no encontrado"
    )


@app.post("/accesorios/")
def crear_accesorio(accesorio: AccesorioCreate):

    app.db.append(accesorio.model_dump())

    return {"accesorio": accesorio}


# health-check
@app.get("/")
def read_root():
    return {"ping": "pong"}


# class Usuario(BaseModel):
#     userid: str
#     product: list
# productos = [x**2 for x in range(20)]
# productos1 = list(range(5000))  # [ 0, 1, 2, 3, 4 ...]
# productos2 = list(range(20))
# productos3 = list(range(30))
# 
# usuarios = {
#     "1": productos1,
#     "2": productos2,
#     "3": productos3
# }
# 
# 
# # health-check
# @app.get("/")
# def read_root():
#     return {"ping": "pong"}
# 
# 
# # endpoint 3 - path -- path con type
# @app.get("/productos/{producto_id}/")
# def read_item(producto_id: int):
#     return {"producto": {"id": productos[producto_id]}}
# 
# 
# # endpoint listar productos -- falta paginacion  
# @app.get("/productos/")
# def read_product(limit: int = 10, skip: int = 0):
# 
#     prod_list = []
# 
#     for i in range(skip, limit+skip):
#         prod_list.append({"id": productos[i]})
# 
#     count = len(productos)
# 
#     return {
#         "productos": prod_list,
#         "total": count
#     }
# 
# 
# @app.get("/usuario/{user_id}/productos/{product_id}")
# def get_user_1_products(user_id: str, product_id: int):
# 
#     return {
#         "producto": usuarios[user_id][product_id]
#     }
# 
# 
# # Vamos a generar un usuario nuevo
# @app.post("/usuarios")
# def crear_usuario(body: Usuario):
#     print(body)
#     usuarios[body.userid] = body.product
# 
#     return {"status": "OK "}
# 