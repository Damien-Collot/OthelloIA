from board import Board
from player import Player
from token import Token
x = Board()
x.find_a_correct_move(Player('aa', Token(Token.WHITE), False))
x.print_board()