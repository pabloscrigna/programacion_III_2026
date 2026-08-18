import pytest

from sample03 import cuenta_caracteres, frase_capitalize, leer_archivo, separar


def test_leer_archivo_OK():

    with open("file_dummy.txt", "w") as file:
        file.write("Hola mundo!!!")

    texto = "Hola mundo!!!"
    assert leer_archivo("file_dummy.txt") == texto


# fixture
@pytest.fixture
def get_frase():
    return "chau mundo"


def test_separar_OK(get_frase):
    assert separar(get_frase) == ["chau", "mundo"]


def test_cuenta_caracteres_OK(get_frase):
    assert cuenta_caracteres(get_frase) == 10


def test_frase_capitalize_OK(get_frase):
    frase = get_frase
    assert frase_capitalize(frase) == "Chau mundo"
