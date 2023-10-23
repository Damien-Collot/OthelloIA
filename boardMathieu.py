from token import Token
import copy
from copy import deepcopy
from player import Player

WEIGHTS = [
    [5, -2, 4, 2, 2, 4, -2, 5],
    [-2, -3, -1, 0, 0, -1, -3, -2],
    [4, -1, 1, 0, 0, 1, -1, 4],
    [2, 0, 0, 1, 1, 0, 0, 2],
    [2, 0, 0, 1, 1, 0, 0, 2],
    [4, -1, 1, 0, 0, 1, -1, 4],
    [-2, -3, -1, 0, 0, -1, -3, -2],
    [5, -2, 4, 2, 2, 4, -2, 5]
]


class BoardMathieu:

    def __init__(self):
        self.board = [
            [Token(Token.EMPTY) for _ in range(8)] for _ in range(8)
        ]
        self.board[3][3] = Token(Token.WHITE)
        self.board[3][4] = Token(Token.BLACK)
        self.board[4][3] = Token(Token.BLACK)
        self.board[4][4] = Token(Token.WHITE)
        self.possible_move = {}
        #self.win_move = []

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

    def find_a_correct_move(self, player):
        posPion = []
        for line in range(len(self.board)):
            for column in range(len(self.board)):
                element = self.board[line][column]
                if isinstance(element, Token) and player.token.type == element.type:
                    posPion.append((line, column))

        # Réinitialisation du plateau
        self.clear_board()

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
                        # Ajoutez le coup possible au dictionnaire avec le numéro de mouvement
                        possible_moves[key_move] = (x, y)
                        key_move += 1

        for key, value in possible_moves.items():
            self.board[value[0]][value[1]] = key

        #print(f"Moves found for {player.token.type}: {possible_moves}")
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
            if tiles_to_flip and 0 <= x < 8 and 0 <= y < 8 and self.board[x][y].type == token:
                for flip_x, flip_y in tiles_to_flip:
                    self.board[flip_x][flip_y].type = token

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

        if move not in [m for m in self.find_a_correct_move(player).values()]:
            return False
        x, y = move
        self.board[x][y] = player.token
        self.clear_board()
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

    WEIGHTS = [
        # ... (votre grille de poids)
    ]

    def min_max(self, p, depth):
        possible_moves = self.find_a_correct_move(p)

        # Initialiser la meilleure valeur à un minimum pour le joueur
        best_value = float('-inf') if p.token.type == Token.WHITE else float('inf')  # Supposition que WHITE veut maximiser et BLACK veut minimiser
        #player.token.type == element.type
        # Pour stocker les valeurs des mouvements pour cette profondeur
        values_for_depth = []

        # Parcourir chaque mouvement possible
        for move in possible_moves.values():
            x, y = move
            current_value = WEIGHTS[x][y]

            # Simulez le mouvement sur un nouveau tableau
            new_board = deepcopy(self)
            new_board.playMove(move, p)

            # Si nous ne sommes pas à la profondeur finale, faites un appel récursif
            if depth > 0:
                # Changer de joueur pour le prochain niveau de récursivité
                opponent = Player("Opponent", Token(Token.BLACK if p.token.type == Token.WHITE else Token.WHITE), False)

                # Récursivité
                current_value += new_board.min_max(opponent, depth - 1)[0]

            values_for_depth.append(current_value)

            # Mise à jour de la meilleure valeur
            if p.color == Token.WHITE:
                best_value = max(best_value, current_value)
            else:
                best_value = min(best_value, current_value)

        # Ajoutez la meilleure valeur de cette profondeur à win_moves
        win_moves = [best_value] + values_for_depth

        return win_moves