from Server.User import User


def test_user_creation():
    email = "jaroslav@gmail.com"
    name = "Jaroslav"
    surname = "Belina"
    password = "123456"
    user = User(email, name, surname, password)

    assert user.key is None
