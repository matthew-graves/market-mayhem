class User:
    def __init__(self, username, balance, lasttradetime):
        self.username = username
        self.balance = balance
        self.lasttradetime = lasttradetime

    def get_balance(self):
        return self.balance


def create_user(username):
    return User(username, 100000, 0)


