from player import Player
import copy

WEIGHTS = [
    [500, -150, 30, 10, 10, 30, -150, 500],
    [-150, -250, 0, 0, 0, 0, -250, -150],
    [30, 0, 1, 2, 2, 1, 0, 30],
    [10, 0, 2, 16, 16, 2, 0, 10],
    [10, 0, 2, 16, 16, 2, 0, 10],
    [30, 0, 1, 2, 2, 1, 0, 30],
    [-150, -250, 0, 0, 0, 0, -250, -150],
    [500, -150, 30, 10, 10, 30, -150, 500],
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
        listValues = self.min_max_maison(self.get_copy(), ai, 0, True)
        if listValues is None:
            return False
        else:
            move = listValues[1]
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

    def mobility_evalutation(self, board, ai):
        # Maximise le nombre de coups possible
        ai_moves = len(board.find_a_correct_move(Player("Temp", ai)))
        board.clear_board()
        opponent_token = "X" if ai.token == "O" else "O"
        opponent_moves = len(board.find_a_correct_move(Player("Temp", self.opponent(ai))))
        board.clear_board()

        # Favoriser les coins.
        corner_bonus = 0
        for x, y in [(0, 0), (0, 7), (7, 0), (7, 7)]:
            if board.board[x][y] == ai.token:
                corner_bonus += 5
            elif board.board[x][y] == opponent_token:
                corner_bonus -= 5

        return (ai_moves - opponent_moves) + corner_bonus

    def positionnal_play(self, board, player):
        score = 0
        opponent = 'O' if player.token == 'X' else 'X'

        for i in range(8):
            for j in range(8):
                if board.board[i][j] == player.token:
                    score += WEIGHTS[i][j]
                elif board.board[i][j] == opponent:
                    score -= WEIGHTS[i][j]
        return score

    def absolute_play(self,board, player):
        board.getScore(player)
        score = player.score
        return score

    def opponent(self, player):
        if player.token == 'X':
            return Player("Opponent", "O")
        else:
            return Player("Opponent", "X")


    def minimax(self, board, depth, maximizing_player, player, nbCoup):
        if depth == 0:
            if nbCoup < 20:
                return self.positionnal_play(board, player)
            elif nbCoup < 50:
                return self.mobility_evalutation(board, player)
            else:
                return self.absolute_play(board, player)

        max_eval = float('-inf')
        min_eval = float('inf')
        legal_moves = board.find_a_correct_move(player)
        board.clear_board()

        for position in legal_moves.values():
            if maximizing_player:
                new_board = board.get_copy()
                new_board.playMove(position, player)
                eval = self.minimax(new_board, depth - 1, False, self.opponent(player), nbCoup+1)
                max_eval = max(max_eval, eval)
            else:
                new_board = board.get_copy()
                new_board.playMove(position, player)
                eval = self.minimax(new_board, depth - 1, True, self.opponent(player), nbCoup+1)
                min_eval = min(min_eval, eval)
        return max_eval

    def new_min_max(self, player, depth, isMax, alpha=float('-inf'), beta=float('inf'), nbCoup=0):
        if depth == 0:
            if nbCoup < 20:
                return self.positionnal_play(self, player)
            elif nbCoup < 50:
                return self.mobility_evalutation(self, player)
            else:
                return self.absolute_play(self, player)

        if isMax:
            maxEval = float('-inf')
            for move in self.find_a_correct_move(player).values():
                new_board = self.get_copy()
                new_board.playMove(move, player)
                eval = new_board.new_min_max(self.opponent(player), depth - 1, False, alpha, beta, nbCoup+1)
                if eval > maxEval:
                    maxEval = eval
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = float('inf')
            for move in self.find_a_correct_move(player).values():
                new_board = self.get_copy()
                new_board.playMove(move, player)
                eval = new_board.new_min_max(self.opponent(player), depth - 1, True, alpha, beta, nbCoup+1)
                if eval < minEval:
                    minEval = eval
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval


    def make_best_move(self, player, nbCoup):
        best_move = float('-inf')
        best_pos = ()
        board = self.get_copy()
        legal_moves = board.find_a_correct_move(player)
        board.clear_board()

        for position in legal_moves.values():
            move = self.new_min_max(player, 3, True, float('-inf'), float('inf'), nbCoup)
            if move > best_move:
                best_move = move
                best_pos = position

        if best_move is float('-inf') or best_pos == ():
            return False
        else:
            self.playMove(best_pos, player)
            return True
