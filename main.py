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
        p1 = Player(playerName, "X", False)
        playerName = input("Choose a name for player 2\n")
        p2 = Player(playerName, "O", False)
        board = Board()
        currentPlayer = 1
        player1canMove = True
        player2canMove = True

        while not endGame:
            current_player_obj = p1 if currentPlayer == 1 else p2
            board.clear_board()
            dictAvailableMove = board.find_a_correct_move(current_player_obj)

            if not dictAvailableMove:
                print(f"No move available for {current_player_obj.name}!")
                if currentPlayer == 1:
                    player1canMove = False
                    currentPlayer = 2  # We will check if the other player can play
                else:
                    player2canMove = False
                    currentPlayer = 1  # We will check if the other player can play
            else:
                while True:
                    try:
                        board.print_board()
                        move = int(input(f"{current_player_obj.name}, choose your move!\n"))
                        if move in dictAvailableMove:
                            break
                        else:
                            print("Wrong choice, please chose a valid move !!\n")
                    except ValueError:
                        print("Please enter a number.\n")

                board.playMove(dictAvailableMove.get(move), current_player_obj)
                board.getScore(p1)
                board.getScore(p2)
                print(f"Actual score {p1.name} : {p1.score}, {p2.name} : {p2.score}")

                # Switch player
                currentPlayer = 1 if currentPlayer == 2 else 2

            if not player1canMove and not player2canMove:
                board.print_board()
                print("--------Game over-------")
                if p1.score > p2.score:
                    print(f"{p1.name} won! Congrats!")
                elif p2.score > p1.score:
                    print(f"{p2.name} won! Congrats!")
                else:
                    print("It's sadly a tie.")
                endGame = True


if __name__ == '__main__':
    newGame()
