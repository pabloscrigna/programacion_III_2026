"""Acceso a datos de Items. Por ahora es una "base de datos" en memoria."""

from datetime import datetime, timezone

from app.items.models import ItemCreate, ItemRead, ItemUpdate


class ItemRepository:
    def __init__(self) -> None:
        self._items: dict[int, ItemRead] = {}
        self._next_id = 1

    def listar(self) -> list[ItemRead]:
        return list(self._items.values())

    def obtener(self, item_id: int) -> ItemRead | None:
        return self._items.get(item_id)

    def crear(self, data: ItemCreate) -> ItemRead:
        ahora = datetime.now(timezone.utc)
        item = ItemRead(
            id=self._next_id,
            creado_en=ahora,
            actualizado_en=ahora,
            **data.model_dump(),
        )
        self._items[item.id] = item
        self._next_id += 1
        return item

    def reemplazar(self, item_id: int, data: ItemCreate) -> ItemRead | None:
        actual = self._items.get(item_id)
        if actual is None:
            return None
        item = ItemRead(
            id=item_id,
            creado_en=actual.creado_en,
            actualizado_en=datetime.now(timezone.utc),
            **data.model_dump(),
        )
        self._items[item_id] = item
        return item

    def actualizar(self, item_id: int, data: ItemUpdate) -> ItemRead | None:
        actual = self._items.get(item_id)
        if actual is None:
            return None
        cambios = data.model_dump(exclude_unset=True)
        cambios["actualizado_en"] = datetime.now(timezone.utc)
        item = actual.model_copy(update=cambios)
        self._items[item_id] = item
        return item

    def borrar(self, item_id: int) -> bool:
        return self._items.pop(item_id, None) is not None


# Instancia única compartida por la app
repo = ItemRepository()


def get_repo() -> ItemRepository:
    """Dependencia de FastAPI (permite reemplazarla en tests)."""
    return repo
