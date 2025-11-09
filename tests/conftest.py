import pytest
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base


@pytest.fixture
def user_id(bf, head):
    gett = bf.get_me(head).json()
    return gett.get('id')

@pytest.fixture
def base():
    return 'https://unacerbic-lorenza-glomerate.ngrok-free.dev'

@pytest.fixture
def test_db():
    engine = create_engine('sqlite:///:memory:', echo=False)

    Base.metadata.create_all(bind=engine)

    ses = sessionmaker(bind=engine)

    session = ses()

    yield session

    session.close()
    engine.dispose()


class basicfunction:
    def __init__(self, base):
        self.base = base

    def register(self, name, email, password):
        return requests.post(f'{self.base}/register', json={'username': name, 'email': email, 'password': password})
    def login(self, name, email, password):
        return requests.post(f'{self.base}/login', json={'username': name, 'email': email, 'password': password})
    
    def get_me(self, head):
        return requests.get(f'{self.base}/users/me', headers=head)

    def delete_me(self, head):
        return requests.delete(f'{self.base}/users/me', headers=head)
    
class postfunctions:
    def __init__(self, base):
        self.base = base
    
    def add_post(self, title, cotent, head):
        return requests.post(f'{self.base}/posts', json={'title': title, 'content': cotent}, headers=head)
    
    def get_post_by_id(self, id):
        return requests.get(f'{self.base}/posts/{id}')
    def edit_post(self, id, title, content, head):
        return requests.put(f'{self.base}/posts/{id}', json={'title': title, 'content': content}, headers=head)
    def delete_post(self, id, head):
        return requests.delete(f'{self.base}/posts/{id}', headers=head)
    
class comment:
    def __init__(self, base):
        self.base = base

    def add_comment(self, id, content, head):
        return requests.post(f'{self.base}/posts/{id}/comments', json={'content': content}, headers=head)
    
@pytest.fixture
def bf(base):
    return basicfunction(base)

@pytest.fixture
def pf(base):
    return postfunctions(base)

@pytest.fixture
def cm(base):
    return comment(base)

