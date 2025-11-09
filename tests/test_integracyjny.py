from fastapi.testclient import TestClient
from main import app
from faker import Faker
import pytest

fake = Faker()

client = TestClient(app)

@pytest.fixture
def base():
    return 'https://unacerbic-lorenza-glomerate.ngrok-free.dev/'

@pytest.fixture
def head(base):
    username = fake.user_name()
    email = fake.email()
    password = fake.password()
    reg = client.post(f'{base}register', json={'username': username, 'email': email, 'password': password})
    log = client.post(f'{base}login', json={'username': username, 'email': email, 'password': password})
    token = log.json()['access_token']
    header = {'Authorization': f'Bearer {token}'}
    return header

def test_delete_user(head, base):
    dele = client.delete(f'{base}users/me', headers=head)
    assert dele.status_code == 204
    gett = client.get(f'{base}users/me', headers=head)
    assert gett.json() == {'detail': 'Invalid or expired token'}
