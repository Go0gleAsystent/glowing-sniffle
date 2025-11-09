from aplikacja import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_add():
    add = client.post('jakisurl', json={'jdjd': 'wefe'})
    assert add.status_code == 200