import sys

sys.path.append('..')

import os
from flask import Flask, render_template, request, redirect, make_response
import smtplib
from email.mime.text import MIMEText
from User import User
import TransferService

app = Flask(__name__)

secret_key = None

print(sys.path)

users = {"jaroslavbelina.ml@seznam.cz": User("jaroslavbelina.ml@seznam.cz", "Jaroslav", "Belina", "123456789")}
user_acc = users["jaroslavbelina.ml@seznam.cz"].account
user_acc['CZK'] = 500
user_acc['CZK'] += 500
user_acc['CZK'] -= 500
user_acc['CZK'] += 1000
user_acc['EUR'] = 500
user_acc['EUR'] -= 100

sender = "stintest@outlook.com"
pw = "Burnerpassword"


# client = new SmtpClient("smtp-mail.outlook.com", 587)

@app.route('/login', methods=['GET'])
def login_get():
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login_post():
    user = request.form['user']
    pwd = request.form['pwd']
    if user in users and users[user].password == pwd:
        secret_key = generate_and_store_key(user)
        send_mail(user, secret_key)
        resp = make_response(redirect('/auth'))
        resp.set_cookie('user', user)
        return resp
    else:
        return redirect('/login')


@app.route('/auth', methods=['GET'])
def auth_get():
    return render_template("auth.html")


@app.route('/auth', methods=['POST'])
def auth_post():
    secret_key = request.form['key']
    user = request.cookies.get('user')
    if user in users and users[user].key == secret_key:
        resp = make_response(redirect('/account'))
        resp.set_cookie('key', secret_key)
        resp.set_cookie('currency', 'CZK')
        return resp
    else:
        return redirect('/login')


@app.route('/account', methods=['GET'])
def account_get():
    if 'user' not in request.cookies or 'key' not in request.cookies:
        return redirect('/login')

    user = request.cookies.get('user')
    account = users[user].account
    secret_key = request.cookies.get('key')
    currency = request.cookies.get('currency')
    try:
        balance = account[currency]
    except:
        pass

    if secret_key != users[user].key:
        return redirect('/login')

    # noinspection PyUnreachableCode
    return render_template("account.html", currencies=account.keys(), transactions=account.get_transactions(currency),
                           currency=currency, balance=balance)


@app.route('/account', methods=['POST'])
def account_transaction():
    user_mail = request.cookies.get('user')
    user = users[user_mail]
    key = request.cookies.get('key')
    amount = float(request.form['amount'])
    currency = request.cookies.get('currency')
    TransferService.process_payment(user, amount, currency)

    resp = make_response(redirect('/account'))
    return resp


@app.route('/submit_currency', methods=['POST'])
def serve_currencies():
    resp = make_response(redirect('/account'))
    currency = request.form['currency']
    if currency == 'Select currency':
        currency = 'CZK'
    resp.set_cookie('currency', currency)
    return resp


def generate_and_store_key(user):
    secret_key = os.urandom(8).hex()
    secret_key = '1'
    users[user].key = secret_key
    return secret_key


def send_mail(user, secretkey):
    msg = MIMEText('ur key %s' % secretkey)
    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = 'Auth Key'
    msg['From'] = sender
    msg['To'] = users[user].email

    s = smtplib.SMTP('smtp-mail.outlook.com', 587)
    s.ehlo()
    s.starttls()
    s.login("stintest@outlook.com", "Burnerpassword")
    s.sendmail(sender, [users[user].email], msg.as_string())
    s.quit()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)