"""Modelos (schemas Pydantic) del recurso Item.

Cada modelo cumple un rol distinto:
- ItemBase:   campos comunes compartidos por los demás modelos.
- ItemCreate: lo que el cliente envía para crear un item (POST).
- ItemUpdate: actualización parcial, todos los campos opcionales (PATCH).
- ItemRead:   lo que la API devuelve (incluye campos generados por el servidor).
"""

from datetime import datetime

from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100, examples=["Teclado"])
    precio: float = Field(..., gt=0, examples=[15000.0])
    descripcion: str | None = Field(None, max_length=500, examples=["Mecánico, switches rojos"])


class ItemCreate(ItemBase):
    """Body del POST /items y del PUT /items/{id} (reemplazo completo)."""


class ItemUpdate(BaseModel):
    """Body del PATCH /items/{id}: sólo se modifican los campos enviados."""

    # Tipo `str` / `float` (no `| None`): se pueden omitir, pero no mandar null,
    # porque nombre y precio son obligatorios en el item.
    nombre: str = Field(None, min_length=1, max_length=100)
    precio: float = Field(None, gt=0)
    descripcion: str | None = Field(None, max_length=500)


class ItemRead(ItemBase):
    """Respuesta de la API."""

    id: int
    creado_en: datetime
    actualizado_en: datetime
