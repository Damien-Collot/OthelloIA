from player import Player
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
                while 0 <= x < len(self.board) and 0 <= y < len(self.board[line]) and self.board[x][
                    y] == opponent_token:
                    tiles_to_flip.append((x, y))
                    x += dx
                    y += dy
                if tiles_to_flip and 0 <= x < len(self.board) and 0 <= y < len(self.board[line]) and self.board[x][
                    y] == ".":
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
        self.clear_board()
        self.reverse_pawn(move, player.token)
        return True

    def play_ai(self, ai):
        value = -4
        listValues = self.min_max_maison(ai, 3, False)
        move = ()
        for weight, position in listValues:
            if weight > value:
                move = position
        if not move:
            return False
        else:
            x, y = move
            self.board[x][y] = ai.token
            self.clear_board()
            self.reverse_pawn([x, y], ai.token)
            return True

    def get_copy(self):
        return copy.deepcopy(self)

    def is_terminal(self):
        player_moves = self.find_a_correct_move(Player("Temp", "X"))
        opponent_moves = self.find_a_correct_move(Player("Temp", "O"))

        if not player_moves and not opponent_moves:
            x_tokens = sum(1 for row in self.board for cell in row if cell == "X")
            o_tokens = sum(1 for row in self.board for cell in row if cell == "O")

            if x_tokens > o_tokens:
                return "X"
            elif o_tokens > x_tokens:
                return "O"
            else:
                return "DRAW"
        return False

    def positional_evaluation(self, player):
        game_result = self.is_terminal()
        if game_result:
            if game_result == player.token:
                return 1000
            elif game_result == "DRAW":
                return 0
            else:
                return -1000

        score = 0
        for x in range(8):
            for y in range(8):
                if self.board[x][y] == player.token:
                    score += WEIGHTS[x][y]
                elif self.board[x][y] == "O" if player.token == "X" else "X":
                    score -= WEIGHTS[x][y]
        return score

    def mobility_evalutation(self, ai_token):
        # Maximise le nombre de coups possible
        ai_moves = len(self.find_a_correct_move(Player("Temp", ai_token)))
        opponent_token = "X" if ai_token == "O" else "O"
        opponent_moves = len(self.find_a_correct_move(Player("Temp", opponent_token)))

        # Favoriser les coins.
        corner_bonus = 0
        for x, y in [(0, 0), (0, 7), (7, 0), (7, 7)]:
            if self.board[x][y] == ai_token:
                corner_bonus += 5
            elif self.board[x][y] == opponent_token:
                corner_bonus -= 5

        return (ai_moves - opponent_moves) + corner_bonus

    def positionnal_play(self, player):
        weight = -4
        move = ()
        dict = self.find_a_correct_move(player)
        if not dict:
            return move
        else:
            for key in dict:
                x, y = dict.get(key)
                if WEIGHTS[x][y] > weight:
                    weight = WEIGHTS[x][y]
                    move = dict.get(key)
            return move

    def absolute_play(self, player):
        score = player.score
        move = ()
        dict = self.find_a_correct_move(player)
        if not dict:
            return move
        else:
            for key in dict:
                self.clear_board()
                b = self.get_copy()
                b.playMove(dict.get(key), player)
                b.getScore(player)
                if player.score > score:
                    score = player.score
                    move = dict.get(key)
            return move

    def min_value(self, depth, max_depth, player):
        if depth == max_depth or self.is_terminal():
            return self.positional_evaluation(player), None

        v = float('inf')
        best_move = None
        for move in self.find_a_correct_move(player):
            copied_board = self.get_copy()
            copied_board.playMove(move, player)
            value, _ = copied_board.max_value(depth + 1, max_depth, player)
            if value < v:
                v = value
                best_move = move
        return v, best_move

    def max_value(self, depth, max_depth, player):
        if depth == max_depth or self.is_terminal():
            return self.positional_evaluation(player), None

        v = float('-inf')
        best_move = None
        for move in self.find_a_correct_move(player):
            copied_board = self.get_copy()
            copied_board.playMove(move, player)
            value, _ = copied_board.min_value(depth + 1, max_depth, player)
            if value > v:
                v = value
                best_move = move
        return v, best_move

    def opponent(self, player):
        opponent = Player("Opponent", "O" if player.token == "X" else "X")
        return opponent if player.token == "O" else player

    def min_max_maison(self, player, depth, isMax, position=()):
        value = None
        if depth == 0:
            return WEIGHTS[position[0]][position[1]], position

        for move, position in self.find_a_correct_move(player).items():
            self.clear_board()
            copied_board = self.get_copy()
            copied_board.playMove(position, player)
            temp = self.min_max_maison(self.opponent(player), depth - 1, not isMax, position)
            # manque le lien avec weight et le return de la fonction
            # il faut return la valeur au lieu de la mettre dans une liste
            # avant de la return il faut verifier le max et le min
            print(temp)
            if isMax:
                # si la temp est plus grand que la value actuelle alors value = temp
                print(temp)
            else:
                # si la temp est plus petite que la value actuelle alors value = temp
                print(temp)
        return value
