#coding:utf-8
"""battleship"""
import os
import time
import random
import copy
import pygame

pygame.mixer.init()


BOARDCOMP = [] #This list stores the data of the computer board.
USERBOARD = [] #This list stores the data of the user board.
VERSUSBOARD = []
PLAYER2 = []
HIDEN1 = []
HIDEN2 = []


COMPUTER_INSULTS = ["You like that?", "That had to hurt...", "Boom!", "Burn, baby!", "Squeal boy, squeal!", "Toasted!", "Loser!", "Eat that!", "Oh yeah!"]
COMPUTER_SUFFER = ["Man Down!", "I'm under heavy attack!","I need some backup!"]



SHIPS = {"aircraft": 5, "battleship": 4, "frigate": 3, "submarine": 3, "minesweeper": 2}
CHARACTER = {"aircraft": "| A ", "battleship": "| B ", "frigate": "| F ", "submarine": "| S ", "minesweeper": "| M "}

pygame.mixer.music.load("Skyward Fire (Original Version).mp3")

SOUNDINVALID = pygame.mixer.Sound("SD_MENU_WRONG_12.wav")
OPTIONSOUND = pygame.mixer.Sound("SD_MENU_SELECT_4.wav")
BADDATA = pygame.mixer.Sound("SD_MENU_WRONG_11.wav")
OTHERVALID = pygame.mixer.Sound("SD_MENU_SELECT_3.wav")


IMPACT = pygame.mixer.Sound("EXPLOBIG.wav")
EXPlOSION = pygame.mixer.Sound("explosion.wav")



YOU_LIKE = pygame.mixer.Sound("You like that.wav") 
BOOM = pygame.mixer.Sound("Boom!.wav")
LOSER = pygame.mixer.Sound("Loser.wav")
YEAH = pygame.mixer.Sound("Oh yeah.wav")
SQUEAL = pygame.mixer.Sound("Squeal boy.wav")
TOASTED = pygame.mixer.Sound("Toasted.wav")
BURN = pygame.mixer.Sound("Burn baby.wav")
EAT = pygame.mixer.Sound("Eat that.wav")
HURT = pygame.mixer.Sound("That hurt.wav")


VICTORY = pygame.mixer.Sound("Winner.wav") 


TAUNTS = {"You like that?": YOU_LIKE, "That had to hurt...": HURT, "Boom!": BOOM, "Burn, baby!": BURN, "Squeal boy, squeal!": SQUEAL, "Toasted!": TOASTED, "Loser!": LOSER, "Eat that!": EAT, "Oh yeah!":YEAH}


def create(board):
    """This function adds several lists at the board list, this will serve to place the boats later."""
    for var in range(0, 10):
        board.append(["|   "] * 10),



def print_tablero(board):
    """Prints board list to be displayed as a game board on the screen."""
    print ""
    print "      1   2   3   4   5   6   7   8   9  10"
    print chr(27) + "[0;94m" + "    -----------------------------------------" + chr(27) + "[0m"
    for fila, elemento in enumerate(board):
        if fila < 9:
            print fila + 1, chr(27) + "[0;94m" + " ", "".join(elemento) + "|"
            print "    -----------------------------------------" + chr(27) + "[0m"
        else:
            print fila + 1,chr(27) + "[0;94m"+ "", "".join(elemento) + "|"
            print "    -----------------------------------------" + chr(27) + "[0m"


def random_row(board):
    """This function generates a random number to locate the row number on the game board."""
    return random.randint(0, len(board) - 1)



def random_col(board):
    """This function generates a random number to locate the column number on the game board."""
    return random.randint(0, len(board[0]) - 1)


def user_decision(board):
    """This function allows the user to decide the position of their ships."""
    create(board)
    print_tablero(board)
    for boat in SHIPS: #Choose one by one the boats in the dictionary to be placed.
        condicion = False
        while condicion == False: #This allows repeat the cycle every time an error is returned.
            if boat == "aircraft": #
                print ">- Place an " + chr(27) + "[3;96m" + boat + chr(27) + "[0m", "it measures", chr(27) + "[3;96m"+ str(SHIPS[boat]) + " squares." + chr(27) + "[0m"
            else:
                print ">- Place a " + chr(27) + "[3;96m" + boat + chr(27) + "[0m", "it measures", chr(27) + "[3;96m"+ str(SHIPS[boat]) + " squares." + chr(27) + "[0m"
            placerow = entering_number_row()
            placecol = entering_number_col()
            position = user_vertical_horizontal()
            if position == "h":
                there_are_boat = no_intersection_horizontal(board, SHIPS, boat, placerow, placecol) #Checks the existence of boats in horizontal position and  if they are put off the board
                if there_are_boat != False: #If true, it means that no ships. Otherwise the loop is repeated again.
                    placing_ship_horizon(board, placerow, placecol, boat) #Place the boats.
                    clear()
                    print_tablero(board)
                    condicion = True #The loop ends to spend the next boat.
            elif position == "v":
                boat_in_vertical = no_exist_vertical(board, SHIPS, boat, placerow, placecol) #Checks the existence of boats in vertical position and  if they are put off the board.
                if boat_in_vertical != False: #If true, it means that no ships. Otherwise the loop is repeated again.
                    placing_ship_vertical(board, placerow, placecol, boat) #Place the boats.
                    clear()
                    print_tablero(board)
                    condicion = True #The loop ends to spend the next boat.



def no_intersection_horizontal(board,dict_ship, boat, row_x, col_y):
    """This function checks that the boats are not placed on other boats."""
    count = 0 #This variable stores the count of the string "|   ".

    try:
        for number in range(dict_ship[boat]):
            if "|   " in board[row_x][col_y + number]:
                count += 1 #When a string "|   " is found, adds 1 to the variable count.
    except: #If an error occurs, an error message is displayed and returns False.
        BADDATA.play()
        print ""
        print chr(27) + "[0;91m" + "    ⚠ You can not put the boat in this position. It is off the board." + chr(27) + "[0m"
        print ""
        return False

    if count == dict_ship[boat]: #If the value of "boat" and the value of "count" match, returns True, it means there are no boats.
        OTHERVALID.play().set_volume(0.1)
        return True
    else: #If the values are different, returns False.
        SOUNDINVALID.play()
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
        BADDATA.play()
        print ""
        print chr(27) + "[0;91m" + "    ⚠ You can not put the boat in this position. It is off the board." + chr(27) + "[0m"
        print ""
        return False

    if count == dict_ship[boat]: #If the value of "boat" and the value of "count" match, returns True, it means there are no boats.
        OTHERVALID.play().set_volume(0.1)
        return True
    else: #If the values are different, returns False.
        SOUNDINVALID.play()
        print ""
        print chr(27) + "[0;91m" + "    ✘ In this position already exists a boat. Try again." + chr(27) + "[0m"
        print ""
        return False 



def placing_ship_horizon(board, coordx, coordy, boat):
    """Esta funcion permite colocar los barcos en posición horizontal."""
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
    """This function allows you to place the boats upright."""
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
    """This function allows the user to choose the position of the boat."""
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
            return "h" #If the user chooses horizontal, returns h, and another function is responsible for placing the ship.
            break
        elif decision_low == "v":
            return "v" #If the user chooses vertical, returns v, and another function is responsible for placing the ship.
            break
        else:
            BADDATA.play()
            print ""
            print chr(27) + "[0;91m" + "              ✘ Invalid data!." + chr(27) + "[0m"
            print message_text



def computer_ships():
    """This function places the computer's ships  randomly."""
    create(BOARDCOMP)
    for boat in SHIPS: #Choose one by one the boats in the dictionary to be placed.
        condicion = False
        while condicion == False:
            position = ["v", "h"]
            numb_x = random_row(BOARDCOMP) ##Chooses row at random.
            numb_y = random_col(BOARDCOMP) #Chooses column at random.
            positionchoice = random.choice(position) #Chooses position at random.
            if positionchoice == "h":
                no_boat = no_intersection_horizontal(BOARDCOMP, SHIPS, boat, numb_x, numb_y) #Checks the existence of boats in horizontal position and  if they are put off the board
                if no_boat != False:
                    placing_ship_horizon(BOARDCOMP, numb_x, numb_y, boat) #Place the boats.
                    condicion = True
            elif positionchoice == "v":
                no_boat_vertical = no_exist_vertical(BOARDCOMP, SHIPS, boat, numb_x, numb_y) #Checks the existence of boats in vertical position and  if they are put off the board.
                if no_boat_vertical != False:
                    placing_ship_vertical(BOARDCOMP, numb_x, numb_y, boat) #Place the boats.
                    condicion = True


def entering_number_row():
    """Allows the user to enter a row number."""
    while True:
        try:
            print ""
            guessrow = int(raw_input("   >Enter row: "))
            if guessrow >= 1 and guessrow <= 10:
                OPTIONSOUND.play()
                guessrow -= 1
                return guessrow
                break
            else:
                SOUNDINVALID.play()
                print ""
                print chr(27) + "[0;91m" + "     ✘ Please enter numbers in the range of 1 - 10." + chr(27) + "[0m"
        except:
            BADDATA.play()
            print ""
            print chr(27) + "[0;91m" + "     ✘ Please enter numbers!" + chr(27) + "[0m"



def entering_number_col():
    """Allows the user to enter a column number."""
    while True:
        try:
            print ""
            guesscol = int(raw_input("   >Enter column: "))
            if guesscol >= 1 and guesscol <=10:
                OPTIONSOUND.play()
                guesscol -= 1
                return guesscol
                break
            else:
                SOUNDINVALID.play()
                print ""
                print chr(27) + "[0;91m" + "     ✘ Please enter numbers in the range of 1 - 10." + chr(27) + "[0m"
        except:
            BADDATA.play()
            print ""
            print chr(27) + "[0;91m" + "     ✘ Please enter numbers!" + chr(27) + "[0m"


def statistics(board):
    """Allows you see the statistics of enemy boats on display."""
    count = 0
    aircraft = 0
    battleship = 0
    frigate = 0
    submarine = 0
    minesweeper = 0
    while count != 10: #Account in the entire list, the characters of vessels.
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
    """Allows you see the statistics your boats on display."""
    count = 0
    aircraft = 0
    battleship = 0
    frigate = 0
    submarine = 0
    minesweeper = 0
    while count != 10: #Account in the entire list, the characters of vessels.
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
    """counts the number of characters of boats stored in the list, if there are no characters returns true, to finish the game."""
    count = 0
    aircraft = 0
    battleship = 0
    frigate = 0
    submarine = 0
    minesweeper = 0
    while count != 10: #Account in the entire list, the characters of vessels.
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

    if aircraft == 0 and battleship == 0 and frigate == 0 and submarine == 0 and minesweeper == 0: #If there are no boats, means the game is over.
        VICTORY.play()

        if board == PLAYER2:
            print ""
            print "                     Player 1 wins!"
            print ""

        elif board == USERBOARD:
            print ""
            print "                     Player 2 wins!"
            print ""

        elif board == BOARDCOMP:
            print ""
            print "                     You win!"
            print ""

        print u"""
      __    __    _____     ____   ________     ____     ______    __      __ 
      ).)  (.(   (_..._)   /.___) (___..___)   /.__.\   (...__.\   ).\    /.( 
     (.(    ).)    |.|    /./         ).)     /./..\.\   ).(__).)   \.\  /./  
      \.\  /./     |.|   (.(         (.(     (.()..().) (....__/     \.\/./   
       \.\/./      |.|   (.(          ).)    (.()..().)  ).\.\.._     \../    
        \../      _|.|__  \.\___     (.(      \.\__/./  (.(.\.\_))     )(     
         \/      /_____(   \____)    /__\      \____/    )_).\__/     /__\    
     .........................................................................
"""
        return True #Returns true to end the game.
    else:
        return False #If the condition is not met, returns false and the game continues.


def count_damage_comp(board):
    """Account the damage caused by the computer to the user"""
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
        print ""
        print "                     You've been defeated" #if no any ship, means the computer has won.
        print ""
        print """
      ._______..._______.._______.._______.....___....___________.
      |       \.|  .____||  .____||  .____|.../   \..|           |
      |  .--.  ||  |__...|  |__...|  |__...../ .^. \.`---|  |----`
      |  |..|  ||  .__|..|  .__|..|  .__|.../  /_\  \....|  |.....
      |  '--'  ||  |____.|  |.....|  |____./  _____  \...|  |.....
      |_______/.|_______||__|.....|_______/__/.....\__\..|__|.....
      ............................................................
"""
        return True
    else:
        return False #If the condition is not met, returns false and the game continues.



def game_alone():
    """allows the user to guess where are the enemy ships."""
    print_tablero(VERSUSBOARD)
    statistics(BOARDCOMP)
    adivina_row = entering_number_row()
    adivina_col = entering_number_col()
    clear()
    view_board = hit_boat(BOARDCOMP, VERSUSBOARD, adivina_row, adivina_col)
    return view_board



def game_multiplayer(hiden_board, show_board):
    """allows the user to guess where are the enemy ships in a multiplayer session."""
    print_tablero(show_board)
    statistics(hiden_board)
    adivina_row = entering_number_row()
    adivina_col = entering_number_col()
    clear()
    view_board = hit_boat(hiden_board, show_board, adivina_row, adivina_col)
    return view_board



def computer_turn():
    """The computer tries to guess where are the boats."""
    hitrow = random_row(USERBOARD)
    hitcol = random_col(USERBOARD)
    view_board = hit_boat_computer(USERBOARD, hitrow, hitcol)
    return view_board



def hit_boat_computer(board, hitrow, hitcol):
    """f"""
    if "|   " in board[hitrow][hitcol]:
        board[hitrow][hitcol] = "| o "
        print "                  Poor shooting!"
        print ""
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
            EXPlOSION.play()
            board[hitrow][hitcol] = "| x "
            print "                  Impact!"
            print ""
            print_tablero(board)
            insulto = random.choice(COMPUTER_INSULTS)
            print ""
            print "   Enemy message: " + str(insulto)
            print ""
            statistics_user(board)
            print "   The enemy has impacted your boat."
            time.sleep(0.4)
            TAUNTS[insulto].play()
            raw_input("   Press enter...")
            return 1


def turnos():
    """Manage shifts for a single player session."""
    create(VERSUSBOARD)
    turn = 0
    destruction = False
    while destruction == False:
        if turn == 0:
            clear()
            print "                  Your turn"
            print ""
            print ""
            print ""
            turn = game_alone()
            destruction = count_damage(BOARDCOMP)
        elif turn == 1:
            clear()
            print "                  Enemy's turn"
            print ""
            turn = computer_turn()
            destruction = count_damage_comp(USERBOARD)



def turnos_multiplayer():
    """Manage shifts for a multi player session."""
    turn = 0
    destruction = False
    while destruction == False:
        if turn == 0:
            clear()
            print "                  Shoot Player 1"
            print ""
            print ""
            print ""
            turn = game_multiplayer(PLAYER2, HIDEN2)
            destruction = count_damage(PLAYER2)
        elif turn == 1:
            clear()
            print "                  Shoot Player 2"
            print ""
            print ""
            print ""
            turn = game_multiplayer(USERBOARD, HIDEN1)
            destruction = count_damage(USERBOARD)



def hit_boat(hiden_board, board, hitrow, hitcol):
    if "|   " in hiden_board[hitrow][hitcol]:
        hiden_board[hitrow][hitcol] = "| o "
        board[hitrow][hitcol] = "| o "
        clear()
        if hiden_board == PLAYER2:
            print "                  Shoot Player 1"
        elif hiden_board == USERBOARD:
            print "                  Shoot Player 2"
        else:
            print "                  Your Turn"

        print ""
        print "                  Poor shooting!"
        print ""
        print_tablero(hiden_board)
        statistics(hiden_board)
        print ""
        print "      You failed"

        if hiden_board == PLAYER2:
            print "      It's turn of player 2"
        elif hiden_board == USERBOARD:
            print "      It's turn of player 1"
        else:
            print "      It's the enemy's turn!"

        raw_input("      Press enter...")

        if hiden_board == USERBOARD:
            return 0
        else:
            return 1

    else:
        if "| o " in hiden_board[hitrow][hitcol]:

            if hiden_board == PLAYER2:
                print "                  Shoot Player 1"
            elif hiden_board == USERBOARD:
                print "                  Shoot Player 2"
            else:
                print "                  Your Turn"
            print ""
            print "                    Not again!"
            print ""
            print_tablero(board)
            statistics(hiden_board)
            print ""
            print "   You've already shot that position. Try again."
            raw_input("   Press enter and try again...")

            if hiden_board == USERBOARD:
                return 1
            else:
                return 0

        elif "| x " in hiden_board[hitrow][hitcol]:

            if hiden_board == PLAYER2:
                print "                  Shoot Player 1"
            elif hiden_board == USERBOARD:
                print "                  Shoot Player 2"
            else:
                print "                  Your Turn"

            print ""
            print "                    Not again!"
            print ""
            print_tablero(board)
            statistics(hiden_board)
            print ""
            print "   You've already shot that position. Try again."
            raw_input("   Press enter and try again...")
            if hiden_board == USERBOARD:
                return 1
            else:
                return 0
        else:
            IMPACT.play()
            hiden_board[hitrow][hitcol] = "| x "
            board[hitrow][hitcol] = "| x "

            if hiden_board == PLAYER2:
                print "                  Shoot Player 1"
            elif hiden_board == USERBOARD:
                print "                  Shoot Player 2"
            else:
                print "                  Your Turn"

            print ""
            print "                  Impact!"
            print ""
            print_tablero(board)
            statistics(hiden_board)
            print ""
            print "   You've hit the enemy ship!"
            raw_input("   Press enter...")
            if hiden_board == USERBOARD:
                return 1
            else:
                return 0




def new_game_single():
    while True:
        playAgain = raw_input("    Play again? y/n ")
        playAgain = playAgain.lower()
        if playAgain == "y" or playAgain == "yes":
            limpiar(USERBOARD, BOARDCOMP, VERSUSBOARD, PLAYER2, HIDEN1, HIDEN2)
            clear()
            single_secion()
            break
        elif playAgain == "n" or playAgain == "no" or playAgain == "not":
            limpiar(USERBOARD, BOARDCOMP, VERSUSBOARD, PLAYER2, HIDEN1, HIDEN2)
            clear()
            first()
            menu()
            break
        else:
            print ""
            print chr(27) + "[0;91m" + "   ✘ Please enter 'y' or 'n' " + chr(27) + "[0m"



def new_game_multiplayer():
    while True:
        new_game = raw_input("    Play again? y/n ")
        new_game = new_game.lower()
        if new_game == "y" or new_game == "yes":
            limpiar(USERBOARD, BOARDCOMP, VERSUSBOARD, PLAYER2, HIDEN1, HIDEN2)
            clear()
            multiplayer()
            break
        elif new_game == "n" or new_game == "no" or new_game == "not":
            limpiar(USERBOARD, BOARDCOMP, VERSUSBOARD, PLAYER2, HIDEN1, HIDEN2)
            clear()
            first()
            menu()
            break
        else:
            print ""
            print chr(27) + "[0;91m" + "   ✘ Please enter 'y' or 'n' " + chr(27) + "[0m"



def limpiar(board1, board2, board3, board4, board5, board6):
    length_board1 = len(board1)
    length_board2 = len(board2)
    length_board3 = len(board3)
    length_board4 = len(board4)
    length_board5 = len(board5)
    length_board6 = len(board6)

    if length_board1 > 0:
        for count in range(length_board1):
            del board1[0]

    if length_board2 > 0:
        for count in range(length_board2):
            del board2[0]

    if length_board3 > 0:
        for count in range(length_board3):
            del board3[0]

    if length_board4 > 0:
        for count in range(length_board4):
            del board4[0]

    if length_board5 > 0:
        for count in range(length_board5):
            del board5[0]

    if length_board6 > 0:
        for count in range(length_board6):
            del board6[0]



def multiplayer():
    loading()
    print ""
    print ""
    print "          Player 1 places your ships"
    print ""
    raw_input("          Press enter to continue...")
    clear()
    print "     It's time to deploy your ships."
    print "     Enter the coordinates."
    user_decision(USERBOARD)
    create(HIDEN1)
    print ""
    print "         All ships in position."
    raw_input("         Press enter to continue...")
    clear()
    print ""
    print "          Player 2 places your ships"
    print ""
    raw_input("         Press enter to continue...")
    clear()
    print "     It's time to deploy your ships."
    print "     Enter the coordinates."
    user_decision(PLAYER2)
    create(HIDEN2)
    print ""
    print "         All ships in position."
    print "         It's time to fight!"
    print ""
    raw_input("         Press enter to continue...")
    clear()
    atacar_image()
    time.sleep(2)
    clear()
    turnos_multiplayer()
    new_game_multiplayer()


def single_secion():
    print """
             
             
             
    """
    raw_input("         Press enter to continue...")
    clear()
    print ""
    print "     It's time to deploy your ships."
    print "     Enter the coordinates."
    user_decision(USERBOARD)
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
    print chr(27) + "[0;93m" + u""" 
██████╗**█████╗*████████╗████████╗██╗*****███████╗███████╗██╗**██╗██╗██████╗*██╗
██╔══██╗██╔══██╗╚══██╔══╝╚══██╔══╝██║*****██╔════╝██╔════╝██║**██║██║██╔══██╗██║
██████╔╝███████║***██║******██║***██║*****█████╗**███████╗███████║██║██████╔╝██║
██╔══██╗██╔══██║***██║******██║***██║*****██╔══╝**╚════██║██╔══██║██║██╔═══╝*╚═╝
██████╔╝██║**██║***██║******██║***███████╗███████╗███████║██║**██║██║██║*****██╗
╚═════╝*╚═╝**╚═╝***╚═╝******╚═╝***╚══════╝╚══════╝╚══════╝╚═╝**╚═╝╚═╝╚═╝*****╚═╝
********************************************************************************"""+ chr(27) + "[0m"
    print chr(27) + "[0;95m" +"""
                                    __/___
                              _____/______|
                      _______/_____\_______\_____
                      \              < < <       |
                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""" + chr(27) + "[0m"
    print chr(27) + "[1;92m" + "   >Welcome to Battleship! Are you ready for war? Everyone to combat positions!" + chr(27) + "[0m"
    print ""
    time.sleep(0.5)
    OTHERVALID.play().set_volume(0.1)
    print chr(27) + "[3;33m" + "   >Press 1 for single player session."
    time.sleep(0.5)
    OTHERVALID.play().set_volume(0.1)
    print "   >Press 2 for multiplayer session."
    time.sleep(0.5)
    OTHERVALID.play().set_volume(0.1)
    print "   >Press 3 to see the game instructions."
    time.sleep(0.5)
    OTHERVALID.play().set_volume(0.1)
    print "   >Press 4 to exit the program." + chr(27) + "[0m"
    time.sleep(0.5)
    print ""
    OTHERVALID.play().set_volume(0.1)

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
            OPTIONSOUND.play()
            clear()
            print ""
            loading()
            clear()
            single_secion()
            break
        elif decision == "2":
            clear()
            OPTIONSOUND.play()
            multiplayer()
            break
        elif decision == "3":
            OPTIONSOUND.play()
            clear()
            instruccions_single()
            break
        elif decision == "4":
            clear()
            break
        else:
            SOUNDINVALID.play()
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
 
 You must enter the orientation of your boat. It can be vertical or horizontal. 
 You should enter the letter "V" for vertical, or the letter "H" for horizontal.
 
 When you hit the enemy ship you get one more chance.
 When the enemy hit your ship, the enemy gets one more chance.

 The game ends when all boats of any opponent, are destroyed.
 
"""
    raw_input("    Press enter to return to Main Menu... ")
    clear()
    first()
    menu()



clear()
image_skull()
loading()
clear()
pygame.mixer.music.play(-1)
first()
menu()


