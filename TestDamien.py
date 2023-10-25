from board import Board
from player import Player

x = Board()
p = Player('test', 'X')
x.print_board()
move = x.absolute_play(p)
print(move)
x.clear_board()
v, y = move
x.board[v][y] = p.token
x.reverse_pawn(move, p.token)
x.print_board()