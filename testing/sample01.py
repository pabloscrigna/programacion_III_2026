def numero_de_elementos(datos: list[int]) -> int:
    return len(datos)


def obtener_valor_minimo(datos: list[int]) -> int:
    datos.sort()
    return datos[0]


def obtener_valor_maximo(datos: list[int]) -> int:
    datos.sort()
    return datos[-1]


if __name__ == "__main__":
    sample = [0, 9, 5, 7, 1]

    print("cantidad de elementos: ", numero_de_elementos(sample))
    print("Minimo: ", obtener_valor_minimo(sample))
    print("Maximo: ", obtener_valor_maximo(sample))

try:
    obtener_valor_maximo([])
except (IndexError, AttributeError):
    print("Error")
