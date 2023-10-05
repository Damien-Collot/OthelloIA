from board import Board
from player import Player
from token import Token


def newGame():
    choice = int(input("Chose your mode  : 1v1 (1), 1vAI (2), AIvAI(3)\n"))
    endGame = False
    if choice == 1:
        playerName = input("Choose a name for player 1 \n")
        p1 = Player(playerName, Token(Token.BLACK), False)
        playerName = input("Choose a name for player 2\n")
        p2 = Player(playerName, Token(Token.WHITE), False)
        board = Board()
        currentPlayer = 1
        player1canMove = True
        player2canMove = True
        while not endGame:
            dictAvailableMove = board.find_correct_move(p1 if currentPlayer == 1 else p2)
            if dictAvailableMove == {}:
                if currentPlayer == 1:
                    player1canMove = False
                else:
                    player2canMove = False
            board.print_board()
            move = int(input("Choose your move !"))
            while move not in dictAvailableMove:
                move = int(input("Wrong choice, please chose a valid move !!"))
            board.playMove(dictAvailableMove.get(move), p1 if currentPlayer == 1 else p2)
            print(f"Actual score {p1.name} : {p1.score}, {p2.name} : {p2.score}")
            currentPlayer = 2 if currentPlayer == 1 else 2
            if not player1canMove and not player2canMove:
                print("--------Game over-------")
                print("Player 1 won congrats !!") if p1.score > p2.score else print(
                    "Player 2 won congrats !!") if p2.score > p1.score else print("It's sadly a tie")
                endGame = True


if __name__ == '__main__':
    newGame()
