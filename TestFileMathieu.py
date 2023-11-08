import time

from board import Board
from player import Player


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
    elif choice == 2:
        playerName = input("Choose a name for player 1 \n")
        p1 = Player(playerName, "X")
        ai = Player("Computer", "O")
        board = Board()
        currentPlayer = 1
        player1canMove = True
        aicanMove = True
        while not endGame:
            current_player_obj = p1 if currentPlayer == 1 else ai
            board.clear_board()
            if current_player_obj == p1:
                dictAvailableMove = board.find_a_correct_move(current_player_obj)
                if not dictAvailableMove:
                    player1canMove = False
                    currentPlayer = 2
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
            else:
                aicanMove = board.play_ai(ai)
            board.print_board()
            board.getScore(p1)
            board.getScore(ai)
            print(f"Actual score {p1.name} : {p1.score}, {ai.name} : {ai.score}")
            time.sleep(2)

            # Switch player
            currentPlayer = 1 if currentPlayer == 2 else 2
            if not player1canMove and not aicanMove:
                board.print_board()
                print("--------Game over-------")
                if p1.score > ai.score:
                    print(f"{p1.name} won! Congrats!")
                elif ai.score > p1.score:
                    print(f"{ai.name} won! Congrats!")
                else:
                    print("It's sadly a tie.")
                endGame = True
    else:
        ai1 = Player("Computer 1", "X")
        ai2 = Player("Computer 2", "O")
        board = Board()
        currentPlayer = 1
        ai11canMove = True
        ai2canMove = True
        while not endGame:
            current_player_obj = ai1 if currentPlayer == 1 else ai2
            board.clear_board()
            if current_player_obj == ai1:
                ai11canMove = board.play_ai(ai1)
            else:
                ai2canMove = board.play_ai(ai2)
            board.getScore(ai1)
            board.getScore(ai2)
            print(f"Actual score {ai1.name} : {ai1.score}, {ai2.name} : {ai2.score}")

            # Switch player
            currentPlayer = 1 if currentPlayer == 2 else 2
            if not ai11canMove and not ai2canMove:
                board.print_board()
                print("--------Game over-------")
                if ai1.score > ai1.score:
                    print(f"{ai1.name} won! Congrats!")
                elif ai2.score > ai2.score:
                    print(f"{ai2.name} won! Congrats!")
                else:
                    print("It's sadly a tie.")
                endGame = True


if __name__ == '__main__':
    newGame()
