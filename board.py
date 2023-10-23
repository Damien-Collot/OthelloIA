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
        posPion = []
        for line in range(len(self.board)):
            for column in range(len(self.board)):
                element = self.board[line][column]
                if player.token.type == element.type:
                    posPion.append((line, column))

        possible_moves = {}
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
       # print(posPion)
        move_number = 1  # Initialisation du chiffre pour le premier coup possible

        for pion in posPion:
            line, column = pion
            for dx, dy in directions:
                x, y = line + dx, column + dy
                while 0 <= x < len(self.board) and 0 <= y < len(self.board[line]):
                    adjacent_position = self.board[x][y]

                    if adjacent_position.type == Token.EMPTY:
                        # Vérifiez si les coordonnées ne sont pas déjà présentes dans la liste des coups possibles
                        if (x, y) not in possible_moves.values():
                            # Ajoutez le coup possible au dictionnaire avec le numéro de mouvement
                            possible_moves[move_number] = (x, y)
                            move_number += 1
                        break
                    elif adjacent_position.type == player.token.type:
                        break
                    x += dx
                    y += dy

        #print(possible_moves)
        for key, value in possible_moves.items():
            self.board[value[0]][value[1]] = key;

        return possible_moves

    def find_a_correct_move(self, player):
        posPion = []
        for line in range(len(self.board)):
            for column in range(len(self.board)):
                element = self.board[line][column]
                if player.token.type == element.type:
                    posPion.append((line, column))

        possible_moves = {}
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        opponent_token = Token.WHITE if player.token.type == Token.BLACK else Token.BLACK
        key_move = 1

        for pion in posPion:
            line, column = pion
            for dx, dy in directions:
                x, y = line + dx, column + dy
                tiles_to_flip = []
                while 0 <= x < len(self.board) and 0 <= y < len(self.board[line]) and self.board[x][
                    y].type == opponent_token:
                    tiles_to_flip.append((x, y))
                    x += dx
                    y += dy
                if tiles_to_flip and 0 <= x < len(self.board) and 0 <= y < len(self.board[line]) and self.board[x][
                    y].type == Token.EMPTY:
                    if (x, y) not in possible_moves.values():
                        possible_moves[key_move] = (x, y)
                        key_move += 1

        for key, value in possible_moves.items():
            self.board[value[0]][value[1]] = key

        print(f"Moves found for {player.token.type}: {possible_moves}")
        return possible_moves

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

    def clear_board(self):
        for x in range(0, 8):
            for y in range(0, 8):
                if isinstance(self.board[x][y], int):
                    self.board[x][y] = Token(Token.EMPTY)

    def playMove(self, move, player):
        print(f"{player.token.type} is playing move: {move}")
        x, y = move
        self.board[x][y] = player.token
        self.reverse_pawn(move, player.token.type)
        self.getScore(player)
        return True

    def get_copy(self):
        return copy.deepcopy(self)

    def is_terminal(self):
        return not self.find_a_correct_move(Token.WHITE) and not self.find_a_correct_move(Token.BLACK)

    def positional_evaluation(self):
        score = 0
        for x in range(8):
            for y in range(8):
                if self.board[x][y].type == Token.WHITE:
                    score += WEIGHTS[x][y]
                elif self.board[x][y].type == Token.BLACK:
                    score -= WEIGHTS[x][y]
        return score

    def min_value(self, depth, max_depth):
        if depth == max_depth or self.is_terminal():
            return self.positional_evaluation()

        v = float('inf')
        for move in self.find_a_correct_move(Token.BLACK):
            copied_board = self.get_copy()
            copied_board.playMove(move, Token.BLACK)
            v = min(v, copied_board.max_value(depth + 1, max_depth))

        return v

    def max_value(self, depth, max_depth):
        if depth == max_depth or self.is_terminal():
            return self.positional_evaluation()

        v = float('-inf')
        for move in self.find_a_correct_move(Token.WHITE):
            copied_board = self.get_copy()
            copied_board.playMove(move, Token.WHITE)
            v = max(v, copied_board.min_value(depth + 1, max_depth))

        return v

    def min_max(self, player, depth):
        possible_moves = self.find_a_correct_move(player)

        # Initialiser la meilleure valeur à un minimum
        best_value = float('-inf')

        # Parcourir chaque mouvement possible
        for move in possible_moves.values():  # move est un tuple (x, y)
            x, y = move
            current_value = WEIGHTS[x][y]

            # Mise à jour de la meilleure valeur
            if current_value > best_value:
                best_value = current_value

        # Stocker la meilleure valeur dans win_move (je l'ai transformé en variable pour simplifier)
        win_move = best_value
        print("Min_max best value " + best_value.__str__())

        return win_move
