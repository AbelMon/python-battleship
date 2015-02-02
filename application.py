#coding:utf-8
"""battleship"""
import os
import time
import random
import copy
import pygame

BOARDCOMP = [] #This list stores the data of the computer board.
USERBOARD = [] #This list stores the data of the user board.
VERSUSBOARD = []
COMPUTER_INSULTS = ["Hahaha. You like that?", "I will destroy you.", "That had to hurt", "Boom!", "Burn, baby!", "Squeal boy, squeal!", "Toasted!", "Die human!"]


SHIPS = {"aircraft": 5, "battleship": 4, "frigate": 3, "submarine": 3, "minesweeper": 2}
CHARACTER = {"aircraft": "| A ", "battleship": "| B ", "frigate": "| F ", "submarine": "| S ", "minesweeper": "| M "}



def create(board):
    """This function adds several lists at the board list, this will serve to place the boats later."""
    for var in range(0, 10):
        board.append(["|   "] * 10),



def print_tablero(board):
    """Prints board list to be displayed as a game board on the screen."""
    print ""
    print "      1   2   3   4   5   6   7   8   9  10"
    print "    -----------------------------------------"
    for fila, elemento in enumerate(board):
        if fila < 9:
            print fila + 1, " ", "".join(elemento) + "|"
            print "    -----------------------------------------"
        else:
            print fila + 1,"", "".join(elemento) + "|"
            print "    -----------------------------------------" 


def random_row(board):
    """This function generates a random number to locate the row number on the game board."""
    return random.randint(0, len(board) - 1)



def random_col(board):
    """This function generates a random number to locate the column number on the game board."""
    return random.randint(0, len(board[0]) - 1)


def user_decision():
    """This function allows the user to decide the position of their ships."""
    create(USERBOARD)
    print_tablero(USERBOARD)
    for boat in SHIPS:
        condicion = False
        while condicion == False: #This allows repeat the cycle every time an error is returned.
            if boat == "aircraft":
                print ">- Place an " + chr(27) + "[3;96m" + boat + chr(27) + "[0m", "it measures", chr(27) + "[3;96m"+ str(SHIPS[boat]) + " squares." + chr(27) + "[0m"
            else:
                print ">- Place a " + chr(27) + "[3;96m" + boat + chr(27) + "[0m", "it measures", chr(27) + "[3;96m"+ str(SHIPS[boat]) + " squares." + chr(27) + "[0m"
            placerow = entering_number_row()
            placecol = entering_number_col()
            position = user_vertical_horizontal()
            if position == "h":
                there_are_boat = no_intersection_horizontal(USERBOARD,SHIPS, boat, placerow, placecol)
                if there_are_boat != False:
                    placing_ship_horizon(USERBOARD,placerow, placecol, boat)
                    clear()
                    print_tablero(USERBOARD)
                    condicion = True
            elif position == "v":
                boat_in_vertical = no_exist_vertical(USERBOARD, SHIPS, boat, placerow, placecol)
                if boat_in_vertical != False:
                    placing_ship_vertical(USERBOARD, placerow, placecol, boat)
                    clear()
                    print_tablero(USERBOARD)
                    condicion = True



def no_intersection_horizontal(board,dict_ship, boat, row_x, col_y):
    """This function checks that the boats are not placed on other boats."""
    count = 0 #This variable stores the count of the string "|   ".

    try:
        for number in range(dict_ship[boat]):
            if "|   " in board[row_x][col_y + number]:
                count += 1 #When a string "|   " is found, adds 1 to the variable count.
    except: #If an error occurs, an error message is displayed and returns False.
        print ""
        print chr(27) + "[0;91m" + "    ⚠ You can not put the boat in this position. It is off the board." + chr(27) + "[0m"
        print ""
        return False

    if count == dict_ship[boat]: #If the value of "boat" and the value of "count" match, returns True
        return True
    else: #If the values are different, returns False.
        print ""
        print chr(27) + "[0;91m" + "    ✘ In this position already exists a boat. Try again." + chr(27) + "[0m"
        print ""
        return False 



def no_exist_vertical(board, dict_ship, boat, row_x, col_y):
    """This function checks that the boats are not placed on other boats in vertical position."""
    count = 0 #This variable stores the count of the string "|   ".

    try:
        for number in range(dict_ship[boat]):
            if "|   " in board[row_x + number][col_y]:
                count += 1 #When a string "|   " is found, adds 1 to the variable count.
    except: #If an error occurs, an error message is displayed and returns False.
        print ""
        print chr(27) + "[0;91m" + "    ⚠ You can not put the boat in this position. It is off the board." + chr(27) + "[0m"
        print ""
        return False

    if count == dict_ship[boat]: #If the value of "boat" and the value of "count" match, returns True
        return True
    else: #If the values are different, returns False.
        print ""
        print chr(27) + "[0;91m" + "    ✘ In this position already exists a boat. Try again." + chr(27) + "[0m"
        print ""
        return False 



def placing_ship_horizon(board, coordx, coordy, boat):
    try:
        for intento in range(SHIPS[boat]):
            board[coordx][coordy + intento] = CHARACTER[boat]
    except:
        try:
            for intento in range(SHIPS[boat]):
                board[coordx][coordy + intento] = "|   "
        except:
            print ""
            print "You can not put the boat in this position. It is off the board."
            return False




def placing_ship_vertical(board, coordx, coordy, boat):
    try:
        for intento in range(SHIPS[boat]):
            board[coordx + intento][coordy] = CHARACTER[boat]
    except:
        try:
            for intento in range(SHIPS[boat]):
                board[coordx + intento ][coordy] = "|   "
        except:
            print ""
            print chr(27) + "[0;91m" + "    ⚠ You can not put the boat in this position. It is off the board." + chr(27) + "[0m"
            print ""
            return False



def user_vertical_horizontal():
    message_text = chr(27) + "[0;95m" + """
   //*Select the position of your boat.
   //*Press 'v' to place boat vertically.
   //*Press 'h' to place the boat horizontally.""" + chr(27) + "[0m"
    print message_text

    while True:
        print ""
        decisionuser = raw_input("   >* v/h: ")
        decision_low = decisionuser.lower()
        if decision_low == "h":
            return "h"
            break
        elif decision_low == "v":
            return "v"
            break
        else:
            print ""
            print chr(27) + "[0;91m" + "              ✘ Invalid data!." + chr(27) + "[0m"
            print message_text



def computer_ships():
    create(BOARDCOMP)
    for boat in SHIPS:
        condicion = False
        while condicion == False:
            position = ["v", "h"]
            numb_x = random_row(BOARDCOMP)
            numb_y = random_col(BOARDCOMP)
            positionchoice = random.choice(position)
            if positionchoice == "h":
                no_boat = no_intersection_horizontal(BOARDCOMP, SHIPS, boat, numb_x, numb_y)
                if no_boat != False:
                    placing_ship_horizon(BOARDCOMP, numb_x, numb_y, boat)
                    condicion = True
            elif positionchoice == "v":
                no_boat_vertical = no_exist_vertical(BOARDCOMP, SHIPS, boat, numb_x, numb_y)
                if no_boat_vertical != False:
                    placing_ship_vertical(BOARDCOMP, numb_x, numb_y, boat)
                    condicion = True


def entering_number_row():
    """Allows the user to guess the row number where a boat can be placed."""
    while True:
        try:
            print ""
            guessrow = int(raw_input("   >Enter row: "))
            if guessrow >= 1 and guessrow <= 10:
                guessrow -= 1
                return guessrow
                break
            else:
                print ""
                print chr(27) + "[0;91m" + "     ✘ Please enter numbers in the range of 1 - 10." + chr(27) + "[0m"
        except:
            print ""
            print chr(27) + "[0;91m" + "     ✘ Please enter numbers!" + chr(27) + "[0m"



def entering_number_col():
    """Allows the user to guess the column number where a boat can be placed."""
    while True:
        try:
            print ""
            guesscol = int(raw_input("   >Enter column: "))
            if guesscol >= 1 and guesscol <=10:
                guesscol -= 1
                return guesscol
                break
            else:
                print ""
                print chr(27) + "[0;91m" + "     ✘ Please enter numbers in the range of 1 - 10." + chr(27) + "[0m"
        except:
            print ""
            print chr(27) + "[0;91m" + "     ✘ Please enter numbers!" + chr(27) + "[0m"


def statistics(board):
    count = 0
    aircraft = 0
    battleship = 0
    frigate = 0
    submarine = 0
    minesweeper = 0
    while count != 10:
        for col in range(10):
            if "| A " in board[count][col]:
                aircraft += 1
            if "| B " in board[count][col]:
                battleship += 1
            if "| F " in board[count][col]:
                frigate += 1
            if "| S " in board[count][col]:
                submarine += 1
            if "| M " in board[count][col]:
                minesweeper += 1
        count += 1
    print ""
    print "        Enemy ships        Squares undamaged"
    print "         Aircraft:               ", aircraft
    print "         Battleship:             ", battleship
    print "         Submarine:              ", submarine
    print "         Frigate:                ", frigate
    print "         Minesweeper:            ", minesweeper
    print ""


def statistics_user(board):
    count = 0
    aircraft = 0
    battleship = 0
    frigate = 0
    submarine = 0
    minesweeper = 0
    while count != 10:
        for col in range(10):
            if "| A " in board[count][col]:
                aircraft += 1
            if "| B " in board[count][col]:
                battleship += 1
            if "| F " in board[count][col]:
                frigate += 1
            if "| S " in board[count][col]:
                submarine += 1
            if "| M " in board[count][col]:
                minesweeper += 1
        count += 1
    print ""
    print "         Your ships        Squares undamaged"
    print "         Aircraft:               ", aircraft
    print "         Battleship:             ", battleship
    print "         Submarine:              ", submarine
    print "         Frigate:                ", frigate
    print "         Minesweeper:            ", minesweeper
    print ""


def count_damage(board):
    count = 0
    aircraft = 0
    battleship = 0
    frigate = 0
    submarine = 0
    minesweeper = 0
    while count != 10:
        for col in range(10):
            if "| A " in board[count][col]:
                aircraft += 1
            if "| B " in board[count][col]:
                battleship += 1
            if "| F " in board[count][col]:
                frigate += 1
            if "| S " in board[count][col]:
                submarine += 1
            if "| M " in board[count][col]:
                minesweeper += 1
        count += 1

    if aircraft == 0 and battleship == 0 and frigate == 0 and submarine == 0 and minesweeper == 0:
        print "Victory is yours"
        return True
    else:
        return False


def count_damage_comp(board):
    count = 0
    aircraft = 0
    battleship = 0
    frigate = 0
    submarine = 0
    minesweeper = 0
    while count != 10:
        for col in range(10):
            if "| A " in board[count][col]:
                aircraft += 1
            if "| B " in board[count][col]:
                battleship += 1
            if "| F " in board[count][col]:
                frigate += 1
            if "| S " in board[count][col]:
                submarine += 1
            if "| M " in board[count][col]:
                minesweeper += 1
        count += 1

    if aircraft == 0 and battleship == 0 and frigate == 0 and submarine == 0 and minesweeper == 0:
        print "You lose"
        return True
    else:
        return False


def main():
    row = random_row(BOARDCOMP)
    col = random_col(BOARDCOMP)
    print row
    print col
    userrow = entering_number_row()
    usercol = entering_number_col()
    print userrow
    print ">>>"
    print type(userrow)
    if userrow == row and usercol == col:
        print "Well done!"
    else:
        BOARDCOMP[userrow - 1][usercol - 1] = "| X "
        print_tablero(BOARDCOMP)



def game_alone():
    print_tablero(VERSUSBOARD)
    statistics(BOARDCOMP)
    adivina_row = entering_number_row()
    adivina_col = entering_number_col()
    clear()
    view_board = hit_boat(BOARDCOMP, VERSUSBOARD, adivina_row, adivina_col)
    return view_board



def computer_turn():
    hitrow = random_row(USERBOARD)
    hitcol = random_col(USERBOARD)
    view_board = hit_boat_computer(USERBOARD, hitrow, hitcol)
    return view_board



def hit_boat_computer(board, hitrow, hitcol):
    if "|   " in board[hitrow][hitcol]:
        board[hitrow][hitcol] = "| o "
        print_tablero(board)
        statistics_user(board)
        print "    The enemy has failed."
        print "    Now it's your turn."
        raw_input("    Press enter...")
        return 0
    else:
        if "| o " in board[hitrow][hitcol]:
            return 1
        elif "| x " in board[hitrow][hitcol]:
            return 1
        else:
            board[hitrow][hitcol] = "| x "
            print_tablero(board)
            print ""
            print "   Enemy message: " + random.choice(COMPUTER_INSULTS)
            print ""
            statistics_user(board)
            print "   The enemy has impacted your boat."
            raw_input("   Press enter...")
            return 1



def turnos():
    create(VERSUSBOARD)
    turn = 0
    destruction = False
    while destruction == False:
        if turn == 0:
            clear()
            print "                  Your turn"
            turn = game_alone()
            destruction = count_damage(BOARDCOMP)
        elif turn == 1:
            clear()
            print "                  Enemy's turn"
            turn = computer_turn()
            destruction = count_damage_comp(USERBOARD)



def hit_boat(hiden_board, board, hitrow, hitcol):
    if "|   " in hiden_board[hitrow][hitcol]:
        hiden_board[hitrow][hitcol] = "| o "
        board[hitrow][hitcol] = "| o "
        clear()
        print "                  Your turn"
        print_tablero(hiden_board)
        statistics(hiden_board)
        print "      You failed"
        print "      It is turn of the enemy."
        print ""
        raw_input("      Press enter...")
        return 1
    else:
        if "| o " in hiden_board[hitrow][hitcol]:
            print "                  Your turn"
            print_tablero(board)
            statistics(hiden_board)
            print ""
            print "   You've already shot that position. Try again."
            raw_input("   Press enter and try again...")
            return 0
        elif "| x " in hiden_board[hitrow][hitcol]:
            print "                  Your turn"
            print_tablero(board)
            statistics(hiden_board)
            print ""
            print "   You've already shot that position. Try again."
            raw_input("   Press enter and try again...")
            return 0
        else:
            hiden_board[hitrow][hitcol] = "| x "
            board[hitrow][hitcol] = "| x "
            print "                  Your turn"
            print_tablero(board)
            statistics(hiden_board)
            print ""
            print "   You've hit the enemy ship!"
            raw_input("   Press enter...")
            return 0


def mainvarios(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5):
    BOARDCOMP[x1 - 1][y1 - 1] = "| 1 "
    BOARDCOMP[x2 - 1][y2 - 1] = "| 2 "
    BOARDCOMP[x3 - 1][y3 - 1] = "| 3 "
    BOARDCOMP[x4 - 1][y4 - 1] = "| 4 "
    BOARDCOMP[x5 - 1][y5 - 1] = "| 5 "
    print_tablero(BOARDCOMP)
    for turno in range(4):
        guessx = entering_number_row()
        guessy = entering_number_col()
        if (guessx == x1 and guessy == y1) or (guessx == x2 and guessy == y2) or (guessx == x3 and guessy == y3) or (guessx == x4 and guessy == y4) or (guessx == x5 and guessy == y5):
            print "Bien"
            BOARDCOMP[guessx - 1][guessy - 1] = "| X "
            print_tablero(BOARDCOMP)
        else:
            print "No adivinas"
            BOARDCOMP[guessx - 1][guessy - 1] = "| X "
            print_tablero(BOARDCOMP)


def new_game_single():
    while True:
        playAgain = raw_input("    Play again? y/n")
        playAgain = playAgain.lower()
        if playAgain == "y" or playAgain == "yes":
            clear()
            single_secion()
            break
        elif playAgain == "n" or playAgain == "no" or playAgain == "not":
            clear()
            first()
            menu()
            break
        else:
            print ""
            print chr(27) + "[0;91m" + "   ✘ Please enter 'y' or 'n' " + chr(27) + "[0m"


def single_secion():
    print """
             
             
             
    """
    raw_input("         Press enter to continue...")
    clear()
    print ""
    print "     It's time to deploy your ships."
    print "     Enter the coordinates."
    user_decision()
    print ""
    print "         All ships in position."
    print ""
    raw_input("         Press enter to continue...")
    clear()
    computer_ships()
    clear()
    atacar_image()
    time.sleep(2)
    turnos()
    new_game_single()

    pass


def first():
    """This is a function that displays the name of the game and the menu instructions"""
    print u""" 
██████╗**█████╗*████████╗████████╗██╗*****███████╗███████╗██╗**██╗██╗██████╗*██╗
██╔══██╗██╔══██╗╚══██╔══╝╚══██╔══╝██║*****██╔════╝██╔════╝██║**██║██║██╔══██╗██║
██████╔╝███████║***██║******██║***██║*****█████╗**███████╗███████║██║██████╔╝██║
██╔══██╗██╔══██║***██║******██║***██║*****██╔══╝**╚════██║██╔══██║██║██╔═══╝*╚═╝
██████╔╝██║**██║***██║******██║***███████╗███████╗███████║██║**██║██║██║*****██╗
╚═════╝*╚═╝**╚═╝***╚═╝******╚═╝***╚══════╝╚══════╝╚══════╝╚═╝**╚═╝╚═╝╚═╝*****╚═╝
********************************************************************************"""
    print """
                                    __/___
                              _____/______|
                      _______/_____\_______\_____
                      \              < < <       |
                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
    print "   >Welcome to Battleship! Are you ready for war? Everyone to combat positions!"
    print ""
    time.sleep(0.5)
    print "   >Press 1 for single player session."
    time.sleep(0.5)
    print "   >Press 2 for multiplayer session."
    time.sleep(0.5)
    print "   >Press 3 to see the game instructions."
    time.sleep(0.5)
    print "   >Press 4 to exit the program."
    time.sleep(0.5)
    print ""


def atacar_image():
    print ""
    print ""
    print """
 ________  _________  _________  ________  ________  ___  __    ___       
|\   __  \|\___   __\ \___   __\ \   __  \|\   ____\|\  \|\  \ |\  \      
\ \  \|\  \|___ \  \_\|___ \  \_\ \  \|\  \ \  \___|\ \  \/  /|\ \  \     
 \ \   __  \   \ \  \     \ \  \ \ \   __  \ \  \    \ \   ___  \ \  \    
  \ \  \ \  \   \ \  \     \ \  \ \ \  \ \  \ \  \____\ \ \ \ \  \ \__\   
   \ \__\ \__\   \ \__\     \ \__\ \ \__\ \__\ \_______\ \_\ \ \__\|__|   
    \|__|\|__|    \|__|      \|__|  \|__|\|__|\|_______|\|__| \|__|   ___ 
                                                                     |\__\ 
                                                                     \|__|"""


def image_skull():
    print """
                  _________-----_____
       _____------           __      ----_
___----             ___------              \ 
   ----________        ----                 \ 
               -----__    |             _____)
                    __-                /     \ 
        _______-----    ___--          \    /)\ 
  ------_______      ---____            \__/  /
               -----__    \ --    _          /\ 
                      --__--__     \_____/   \_/\ 
                              ----|   /          |
                                  |  |___________|
                                  |  | ((_(_)| )_)
                                  |  \_((_(_)|/(_)
                                  \             (
                                   \_____________)"""



def loading():
    """Function that displays a load message at the start of the game."""
    print """
                                                       
                                                       
                                  |  _  _  _|. _  _    
                                  |_(_)(_|(_||| |(_|...
                                                  _|   """
    time.sleep(2)



def clear():
    """This function clears the screen at the terminal. Works on windows and ubuntu."""
    if os.name == "posix":
        os.system("reset")
    elif os.name == "nt":
        os.system("cls")


def menu():
    """Main Menu."""
    while True:
        decision = raw_input(   ">* Choose an option: ")
        if decision == "1":
            clear()
            print ""
            loading()
            clear()
            single_secion()
            break
        elif decision == "2":
            computer_ships()
            print_tablero(BOARDCOMP)
            count_damage(BOARDCOMP)
            break
        elif decision == "3":
            clear()
            instruccions_single()
            break
        elif decision == "4":
            clear()
            break
        else:
            print ""
            print chr(27) + "[0;91m" + "   ✘ Please enter NUMBERS from 1 to 4." + chr(27) + "[0m"
            print ""


def instruccions_single():
    print """

        ____           __                  __  _                     
       /  _/___  _____/ /________  _______/ /_(_)___  ____  _____    
       / // __ \/ ___/ __/ ___/ / / / ___/ __/ / __ \/ __ \/ ___/    
     _/ // / / (__  ) /_/ /  / /_/ / /__/ /_/ / /_/ / / / (__  )     
    /___/_/ /_/____/\__/_/   \__,_/\___/\__/_/\____/_/ /_/____/


    Before the battle you should place the ships on the board.
    The measures of ships are:

            Ship                          Measure

            Aircraft......................5 squares
            Battleship....................4 squares
            Frigate.......................3 squares
            Submarine.....................3 squares
            Minesweeper...................2 squares
 
 Enter the row number and column number where you want to place your boat.
 You must enter numbers in the range of 1 - 10.
"""
    raw_input("    Press enter to return to the main menu... ")
    clear()
    first()
    menu()



clear()
image_skull()
loading()
clear()
first()
menu()


