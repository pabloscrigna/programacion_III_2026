# API de Items (FastAPI)

API REST para gestionar items, hecha con [FastAPI](https://fastapi.tiangolo.com/) y [uv](https://docs.astral.sh/uv/).
Por ahora los datos se guardan en memoria (se pierden al reiniciar el servidor).

## Requisitos

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Python 3.13 (si no lo tenés, uv lo descarga solo)

## Cómo levantarla

```bash
uv sync              # crea .venv e instala las dependencias
uv run fastapi dev   # servidor de desarrollo con recarga automática
```

- API: http://localhost:8000
- Documentación interactiva (Swagger): http://localhost:8000/docs
- Documentación alternativa (ReDoc): http://localhost:8000/redoc

Para producción: `uv run fastapi run`.

## Estructura

```
app/
├── main.py              # crea la app e incluye los routers
└── items/
    ├── models.py        # modelos Pydantic (schemas)
    ├── repository.py    # acceso a datos (en memoria)
    └── router.py        # endpoints /items
```

## Modelos

| Modelo       | Uso                                   | Campos                                              |
|--------------|---------------------------------------|-----------------------------------------------------|
| `ItemBase`   | Campos comunes                        | `nombre`, `precio`, `descripcion`                   |
| `ItemCreate` | Body de `POST` y `PUT`                | igual que `ItemBase`                                |
| `ItemUpdate` | Body de `PATCH` (todos opcionales)    | `nombre`, `precio`, `descripcion`                   |
| `ItemRead`   | Respuesta de la API                   | `ItemBase` + `id`, `creado_en`, `actualizado_en`    |

Validaciones:

- `nombre`: entre 1 y 100 caracteres.
- `precio`: mayor a 0.
- `descripcion`: opcional, hasta 500 caracteres.

En `PATCH` sólo se modifican los campos enviados. `descripcion` se puede borrar mandando `null`;
`nombre` y `precio` no aceptan `null`.

## Endpoints

| Método | Ruta          | Descripción              | Respuesta OK |
|--------|---------------|--------------------------|--------------|
| GET    | `/`           | Mensaje de bienvenida    | 200          |
| GET    | `/health`     | Healthcheck              | 200          |
| GET    | `/items`      | Lista todos los items    | 200          |
| GET    | `/items/{id}` | Obtiene un item          | 200          |
| POST   | `/items`      | Crea un item             | 201          |
| PUT    | `/items/{id}` | Reemplaza un item        | 200          |
| PATCH  | `/items/{id}` | Actualiza parcialmente   | 200          |
| DELETE | `/items/{id}` | Borra un item            | 204          |

Errores: `404` si el item no existe, `422` si el body no pasa la validación.

## Ejemplos

```bash
# Crear
curl -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Teclado", "precio": 15000, "descripcion": "Mecánico"}'

# Listar
curl http://localhost:8000/items

# Actualizar sólo el precio
curl -X PATCH http://localhost:8000/items/1 \
  -H "Content-Type: application/json" \
  -d '{"precio": 12000}'

# Borrar
curl -X DELETE http://localhost:8000/items/1
```

Respuesta de ejemplo:

```json
{
  "nombre": "Teclado",
  "precio": 15000.0,
  "descripcion": "Mecánico",
  "id": 1,
  "creado_en": "2026-11-19T22:33:28.451160Z",
  "actualizado_en": "2026-11-19T22:33:28.451160Z"
}
```

## Dependencias

```bash
uv add <paquete>          # agregar dependencia
uv add --dev <paquete>    # agregar dependencia de desarrollo
```
