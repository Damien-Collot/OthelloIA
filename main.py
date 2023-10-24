from board import Board
from player import Player
from token import Token


def newGame():
    while True:
        try:
            choice = int(input("Chose your mode  : 1v1 (1), 1vAI (2), AIvAI(3)\n"))
            if choice in [1, 2, 3]:
                break
            else:
                print("Invalid choice. Please choose 1, 2, or 3.")
        except ValueError:
            print("Please enter a number.")

    endGame = False
    if choice == 1:
        playerName = input("Choose a name for player 1 \n")
        p1 = Player(playerName, Token(Token.WHITE), False)
        playerName = input("Choose a name for player 2\n")
        p2 = Player(playerName, Token(Token.BLACK), False)
        board = Board()
        currentPlayer = p1
        noMovesForCurrentPlayer = False

        while not endGame:
            board.clear_board()
            dictAvailableMove = board.find_a_correct_move(currentPlayer)

            if not dictAvailableMove:
                if noMovesForCurrentPlayer:  # Si le joueur précédent n'avait pas de mouvements, terminez le jeu.
                    print("--------Game over-------")
                    if p1.score > p2.score:
                        print(f"{p1.name} won! Congrats!")
                    elif p2.score > p1.score:
                        print(f"{p2.name} won! Congrats!")
                    else:
                        print("It's sadly a tie.")
                    endGame = True
                    break
                else:  # Passez au joueur suivant et marquez que le joueur actuel n'a pas de mouvements.
                    noMovesForCurrentPlayer = True
                    currentPlayer = p2 if currentPlayer == p1 else p1
                    continue
            else:
                noMovesForCurrentPlayer = False  # Réinitialisez le marqueur, car le joueur actuel a des mouvements disponibles.

            board.print_board()
            move = int(input(f"{currentPlayer.name}, choose your move!\n"))
            while move not in dictAvailableMove:
                move = int(input("Wrong choice, please chose a valid move !!\n"))

            board.playMove(dictAvailableMove.get(move), currentPlayer)

            print(f"Actual score {p1.name} : {p1.score}, {p2.name} : {p2.score}")

            # Switch player
            currentPlayer = p2 if currentPlayer == p1 else p1


if __name__ == '__main__':
    newGame()
