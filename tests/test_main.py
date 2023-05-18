from flask import Flask, session
import pytest
import main

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True

    app.route('/login', methods=['GET'])(main.login_get)
    app.route('/login', methods=['POST'])(main.login_post)
    app.route('/auth', methods=['GET'])(main.auth_get)
    app.route('/auth', methods=['POST'])(main.auth_post)
    app.route('/account', methods=['GET'])(main.account_get)
    app.route('/account', methods=['POST'])(main.account_transaction)
    app.route('/submit_currency', methods=['POST'])(main.serve_currencies)

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()


def test_login_get(client):
    response = client.get('/login')
    assert response.status_code == 200


def test_login_post(client):
    user = 'jaroslavbelina.ml@seznam.cz'
    '''correct user'''
    response = client.post("/login", data={
            "user": user,
            "pwd": "123456789"
            }, follow_redirects=True)
    assert response.request.path == "/auth"

    '''incorrect user'''
    response = client.post("/login", data={
        "user": user + 'bogus',
        "pwd": "123456789"
    }, follow_redirects=True)
    assert response.request.path == "/login"

def test_auth_get(client):
    response = client.get('/auth')
    assert response.status_code == 200

def test_auth_post(client):
    '''correct auth'''
    user = 'jaroslavbelina.ml@seznam.cz'
    response_login = client.post("/login", data={
        "user": user,
        "pwd": "123456789"
    })
    key = main.users['jaroslavbelina.ml@seznam.cz'].key
    client.set_cookie('localhost', 'user', user)
    client.set_cookie('localhost', 'key', key)
    response = client.post('/auth', data={
        "key": key
    }, follow_redirects=True)
    assert response.request.path == "/account"

    '''Incorrect auth'''
    response = client.post('/auth', data={
        "key": '.'
    }, follow_redirects=True)
    assert response.request.path == "/login"
