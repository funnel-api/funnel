import pytest

from funnel.core import create_app
from funnel.core import register


@pytest.fixture
def client():
    with create_app().test_client() as client:
        yield client


CLS_NAME = "My_Function"


def func1(a, b=1):
    return {"result": a + b}


def func2(a, b=1, *args, c, d=2, **kwargs):
    val = a + b + sum(args) + c + d + sum(kwargs.values())
    return {"result": val}


def test_root_url(client):
    register(func1, CLS_NAME, "/")
    response = client.post(
        "/",
        json={"a": 10},
    )
    data = response.json
    assert data == {"result": 11}


def test_urls(client):
    register(func1, CLS_NAME, "/myfunction", "/my/function")
    response = client.post(
        "/myfunction",
        json={"a": 10},
    )
    data = response.json
    assert data == {"result": 11}
    response = client.post(
        "/my/function",
        json={"a": 10},
    )
    data = response.json
    assert data == {"result": 11}


def test_func2(client):
    register(func2, CLS_NAME, "/")
    response = client.post(
        "/",
        json={
            "a": 10,
            "args": [1, 2, 3],
            "c": 4,
            "kwargs": {
                "e": 5,
                "f": 6,
            },
        },
    )
    data = response.json
    assert data == {"result": 34}


def test_missing_arg(client):
    register(func1, CLS_NAME, "/")
    response = client.post(
        "/",
        json={"b": 10},
    )
    data = response.json
    assert data == {"message": "a is missing"}


def test_missing_kwarg(client):
    register(func2, CLS_NAME, "/")
    response = client.post(
        "/",
        json={
            "a": 10,
        },
    )
    data = response.json
    assert data == {"message": "c is missing"}
