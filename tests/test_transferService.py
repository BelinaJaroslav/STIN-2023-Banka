import pytest
from Server.TransferService import *
from Server.User import User
from decimal import Decimal
from Server.User import User


@pytest.fixture
def user():
    email = "jaroslav@gmail.com"
    name = "Jaroslav"
    surname = "Belina"
    password = "123456"
    user = User(email, name, surname, password)
    user.account['CZK'] = 4000
    user.account['EUR'] = 500
    return user


def test_payment_incoming_czk(user):
    currency = 'CZK'
    amount = 400
    payment_incoming(user, amount, currency)
    assert user.account['CZK'] == 4400

def test_payment_outgoing_czk(user):
    currency = 'CZK'
    amount = 400
    payment_outgoing(user, amount, currency)
    assert user.account['CZK'] == 3600

def test_payment_outgoing_czk_sub_zero(user):
    currency = 'CZK'
    amount = 4400
    payment_outgoing(user, amount, currency)
    assert user.account['CZK'] == 4000

def test_payment_outgoing_eur(user):
    currency = 'EUR'
    amount = 490
    payment_outgoing(user, amount, currency)
    assert user.account['EUR'] == 10
    amount = 20
    payment_outgoing(user, amount, currency)
    assert user.account['EUR'] == 10 and user.account['CZK'] < 4000

def test_process_payment(user):
    currency = 'EUR'
    amount = 490
    process_payment(user, amount, currency)
    assert user.account['EUR'] == 990
    amount = -100
    process_payment(user, amount, currency)
    assert user.account['EUR'] == 890
    currency = 'CZK'
    process_payment(user, amount, currency)
    assert user.account['CZK'] == 3900