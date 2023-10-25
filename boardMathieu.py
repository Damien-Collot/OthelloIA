from token import Token
import copy

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

class Board:

    def __init__(self):
        self.board = [
            ["." for _ in range(8)] for _ in range(8)
        ]
        self.board[3][3] = "X"
        self.board[3][4] = "O"
        self.board[4][3] = "O"
        self.board[4][4] = "X"
        self.possible_move = {}

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
                if player.token == element:
                    posPion.append((line, column))

        possible_moves = {}
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        opponent_token = "X" if player.token == "O" else "O"
        key_move = 1

        for pion in posPion:
            line, column = pion
            for dx, dy in directions:
                x, y = line + dx, column + dy
                tiles_to_flip = []
                while 0 <= x < len(self.board) and 0 <= y < len(self.board[line]) and self.board[x][y] == opponent_token:
                    tiles_to_flip.append((x, y))
                    x += dx
                    y += dy
                if tiles_to_flip and 0 <= x < len(self.board) and 0 <= y < len(self.board[line]) and self.board[x][y] == ".":
                    if (x, y) not in possible_moves.values():
                        possible_moves[key_move] = (x, y)
                        key_move += 1

        for key, value in possible_moves.items():
            self.board[value[0]][value[1]] = key

        return possible_moves

    def reverse_pawn(self, pos, token):
        opponent_token = "X" if token == "O" else "O"
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for dx, dy in directions:
            x, y = pos
            x += dx
            y += dy
            tiles_to_flip = []

            while 0 <= x < 8 and 0 <= y < 8:
                cell = self.board[x][y]
                if cell == opponent_token:
                    tiles_to_flip.append((x, y))
                    x += dx
                    y += dy
                else:
                    break
            if not tiles_to_flip:
                continue

            if tiles_to_flip and 0 <= x < 8 and 0 <= y < 8:
                cell = self.board[x][y]
                if cell == token:
                    for flip_x, flip_y in tiles_to_flip:
                        self.board[flip_x][flip_y] = token

    def getScore(self, player):
        score = 0
        for line in range(0, len(self.board)):
            for column in range(0, len(self.board)):
                element = self.board[line][column]
                if player.token == element:
                    score += 1
        player.score = score

    def clear_board(self):
        for x in range(0, 8):
            for y in range(0, 8):
                if isinstance(self.board[x][y], int):
                    self.board[x][y] = "."

    def playMove(self, move, player):
        x, y = move
        self.board[x][y] = player.token
        self.reverse_pawn(move, player.token)
        return True

    def get_copy(self):
        return copy.deepcopy(self)

    def is_terminal(self):
        return not self.find_a_correct_move(Token.WHITE) and not self.find_a_correct_move(Token.BLACK)

    def positional_evaluation(self):
        score = 0
        for x in range(8):
            for y in range(8):
                if self.board[x][y] == "X":
                    score += WEIGHTS[x][y]
                elif self.board[x][y] == "O":
                    score -= WEIGHTS[x][y]
        return score

    def min_value(self, depth, max_depth):

        return

    def max_value(self, depth, max_depth):

        return

    def min_max(self, isMax,player, depth):

        possible_moves = self.find_a_correct_move(player)
        tree = []
        # Parcourir chaque mouvement possible
        for move in possible_moves.values():  # move est un tuple (x, y)
            x, y = move
            newBranch = []

            #current_value = WEIGHTS[x][y]
            # max
            if isMax:
                if depth >= 0:
                    isMax = not isMax
                    depth -= depth
                    result = self.min_max(isMax,player,depth)
#traitement du max
            # min
            else:
                if depth >= 0:
                    depth -= depth
                    isMax = not isMax
                    #traitement du minee.append(newBranch)

        return False
