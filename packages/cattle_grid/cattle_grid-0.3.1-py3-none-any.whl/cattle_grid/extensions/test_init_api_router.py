from fastapi import FastAPI
from fastapi.testclient import TestClient

from . import Extension
from .load import add_routes_to_api


def test_api_router():
    ext = Extension("test", api_prefix="/test", module=__name__)
    result = {"extension": "yes"}

    @ext.get("/")
    async def root_path():
        return result

    ext.configure({})

    app = FastAPI()
    add_routes_to_api(app, [ext])

    test_client = TestClient(app)

    response = test_client.get("/test")

    assert response.status_code == 200

    data = response.json()

    assert data == result
