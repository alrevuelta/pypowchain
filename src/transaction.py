import jsonpickle


class Transaction:
    def __init__(self, sender, to, amount):
        self.sender = sender
        self.to = to
        self.amount = amount

    def __str__(self):
        return jsonpickle.encode(self)

    def __repr__(self):
        return str(self)