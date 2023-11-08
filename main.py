import time

from board import Board
from player import Player
import random


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
        n = 0
        winAi = 0
        winRand = 0
        tie = 0
        while n < 100:
            res = IA_sim()
            print(res)
            if res == 1:
                winAi += 1
            elif res == 2:
                winRand += 1
            else:
                tie +=1
            n += 1
        print(f"Fin de la simu Win ia : {winAi} win rand : {winRand} egalité : {tie}")

def IA_sim():
    endGame = False
    nbCoup = 0
    ai1 = Player("Computer 1", "X")
    ai2 = Player("Computer 2", "O")
    board = Board()
    currentPlayer = 2
    ai11canMove = True
    ai2canMove = True
    while not endGame:
        board.clear_board()
        if currentPlayer == 1:
            ai11canMove = board.make_best_move(ai1, nbCoup)
        else:
            # ai2canMove = board.make_best_move(ai1, nbCoup)
            bite = board.find_a_correct_move(ai2)
            if not bite:
                ai2canMove = False
            else:
                rand = random.randint(0, len(bite) - 1)

                move_index = random.choice(list(bite.keys()))
                board.playMove(bite[move_index], ai2)

                # board.playMove(bite[rand], ai2)
                ai2canMove = True
        board.getScore(ai1)
        board.getScore(ai2)

        # Switch player
        currentPlayer = 1 if currentPlayer == 2 else 2
        nbCoup += 1
        if not ai11canMove and not ai2canMove:
            if ai1.score > ai2.score:
                return 1
            elif ai2.score > ai1.score:
                return 2
            else:
                return 3
            endGame = True


if __name__ == '__main__':
    newGame()
