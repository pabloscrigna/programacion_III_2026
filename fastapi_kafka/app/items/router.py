"""Endpoints del recurso Item."""

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.items.models import ItemCreate, ItemRead, ItemUpdate
from app.items.repository import ItemRepository, get_repo

router = APIRouter(prefix="/items", tags=["items"])


def _no_encontrado() -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")


@router.get("", response_model=list[ItemRead])
def listar_items(repo: ItemRepository = Depends(get_repo)):
    
    return repo.listar()


@router.get("/{item_id}", response_model=ItemRead)
def obtener_item(item_id: int, repo: ItemRepository = Depends(get_repo)):
    item = repo.obtener(item_id)
    if item is None:
        raise _no_encontrado()
    return item


@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def crear_item(data: ItemCreate, repo: ItemRepository = Depends(get_repo)):
    return repo.crear(data)


@router.put("/{item_id}", response_model=ItemRead)
def reemplazar_item(item_id: int, data: ItemCreate, repo: ItemRepository = Depends(get_repo)):
    item = repo.reemplazar(item_id, data)
    if item is None:
        raise _no_encontrado()
    return item


@router.patch("/{item_id}", response_model=ItemRead)
def actualizar_item(item_id: int, data: ItemUpdate, repo: ItemRepository = Depends(get_repo)):
    item = repo.actualizar(item_id, data)
    if item is None:
        raise _no_encontrado()
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_item(item_id: int, repo: ItemRepository = Depends(get_repo)):
    if not repo.borrar(item_id):
        raise _no_encontrado()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
