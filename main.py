import time

from board import Board
from player import Player
import random


def newGame():
    # Boucle pour sélectionner le mode de jeu
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
    # Mode 1v1: Deux joueurs humains
    if choice == 1:
        # Initialisation des joueurs
        playerName = input("Choose a name for player 1 \n")
        p1 = Player(playerName, "X")
        playerName = input("Choose a name for player 2\n")
        p2 = Player(playerName, "O")
        board = Board()
        currentPlayer = 1
        player1canMove = True
        player2canMove = True
        # Boucle principale de jeu
        while not endGame:
            # Logique de jeu pour 1v1
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
    # Mode 1vAI: Joueur humain contre IA
    elif choice == 2:
        # Initialisation du joueur humain et de l'IA
        # Logique de jeu pour 1vAI
        playerName = input("Choose a name for player 1 \n")
        p1 = Player(playerName, "X")
        choice_ai = int(input("Choose algorithm for AI 1 : 1(positional) 2(mobility) 3(absolute) 4(mixte)\n"))
        name_ai = ''
        match choice_ai:
            case 1:
                name_ai = 'positional'
            case 2:
                name_ai = 'move'
            case 3:
                name_ai = 'absolute'
            case _:
                name_ai = 'mix'
        ai = Player(name_ai, "O")
        board = Board()
        currentPlayer = 1
        player1canMove = True
        aicanMove = True
        nbCoup = 0
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
                aicanMove = board.make_best_move(ai, nbCoup, ai.name, ai.name)
            board.print_board()
            board.getScore(p1)
            board.getScore(ai)
            print(f"Actual score {p1.name} : {p1.score}, {ai.name} : {ai.score}")
            time.sleep(2)

            # Switch player
            currentPlayer = 1 if currentPlayer == 2 else 2
            nbCoup += 1
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
    # Mode AIvAI: Deux IA jouent l'une contre l'autre
    else:
        # Simulation de jeu entre deux IA
        # Logique de jeu pour AIvAI
        n = 0
        winAi = 0
        winRand = 0
        tie = 0
        while n < 1:
            res = IA_sim()
            print(res)
            if res == 1:
                winAi += 1
            elif res == 2:
                winRand += 1
            else:
                tie +=1
            n += 1
        print(f"Fin de la simu Win Ia 1 : {winAi} win Ia 2 : {winRand} egalité : {tie}")

def IA_sim():
    # Fonction pour simuler un jeu entre deux IA
    # Initialisation des IA et du plateau de jeu
    # Boucle principale de jeu pour AIvAI
    endGame = False
    nbCoup = 0
    choice_ai = int(input("Choose algorithm for AI 1 : 1(positional) 2(mobility) 3(absolute) 4(mixte)\n"))
    name_ai = ''
    match choice_ai:
        case 1:
            name_ai = 'positional'
        case 2:
            name_ai = 'move'
        case 3:
            name_ai = 'absolute'
        case _:
            name_ai = 'mix'

    ai1 = Player(name_ai, "O")
    choice_ai = int(input("Choose algorithm for AI 1 : 1(positional) 2(mobility) 3(absolute) 4(mixte)\n"))
    name_ai = ''
    match choice_ai:
        case 1:
            name_ai = 'positional'
        case 2:
            name_ai = 'move'
        case 3:
            name_ai = 'absolute'
        case _:
            name_ai = 'mix'
    ai2 = Player(name_ai, "X")
    board = Board()
    currentPlayer = 1
    ai11canMove = True
    ai2canMove = True
    while not endGame:
        board.clear_board()
        if currentPlayer == 1:
            ai11canMove = board.make_best_move(ai1, nbCoup, ai1.name, ai2.name)
        else:
            ai2canMove = board.make_best_move(ai2, nbCoup, ai2.name, ai1.name)
            #git = board.find_a_correct_move(ai2)
            #if not git:
            #    ai2canMove = False
            #else:
            #    rand = random.randint(0, len(git) - 1)

            #    move_index = random.choice(list(git.keys()))
            #    board.playMove(git[move_index], ai2)

                # board.playMove(git[rand], ai2)
            #    ai2canMove = True
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


if __name__ == '__main__':
    # Point d'entrée du programme pour démarrer un nouveau jeu
    newGame()
