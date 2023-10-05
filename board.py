from token import Token



class Board:
    def __init__(self):
        self.board = [
            [Token(Token.EMPTY) for _ in range(8)] for _ in range(8)
        ]
        self.board[3][3] = Token(Token.WHITE)
        self.board[3][4] = Token(Token.BLACK)
        self.board[4][3] = Token(Token.BLACK)
        self.board[4][4] = Token(Token.WHITE)



    def print_board(self):
        # Afficher les numéros de colonne
        print("     1  2  3  4  5  6  7  8")
        print("  +--------------------------+")

        # Parcourir chaque ligne du plateau
        for i, row in enumerate(self.board, 1):
            row_str = [str(i)]  # Numéro de ligne
            row_str.append("| ")

            # Parcourir chaque case de la ligne
            for cell in row:
                row_str.append(str(cell) + " ")

            row_str.append("|")
            print(" ".join(row_str))

        print("  +--------------------------+")


    def find_correct_move(self, player):
        #result = {"1": (1,2)}
        posPion = []
        # répérer les bons pions à jouer
        for line in range(0, len(self.board)):
            for column in range(0, len(self.board)):
                element = self.board[line][column]
                if player.token.type == element.type:
                    posPion.append((line, column))

        print(posPion)
        #vérification du coup jouer
       # for element in posPion:




        #modifier la grille


    def reverse_pawn(self, pos, token):
        opponent_token = Token.WHITE if token == Token.BLACK else Token.BLACK
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dx, dy in directions:
            x, y = pos
            x += dx
            y += dy
            tiles_to_flip = []
            while 0 <= x < 8 and 0 <= y < 8 and self.board[x][y].type == opponent_token:
                tiles_to_flip.append((x, y))
                x += dx
                y += dy
            if 0 <= x < 8 and 0 <= y < 8 and self.board[x][y].type == token:
                for x, y in tiles_to_flip:
                    self.board[x][y].type = token

    def getScore(self, player):
        score = 0
        for line in range(0, len(self.board)):
            for column in range(0, len(self.board)):
                element = self.board[line][column]
                if player.token.type == element.type:
                    score += 1
        player.score = score

    def playMove(self, move, player):
        x, y = move
        self.board[x][y] = player.token
        self.reverse_pawn(move, player.token.type)
        self.getScore(player)
