from collections import defaultdict
from datetime import datetime


class User:
    def __init__(self, email, name, surname, password):
        self.email = email
        self.account = MemoryDict()
        self.name = name
        self.surname = surname
        self.password = password
        self.key = None


class MemoryDict(dict):
    def __init__(self):
        self.memory = []

    def __setitem__(self, key, value):
        self.memory.append((key, datetime.now(), value - self.get(key, 0)))
        super().__setitem__(key, value)

    def get_transactions(self, key):
        return [i for i in self.memory if i[0] == key]
