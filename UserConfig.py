from User import User
import os
import pickle

def load_users():
    if os.path.isfile('data.p'):
        users = pickle.load(open("save.p", "rb"))
    else:
        users = define_users()
        pickle.dump(users, open("save.p", "wb"))
    return users


def define_users():
    # User 1
    email = "jaroslavbelina.ml@seznam.cz"
    users = {email: User(email, "Jaroslav", "Bělina", "123456789")}
    user_acc = users[email].account
    user_acc['CZK'] = 500
    user_acc['CZK'] += 500
    user_acc['CZK'] -= 500
    user_acc['CZK'] += 1000
    user_acc['EUR'] = 500
    user_acc['EUR'] -= 100

    # User 2
    email = "jaroslav.belina@tul.cz"
    users |= {email: User(email, "Jaroslav", "Bělina", "987654321")}
    user_acc = users[email].account
    user_acc['CZK'] = 500
    user_acc['CZK'] += 500
    user_acc['CZK'] -= 500
    user_acc['CZK'] += 1000
    user_acc['JPY'] = 500000
    user_acc['JPY'] -= 100000

    return users
