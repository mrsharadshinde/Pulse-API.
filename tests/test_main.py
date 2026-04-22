# test/test_main.py
from http import client


def test_root_route(client):
    #1. make fake GET req
    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {"message": "Welcome to pulse | All in one social app"}

