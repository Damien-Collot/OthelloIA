from token import Token

class Player:
    def __init__(self, name, token, ai):
        self.name = name
        self.token = token
        self.ai = ai
        self.score = 0
