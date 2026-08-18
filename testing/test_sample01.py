import pytest

from sample01 import numero_de_elementos, obtener_valor_minimo


def test_obtener_numero_de_elemntos_OK():
    datos = [0, 4, 7]
    cant_datos = 3

    cant = numero_de_elementos(datos)

    assert cant_datos == cant


def test_obtener_valor_minimo_OK():
    datos = [4, 0, 2]

    minimo = obtener_valor_minimo(datos)

    assert minimo == 0


def test_obtener_minimo_atterror():
    datos = ""

    with pytest.raises(AttributeError):
        obtener_valor_minimo(datos)


def test_obtener_minimo_indexerror():
    datos = []

    with pytest.raises(IndexError):
        obtener_valor_minimo(datos)
