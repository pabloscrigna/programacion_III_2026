"""
Funcion que lea un archivo y retorne el contenido
"""


def leer_archivo(archivo: str) -> str:

    with open(archivo, "r") as file:
        return file.read()


# Pruebas


def cuenta_caracteres(frase):
    return len(frase)


def separar(frase):
    return frase.split()


def frase_capitalize(frase):
    return frase.capitalize()


if __name__ == "__main__":
    print(leer_archivo("demo.txt"))
    frase = "hola mundo"
    print("cuente: ", cuenta_caracteres(frase))
    print("separar: ", separar(frase))
    print("capitalize: ", frase_capitalize(frase))
