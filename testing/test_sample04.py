# instalar pytest-mock --  uv add pytest-mock --dev
import pytest
import requests


from sample04 import get_url


class GetResponse:
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text


def test_get_url_status_code_ok(mocker):

    response_esperado = GetResponse(200, "Hola")

    mocker.patch.object(requests, "get", return_value=response_esperado)
    status, _ = get_url("http://dominio.com")

    assert status == response_esperado.status_code


def test_get_url_text_ok(mocker):

    response_esperado = GetResponse(200, "Hola")

    mocker.patch.object(requests, "get", return_value=response_esperado)
    _, text = get_url("http://dominio.com")

    assert text == response_esperado.text
