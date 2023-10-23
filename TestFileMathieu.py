from boardMathieu import BoardMathieu
from player import Player
from token import Token


def newGame():

    playerName = input("Choose a name for player 1 \n")
    p1 = Player(playerName, Token(Token.WHITE), False)
    playerName = input("Choose a name for player 2\n")
    p2 = Player(playerName, Token(Token.BLACK), False)
    boardMathieu = BoardMathieu()
    isPlayer1ToPlay = True
    player1canMove = True
    player2canMove = True
    currentPlayer = 1
    endGame = False
    while not endGame:
        if currentPlayer == 1:
            dictAvailableMove = boardMathieu.find_a_correct_move(p1)
            if dictAvailableMove == {}:
                print("No move available for Player 1!")
                player1canMove = False
                currentPlayer = 2
            else:
                boardMathieu.print_board()
                player1canMove = True
                move = int(input("Choose your move, Player 1!\n"))
                while move not in dictAvailableMove:
                    move = int(input("Wrong choice, please chose a valid move !!\n"))
                boardMathieu.playMove(dictAvailableMove.get(move), p1)
                currentPlayer = 2
        else:
            boardMathieu.min_max(p2, 3)
            print(boardMathieu.win_move)
            currentPlayer = 1

       # print(f"Actual score {p1.name} : {p1.score}, {p2.name} : {p2.score}")
        if not player1canMove and not player2canMove:
            print("--------Game over-------")
            print("Player 1 won congrats !!") if p1.score > p2.score else print(
                "Player 2 won congrats !!") if p2.score > p1.score else print("It's sadly a tie")
            endGame = True


if __name__ == '__main__':
    newGame()
