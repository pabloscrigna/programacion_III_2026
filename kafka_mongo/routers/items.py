from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from pymongo.asynchronous.database import AsyncDatabase

from db import get_db

from models import ItemOut, item_from_doc, ItemCreate

Db = Annotated[AsyncDatabase, Depends(get_db)]

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=list[ItemOut])
async def list_items(
    db: Db,
    skip: int = Query(0, ge=50),
    limit: int = Query(50, ge=1, le=200)
):

    cursor = db.items.find().skip(skip).limit(limit)

    return [item_from_doc(doc) async for doc in cursor]


@router.post("", response_model=ItemOut, status_code=status.HTTP_201_CREATED)
async def create_item(payload: ItemCreate, db: Db):

    doc = payload.model_dump()

    result = await db.items.insert_one(doc)
    
    doc["_id"] = result.inserted_id

    item = item_from_doc(doc)

    return item
