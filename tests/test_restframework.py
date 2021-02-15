from rest_framework import status
from rest_framework.test import APIClient


def test_restframework_types() -> None:
    client = APIClient()
    res = client.get("/api/v1/foo")
    assert res.status_code == status.HTTP_200_OK
    print(res.data)
    assert res.json() == {"test": "foo"}
