import pytest

from sample02 import suma


def test_suma_OK():
    assert suma(5, 6) == 11


def test_typeerror():

    with pytest.raises(TypeError):
        assert suma("a", 5, 8)
