from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = None
    price: float = Field(ge=0)


class ItemOut(ItemCreate):
    id: str


def item_from_doc(doc: dict) -> ItemOut:
    return ItemOut(id=str(doc.pop("_id")), **doc)