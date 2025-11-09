from conftest import test_db, bf, pf, cm, user_id
from models import User, Post, Comment
from faker import Faker
import pytest


fake = Faker()

#==================MODEL'S TESTS===================
def test_model_User(test_db):
    un = fake.user_name()
    el = fake.email()
    ps = fake.password()
    user = User(username=un, email=el, hashed_password=ps)
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)

    assert user.id is not None

def test_model_Post(test_db):
    tit = fake.street_name() #używam tych rzeczy bo w teście nic to nie zmienia prócz tego, że są przejrzyste
    con = fake.user_name()
    post = Post(title=tit, content=con)
    test_db.add(post)
    test_db.commit()
    test_db.refresh(post)

    assert post.id is not None

def test_model_comment(test_db):
    con = fake.user_name() #używam tych rzeczy bo w teście nic to nie zmienia prócz tego, że są przejrzyste
    comment = Comment(content=con)
    test_db.add(comment)
    test_db.commit()
    test_db.refresh(comment)

    assert comment.id is not None

#=====================HEADERS=======================
@pytest.fixture
def head(bf): #teoretycznie jeżeli test_delete działa nie muszę tego testować 
    name = fake.user_name()
    email = fake.email()
    password = fake.password()

    reg = bf.register(name, email, password)


    log = bf.login(name, email, password)

    token = log.json().get("access_token")
    header = {'Authorization': f'Bearer {token}'}
    return header


#===================USER'S TEST====================
def test_delete(bf, head):
    dele = bf.delete_me(head)
    assert dele.status_code == 204
    getme = bf.get_me(head)
    assert getme.json() == {'detail': 'Invalid or expired token'}

#================POST'S TESTS===================

def test_add_post(pf, head, user_id):
    title = fake.user_name() #używam tych rzeczy bo w teście nic to nie zmienia prócz tego, że są przejrzyste
    content = fake.password()
    add = pf.add_post(title, content, head)
    assert add.status_code == 201
    pid = add.json().get('id')
    getjson = pf.get_post_by_id(pid).json()
    ca = getjson['created_at']
    assert getjson == {'id': pid, 'title': title, 'content': content, 'created_at': ca,'user_id': user_id}


def test_edit_post(pf, head, user_id):
    title = fake.user_name() #używam tych rzeczy bo w teście nic to nie zmienia prócz tego, że są przejrzyste
    content = fake.password()
    add = pf.add_post(title, content, head)
    pid = add.json().get('id')
    new_title = fake.password()
    new_content = fake.user_name()
    edit = pf.edit_post(pid, new_title, new_content, head)
    assert edit.status_code == 200
    gett = pf.get_post_by_id(pid).json()
    getjson = pf.get_post_by_id(pid).json()
    ca = getjson['created_at']
    assert gett == {'id': pid, 'title': new_title, 'content': new_content, 'created_at': ca,'user_id': user_id}




    