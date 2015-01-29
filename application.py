#coding:utf-8
"""battleship"""
import os
import time
import random

BOARDCOMP = []
USERBOARD = []
SHIPS = {"aircraft": 5, "battleship": 4, "frigate": 3, "submarine": 3, "minesweeper": 2}
CHARACTER = {"aircraft": "| A ", "battleship": "| B ", "frigate": "| F ", "submarine": "| S ", "minesweeper": "| M "}

def create(board):
    """This function adds several lists at the BOARDCOMP list, this will serve to place the boats later."""
    for var in range(0, 10):
        board.append(["|   "] * 10),
    print_tablero(board)


def print_tablero(board):
    """Prints BOARDCOMP list to be displayed as a game board on the screen."""
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

def user_decision():
    create(USERBOARD)
    booleanvar = False
    for boat in SHIPS:
        if boat == "aircraft":
            print "  >Place an %s. It measures %d squares." %(boat, SHIPS[boat])
        else:
            print "  >Place a %s. It measures %d squares." %(boat, SHIPS[boat])
        print ""
        placerow = entering_number_row()
        placecol = entering_number_col()
        position = user_vertical_horizontal()
        if position == "h":
            for horizont in range(SHIPS[boat]):
                USERBOARD[placerow - 1][(placecol - 1) + horizont] = CHARACTER[boat]
            print_tablero(USERBOARD)
        elif position == "v":
            for vertical in range(SHIPS[boat]):
                USERBOARD[(placerow - 1) + vertical][placecol - 1] = CHARACTER[boat]
            print_tablero(USERBOARD)


def placing_ship_vertical(coordx, coordy, boat):
    pass



def user_vertical_horizontal():
    print ""
    print "Select the position of your boat."
    print "Press 'v' to place boat vertically."
    print "Press 'h' to place the boat horizontally."
    while True:
        print ""
        decisionuser = raw_input("   >* v/h: ")
        decision_low = decisionuser.lower()
        if decision_low == "h":
            print "horizontal"
            return "h"
            break
        elif decision_low == "v":
            print "vertical"
            return "v"
            break
        else:
            print ""
            print chr(27) + "[0;91m" + "   Invalid data!." + chr(27) + "[0m"
            print ""
            print "Press 'v' to place boat vertically."
            print "Press 'h' to place the boat horizontally."

def random_row(board):
    """This function generates a random number to locate the row number on the game board."""
    return random.randint(1, len(board))



def random_col(board):
    """This function generates a random number to locate the column number on the game board."""
    return random.randint(1, len(board[0]))


def check_dictionary(dictionary):
    cycle = 0
    found = 0
    nomatch = 0
    while cycle != 10:
        for x in range(10):
            if "| X " in dictionary[cycle][x]:
                found += 1
            else:
                nomatch += 1
        cycle += 1
    print found
    print nomatch



def more_ships():
    """This function creates random coordinates to position five ships."""
    position = ["v", "h"]
    verthorizon = random.choice(position)
    numb_x1 = random_row(BOARDCOMP)
    numb_y1 = random_col(BOARDCOMP)
    numb_x2 = random_row(BOARDCOMP)
    numb_y2 = random_col(BOARDCOMP)
    numb_x3 = random_row(BOARDCOMP)
    numb_y3 = random_col(BOARDCOMP)
    numb_x4 = random_row(BOARDCOMP)
    numb_y4 = random_col(BOARDCOMP)
    numb_x5 = random_row(BOARDCOMP)
    numb_y5 = random_col(BOARDCOMP)


    while (numb_x1 == numb_x2 and numb_y1 == numb_y2) or (numb_x1 == numb_x3 and numb_y1 == numb_y3) or (numb_x1 == numb_x4 and numb_y1 == numb_y4) or (numb_x1 == numb_x5 and numb_y1 == numb_y5) or (numb_x2 == numb_x3 and numb_y2 == numb_y3) or (numb_x2 == numb_x4 and numb_y2 == numb_y4) or (numb_x2 == numb_x5 and numb_y2 == numb_y5) or (numb_x3 == numb_x4 and numb_y3 == numb_y4) or (numb_x3 == numb_x5 and numb_y3 == numb_y5) or (numb_x4 == numb_x5 and numb_y4 == numb_y5):
        numb_x1 = random_row(BOARDCOMP) #If the coordinates are identical, new coordinates
        numb_y1 = random_col(BOARDCOMP) # are generated until no matches are found.
        numb_x2 = random_row(BOARDCOMP)
        numb_y2 = random_col(BOARDCOMP)
        numb_x3 = random_row(BOARDCOMP)
        numb_y3 = random_col(BOARDCOMP)
        numb_x4 = random_row(BOARDCOMP)
        numb_y4 = random_col(BOARDCOMP)
        numb_x5 = random_row(BOARDCOMP)
        numb_y5 = random_col(BOARDCOMP)


    print "   ---1-----"
    print "x1 ", numb_x1
    print "y1 ", numb_y1
    print "   ---2-----"
    print "x2 ", numb_x2
    print "y2 ", numb_y2
    print "   ---3-----"
    print "x3 ", numb_x3
    print "y3 ", numb_y3
    print "   ---4-----"
    print "x4 ", numb_x4
    print "y4 ", numb_y4
    print "   ---5-----"
    print "x5 ", numb_x5
    print "y5 ", numb_y5
    print verthorizon

    mainvarios(numb_x1, numb_y1, numb_x2, numb_y2, numb_x3, numb_y3, numb_x4, numb_y4, numb_x5, numb_y5)


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



def entering_number_row():
    """Allows the user to guess the row number where a boat can be placed."""
    while True:
        try:
            print ""
            guessrow = int(raw_input("   >Enter row: "))
            if guessrow >= 1 and guessrow <= 10:
                return guessrow
                break
            else:
                print ""
                print "Please enter numbers in the range of 1 - 10"
        except:
            print ""
            print "Please enter numbers!"



def entering_number_col():
    """Allows the user to guess the column number where a boat can be placed."""
    while True:
        try:
            print ""
            guesscol = int(raw_input("   >Enter column: "))
            if guesscol >= 1 and guesscol <=10:
                return guesscol
                break
            else:
                print ""
                print "Please enter numbers in the range of 1 - 10"
        except:
            print ""
            print "Please enter numbers!"



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
            user_decision()
            break
        elif decision == "2":
            print ""
            break
        elif decision == "3":
            print "3"
            break
        elif decision == "4":
            clear()
            break
        else:
            print ""
            print chr(27) + "[0;91m" + "   Please enter NUMBERS from 1 to 4." + chr(27) + "[0m"
            print ""


clear()
loading()
clear()
first()
menu()


