import pytest
import json
import time
from fastapi.testclient import TestClient
from a import app 


@pytest.fixture
def client():
    return TestClient(app)

def test_contactos(client):
    response = client.get("/billetera/contactos?minumero=1")
    assert response.status_code==200 and response.json()=={"2":"Gabriel","3":"Juan"}

def test_envio_dinero(client):
    response = client.get("/billetera/pagar?minumero=2&numerodestino=3&valor=100")
    assert response.status_code==200 and ("info" in response.json())


def test_envio_dinero_2(client):
    response = client.get("/billetera/pagar?minumero=1&numerodestino=3&valor=25")
    assert response.status_code==200 and ("info" in response.json())

def test_historial(client):
    response = client.get("/billetera/historial?minumero=2")
    assert response.status_code==200 and (response.json()=={'0': 'Pago realizado de 100.0 a 3'})

def test_malo_contactos(client):
    response = client.get("/billetera/historial?minumero=222")
    assert response.status_code==404 and (response.json()["detail"]=="User not found")

def test_malo_envio_dinero(client):
    response = client.get("/billetera/pagar?minumero=1&numerodestino=2&valor=10000")
    assert response.status_code==500 and (response.json()["detail"]=="Not enough funds")

