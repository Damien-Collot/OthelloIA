from board import Board
from player import Player
from token import Token
x = Board()
x.find_a_correct_move(Player('aa', Token(Token.WHITE), False))
x.print_board()

'''
x = Board()
x.board[1][6] = Token(Token.WHITE)
x.board[2][5] = Token(Token.WHITE)
x.print_board()
x.playMove((0,7), Player('aa', Token(Token.BLACK), False))
x.print_board()
'''