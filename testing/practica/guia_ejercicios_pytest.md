# Guía de ejercicios — Pytest básico y Fixtures

## Objetivo

Practicar los conceptos fundamentales de Pytest mediante ejercicios progresivos:

- Crear y ejecutar tests.
- Usar `assert`.
- Probar distintos casos.
- Comprobar excepciones con `pytest.raises`.
- Crear y utilizar fixtures.
- Usar fixtures con `yield`.
- Comprender `autouse`.
- Comprender `scope`.
- Utilizar `conftest.py`.
- Parametrizar tests con `pytest.mark.parametrize`.

---

# 1. Preparación del proyecto

Crear la siguiente estructura:

```text
pytest-practica/
├── src/
│   └── operaciones.py
├── tests/
│   └── test_operaciones.py
└── pyproject.toml
```

Si utilizás `uv`:

```bash
uv init
uv add --dev pytest
```

Ejecutar los tests:

```bash
uv run pytest
```

También podés utilizar:

```bash
pytest
```

si Pytest está disponible directamente en tu entorno.

---

# Ejercicio 1 — Primer test

Crear `src/operaciones.py`:

```python
def suma(a, b):
    return a + b
```

Crear `tests/test_operaciones.py`.

### Consigna

Crear un test que compruebe que:

```text
2 + 3 = 5
```

### Preguntas

1. ¿Cómo debe llamarse la función de test para que Pytest la encuentre automáticamente?
2. ¿Qué ocurre si el `assert` falla?
3. ¿Qué información muestra Pytest?

---

# Ejercicio 2 — Varios casos

Agregar:

```python
def resta(a, b):
    return a - b
```

Crear tests para:

```text
5 - 3 = 2
10 - 5 = 5
3 - 5 = -2
0 - 0 = 0
```

### Desafío

Crear un test independiente para cada caso.

---

# Ejercicio 3 — `assert`

Crear:

```python
def es_par(numero):
    return numero % 2 == 0
```

### Consigna

Crear tests para:

```text
2 → True
4 → True
7 → False
9 → False
0 → True
```

Utilizar:

```python
assert resultado is True
```

o:

```python
assert resultado is False
```

---

# Ejercicio 4 — Listas

Crear:

```python
def obtener_pares(numeros):
    return [numero for numero in numeros if numero % 2 == 0]
```

### Consigna

Probar los siguientes casos:

```text
[1, 2, 3, 4] → [2, 4]

[1, 3, 5] → []

[2, 4, 6] → [2, 4, 6]

[] → []
```

### Pregunta

¿Por qué es importante probar también el caso de una lista vacía?

---

# Ejercicio 5 — Excepciones

Crear:

```python
def dividir(a, b):
    return a / b
```

### Consigna

Crear tests para:

```text
10 / 2 → 5
10 / 0 → ZeroDivisionError
```

Para el segundo caso utilizar:

```python
pytest.raises
```

Ejemplo de estructura:

```python
def test_dividir_por_cero():
    with pytest.raises(ZeroDivisionError):
        dividir(10, 0)
```

### Desafío

Probar también:

```text
0 / 10 → 0
-10 / 2 → -5
```

---

# Ejercicio 6 — Excepciones y mensajes

Crear:

```python
def validar_edad(edad):
    if edad < 0:
        raise ValueError("La edad no puede ser negativa")

    return True
```

### Consigna

Crear tests para:

```text
18 → True
0 → True
-1 → ValueError
```

Para el caso negativo comprobar también el mensaje:

```text
"La edad no puede ser negativa"
```

Investigar cómo utilizar:

```python
pytest.raises(..., match=...)
```

---

# Ejercicio 7 — Primera fixture

Crear una fixture que devuelva:

```python
{
    "nombre": "Juan",
    "edad": 30
}
```

### Consigna

Utilizar la fixture en dos tests:

```text
test_nombre_usuario
test_edad_usuario
```

Comprobar:

```text
nombre → Juan
edad → 30
```

### Pregunta

¿Qué ventaja tiene utilizar una fixture en lugar de crear el diccionario dentro de cada test?

---

# Ejercicio 8 — Fixture reutilizable

Crear:

```python
def calcular_iva(precio):
    return precio * 1.21
```

Crear una fixture llamada `precio` que devuelva:

```text
100
```

Crear un test que compruebe:

```text
100 → 121
```

### Desafío

Crear otra fixture que devuelva una lista de precios:

```text
[100, 200, 300]
```

y utilizarla en un test.

---

# Ejercicio 9 — Fixture con `yield`

Crear una fixture que genere un archivo temporal:

```text
test_file.txt
```

El archivo debe contener:

```text
Hola mundo
prueba
```

La fixture debe:

1. Crear el archivo.
2. Hacer `yield`.
3. Eliminar el archivo después del test.

Conceptualmente:

```text
fixture
   │
   ├── crear archivo
   │
   ├── yield
   │      ↓
   │    test
   │
   └── eliminar archivo
```

### Consigna

Crear un test que compruebe que el archivo existe y contiene el texto esperado.

### Desafío

Comprobar después del test que el archivo fue eliminado.

---

# Ejercicio 10 — `autouse=True`

Crear una fixture:

```python
@pytest.fixture(autouse=True)
def preparar():
    print("Preparando test")
```

Crear dos tests.

### Consigna

Comprobar cuándo se ejecuta la fixture.

Probar primero:

```python
@pytest.fixture
```

y después:

```python
@pytest.fixture(autouse=True)
```

### Pregunta

¿Cuál es la diferencia?

### Reflexión

¿Por qué puede ser peligroso abusar de `autouse=True`?

---

# Ejercicio 11 — Scope

Crear una fixture con:

```python
@pytest.fixture(scope="function")
```

y otra con:

```python
@pytest.fixture(scope="module")
```

Agregar mensajes:

```python
print("Creando fixture")
```

Crear varios tests que utilicen la fixture.

### Consigna

Observar cuántas veces se ejecuta.

Comparar:

```text
function
module
```

### Desafío

Investigar qué ocurre con:

```text
session
class
```

---

# Ejercicio 12 — Mini proyecto: usuarios

Crear:

```python
def crear_usuario(nombre, edad):
    if not nombre:
        raise ValueError("El nombre es obligatorio")

    if edad < 0:
        raise ValueError("La edad no puede ser negativa")

    return {
        "nombre": nombre,
        "edad": edad,
    }


def es_mayor_de_edad(usuario):
    return usuario["edad"] >= 18
```

### Tests requeridos

Para `crear_usuario`:

- [ ] Crear usuario correctamente.
- [ ] Nombre vacío genera `ValueError`.
- [ ] Edad negativa genera `ValueError`.
- [ ] Edad 0 funciona.
- [ ] Edad 18 funciona.
- [ ] Edad 50 funciona.

Para `es_mayor_de_edad`:

- [ ] 17 → `False`
- [ ] 18 → `True`
- [ ] 30 → `True`

### Requisitos

Utilizar en este ejercicio:

- `assert`
- `pytest.raises`
- fixture

---

# Ejercicio 13 — Mini proyecto: archivos

Crear una función:

```python
def contar_lineas(nombre_archivo):
    with open(nombre_archivo, "r") as archivo:
        return len(archivo.readlines())
```

Crear una fixture que prepare un archivo:

```text
Hola mundo
Python
Pytest
```

### Consigna

Testear:

```text
contar_lineas(...) → 3
```

La fixture debe encargarse de:

```text
crear archivo
      ↓
yield
      ↓
ejecutar test
      ↓
eliminar archivo
```

### Desafío

Crear un segundo test que compruebe qué ocurre si el archivo no existe.

---

# Ejercicio 14 — Integración de conceptos

Crear una función:

```python
def calcular_promedio(numeros):
    if not numeros:
        raise ValueError("La lista no puede estar vacía")

    return sum(numeros) / len(numeros)
```

### Tests

Probar:

```text
[1, 2, 3] → 2
[10, 20] → 15
[5] → 5
[] → ValueError
```

### Requisitos

Utilizar:

- `pytest.raises`

---

# Desafío final

Crear un pequeño proyecto de gestión de productos.

Cada producto tendrá:

```python
{
    "nombre": "Notebook",
    "precio": 1000,
    "stock": 5
}
```

Crear funciones:

```python
def crear_producto(nombre, precio, stock):
    ...


def hay_stock(producto):
    ...


def calcular_total(producto, cantidad):
    ...
```

### Reglas

`crear_producto` debe rechazar:

```text
nombre vacío
precio negativo
stock negativo
```

`hay_stock` debe devolver:

```text
True  → si stock > 0
False → si stock == 0
```

`calcular_total` debe calcular:

```text
precio × cantidad
```

y debe generar un error si:

```text
cantidad <= 0
cantidad > stock
```

### Tests requeridos

- [ ] Tests de creación correcta.
- [ ] Tests de validaciones.
- [ ] Tests de excepciones.
- [ ] Tests de stock.
- [ ] Tests de cálculo.
- [ ] Fixture para crear productos.
- [ ] Fixture para diferentes productos.
- [ ] Al menos un caso de cleanup utilizando `yield`.

---

# Comandos útiles

Ejecutar todos los tests:

```bash
pytest
```

Ejecutar mostrando los tests:

```bash
pytest -v
```

Ejecutar un archivo:

```bash
pytest tests/test_usuarios.py
```

Ejecutar un test específico:

```bash
pytest tests/test_usuarios.py::test_nombre_usuario
```

Mostrar `print()`:

```bash
pytest -s
```

Detenerse en el primer error:

```bash
pytest -x
```

Mostrar más información:

```bash
pytest -vv
```

---

# Checklist final

Al terminar la guía deberías poder explicar:

- [ ] ¿Qué es Pytest?
- [ ] ¿Cómo descubre los tests?
- [ ] ¿Qué hace `assert`?
- [ ] ¿Cómo se testean excepciones?
- [ ] ¿Qué es una fixture?
- [ ] ¿Para qué sirve `yield` en una fixture?
- [ ] ¿Qué hace `autouse=True`?
- [ ] ¿Qué significa `scope="function"`?
- [ ] ¿Qué significa `scope="module"`?
- [ ] ¿Para qué sirve `conftest.py`?
- [ ] ¿Cuándo utilizarías una fixture?
- [ ] ¿Cuándo utilizarías `pytest.raises`?
- [ ] ¿Cómo ejecutarías un único test?

## Siguiente nivel

Una vez terminados estos ejercicios, los siguientes temas recomendados son:

```text
Pytest básico
     ↓
Fixtures
     ↓
Mocking
     ↓
pytest-mock
     ↓
Testing de APIs
     ↓
FastAPI + TestClient
     ↓
Tests de base de datos
     ↓
Integration tests
```
