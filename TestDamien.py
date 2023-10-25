from board import Board
from player import Player

x = Board()
p = Player('test', 'X')
move = x.positionnal_play(p)
print(move)
x.print_board()
x.clear_board()
x.reverse_pawn(move, p.token)
x.print_board()