from board import Board
from token import Token
from player import Player

x = Board()
x.board[1][6] = Token(Token.WHITE)
x.board[2][5] = Token(Token.WHITE)
x.print_board()
x.playMove((0,7), Player('aa', Token(Token.BLACK), False))
x.print_board()