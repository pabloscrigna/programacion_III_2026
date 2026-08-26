import requests


# cada vez que hacemos un requests HTTP (GET (READ item/list) - POST (create item) - PUT/PATCH (update) - DELETE (item) )
# respuesta:


def get_url(url: str) -> tuple:
    r = requests.get(url)

    return r.status_code, r.text


if __name__ == "__main__":
    # response = requests.get("https://ole.com.ar")
    url = "https://ole.com.ar"
    response = get_url(url)
    print(f"status code :  {response[0]}")
