from flask import Flask, session
import pytest
import main

@pytest.fixture
def client():
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
    assert response.statuscode == 200


def test_login_post(client):
    response = client.post("/login", data={
            "user": "jaroslavbelina.ml@seznam.cz",
            "pwd": "123456789"
            })
    assert response.statuscode == 302
