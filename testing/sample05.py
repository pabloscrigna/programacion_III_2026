from datetime import datetime


def get_saludo():

    hora = datetime.now().hour
    print("hora: ", hora)

    if hora < 12:
        return "Buen dia"
    else:
        return "Buenas noches"


if __name__ == "__main__":
    get_saludo()
