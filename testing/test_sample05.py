from datetime import datetime

import pytest

from sample05 import get_saludo


def test_get_saludo(mocker):
    fake_hour = datetime(2026, 1, 1, 9, 0, 0)

    mocker.patch("sample05.datetime")
    mocker.patch("sample05.datetime.now", return_value=fake_hour)

    saludo = get_saludo()

    assert saludo == "Buen dia"
