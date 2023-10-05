class Token:
    EMPTY = 0
    WHITE = 1
    BLACK = 2

    SYMBOLS = {
        EMPTY: ".",
        WHITE: "O",
        BLACK: "X"
    }

    def __init__(self, type):
        self.type = type

    def __str__(self):
        return Token.SYMBOLS[self.type]
