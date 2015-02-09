#coding:utf-8
"""battleship"""
import os
import time
import random
import copy
import pygame
import sys

pygame.mixer.init()

class battleship(object):
    """docstring for ClassName"""
    pygame.mixer.music.load("Skyward Fire (Original Version).mp3")

    def __init__(self):
        self.BOARDCOMP = [] #This list stores the data of the computer board.
        self.USERBOARD = [] #This list stores the data of the user board.
        self.VERSUSBOARD = []
        self.PLAYER2 = []
        self.HIDEN1 = []
        self.HIDEN2 = []
    
        self.SOUNDINVALID = pygame.mixer.Sound("SD_MENU_WRONG_12.wav")
        self.OPTIONSOUND = pygame.mixer.Sound("SD_MENU_SELECT_4.wav")
        self.BADDATA = pygame.mixer.Sound("SD_MENU_WRONG_11.wav")
        self.OTHERVALID = pygame.mixer.Sound("SD_MENU_SELECT_3.wav")


        self.IMPACT = pygame.mixer.Sound("EXPLOBIG.wav")
        self.EXPlOSION = pygame.mixer.Sound("explosion.wav")



        self.YOU_LIKE = pygame.mixer.Sound("You like that.wav") 
        self.BOOM = pygame.mixer.Sound("Boom!.wav")
        self.LOSER = pygame.mixer.Sound("Loser.wav")
        self.YEAH = pygame.mixer.Sound("Oh yeah.wav")
        self.SQUEAL = pygame.mixer.Sound("Squeal boy.wav")
        self.TOASTED = pygame.mixer.Sound("Toasted.wav")
        self.BURN = pygame.mixer.Sound("Burn baby.wav")
        self.EAT = pygame.mixer.Sound("Eat that.wav")
        self.HURT = pygame.mixer.Sound("That hurt.wav")


        self.VICTORY = pygame.mixer.Sound("Winner.wav")

        self.COMPUTER_INSULTS = ["You like that?", "That had to hurt...", "Boom!", "Burn, baby!", "Squeal boy, squeal!", "Toasted!", "Loser!", "Eat that!", "Oh yeah!"]
        self.COMPUTER_SUFFER = ["Man Down!", "I'm under heavy attack!","I need some backup!"]



        self.SHIPS = {"aircraft": 5, "battleship": 4, "frigate": 3, "submarine": 3, "minesweeper": 2}
        self.CHARACTER = {"aircraft": "| A ", "battleship": "| B ", "frigate": "| F ", "submarine": "| S ", "minesweeper": "| M "}



        self.TAUNTS = {"You like that?": self.YOU_LIKE, "That had to hurt...": self.HURT, "Boom!": self.BOOM, "Burn, baby!": self.BURN, "Squeal boy, squeal!": self.SQUEAL, "Toasted!": self.TOASTED, "Loser!": self.LOSER, "Eat that!": self.EAT, "Oh yeah!":self.YEAH}


    def create(self, board):
        """This function adds several lists at the board list, this will serve to place the boats later."""
        for var in range(0, 10):
            board.append(["|   "] * 10),



    def print_tablero(self, board):
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


    def random_row(self, board):
        """This function generates a random number to locate the row number on the game board."""
        return random.randint(0, len(board) - 1)



    def random_col(self, board):
        """This function generates a random number to locate the column number on the game board."""
        return random.randint(0, len(board[0]) - 1)


    def user_decision(self, board):
        """This function allows the user to decide the position of their ships."""
        self.create(board)
        self.print_tablero(board)
        for boat in self.SHIPS: #Choose one by one the boats in the dictionary to be placed.
            condicion = False
            while condicion == False: #This allows repeat the cycle every time an error is returned.
                if boat == "aircraft": #
                    print ">- Place an " + chr(27) + "[3;96m" + boat + chr(27) + "[0m", "it measures", chr(27) + "[3;96m"+ str(self.SHIPS[boat]) + " squares." + chr(27) + "[0m"
                else:
                    print ">- Place a " + chr(27) + "[3;96m" + boat + chr(27) + "[0m", "it measures", chr(27) + "[3;96m"+ str(self.SHIPS[boat]) + " squares." + chr(27) + "[0m"
                placerow = self.entering_number_row()
                if placerow == "exit":
                    break
                placecol = self.entering_number_col()
                if placecol == "exit":
                    break
                position = self.user_vertical_horizontal()

                if position == "h":
                    there_are_boat = self.no_intersection_horizontal(board, self.SHIPS, boat, placerow, placecol) #Checks the existence of boats in horizontal position and  if they are put off the board
                    if there_are_boat != False: #If true, it means that no ships. Otherwise the loop is repeated again.
                        self.placing_ship_horizon(board, placerow, placecol, boat) #Place the boats.
                        self.clear()
                        self.print_tablero(board)
                        condicion = True #The loop ends to spend the next boat.
                elif position == "v":
                    boat_in_vertical = self.no_exist_vertical(board, self.SHIPS, boat, placerow, placecol) #Checks the existence of boats in vertical position and  if they are put off the board.
                    if boat_in_vertical != False: #If true, it means that no ships. Otherwise the loop is repeated again.
                        self.placing_ship_vertical(board, placerow, placecol, boat) #Place the boats.
                        self.clear()
                        self.print_tablero(board)
                        condicion = True #The loop ends to spend the next boat.



    def no_intersection_horizontal(self, board, dict_ship, boat, row_x, col_y):
        """This function checks that the boats are not placed on other boats."""
        count = 0 #This variable stores the count of the string "|   ".

        try:
            for number in range(dict_ship[boat]):
                if "|   " in board[row_x][col_y + number]:
                    count += 1 #When a string "|   " is found, adds 1 to the variable count.
        except: #If an error occurs, an error message is displayed and returns False.
            self.BADDATA.play()
            print ""
            print chr(27) + "[0;91m" + "    ⚠ You can not put the boat in this position. It is off the board." + chr(27) + "[0m"
            print ""
            return False

        if count == dict_ship[boat]: #If the value of "boat" and the value of "count" match, returns True, it means there are no boats.
            return True
        else: #If the values are different, returns False.
            self.SOUNDINVALID.play()
            print ""
            print chr(27) + "[0;91m" + "    ✘ In this position already exists a boat. Try again." + chr(27) + "[0m"
            print ""
            return False 



    def no_exist_vertical(self, board, dict_ship, boat, row_x, col_y):
        """This function checks that the boats are not placed on other boats in vertical position."""
        count = 0 #This variable stores the count of the string "|   ".

        try:
            for number in range(dict_ship[boat]):
                if "|   " in board[row_x + number][col_y]:
                    count += 1 #When a string "|   " is found, adds 1 to the variable count.
        except: #If an error occurs, an error message is displayed and returns False.
            self.BADDATA.play()
            print ""
            print chr(27) + "[0;91m" + "    ⚠ You can not put the boat in this position. It is off the board." + chr(27) + "[0m"
            print ""
            return False

        if count == dict_ship[boat]: #If the value of "boat" and the value of "count" match, returns True, it means there are no boats.
            return True
        else: #If the values are different, returns False.
            self.SOUNDINVALID.play()
            print ""
            print chr(27) + "[0;91m" + "    ✘ In this position already exists a boat. Try again." + chr(27) + "[0m"
            print ""
            return False 



    def placing_ship_horizon(self, board, coordx, coordy, boat):
        """Esta funcion permite colocar los barcos en posición horizontal."""
        try:
            for intento in range(self.SHIPS[boat]):
                board[coordx][coordy + intento] = self.CHARACTER[boat]
        except:
            try:
                for intento in range(self.SHIPS[boat]):
                    board[coordx][coordy + intento] = "|   "
            except:
                print ""
                print "You can not put the boat in this position. It is off the board."
                return False




    def placing_ship_vertical(self, board, coordx, coordy, boat):
        """This function allows you to place the boats upright."""
        try:
            for intento in range(self.SHIPS[boat]):
                board[coordx + intento][coordy] = self.CHARACTER[boat]
        except:
            try:
                for intento in range(self.SHIPS[boat]):
                    board[coordx + intento ][coordy] = "|   "
            except:
                print ""
                print chr(27) + "[0;91m" + "    ⚠ You can not put the boat in this position. It is off the board." + chr(27) + "[0m"
                print ""
                return False



    def user_vertical_horizontal(self):
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
                self.BADDATA.play()
                print ""
                print chr(27) + "[0;91m" + "              ✘ Invalid data!." + chr(27) + "[0m"
                print message_text



    def computer_ships(self):
        """This function places the computer's ships  randomly."""
        self.create(self.BOARDCOMP)
        for boat in self.SHIPS: #Choose one by one the boats in the dictionary to be placed.
            condicion = False
            while condicion == False:
                position = ["v", "h"]
                numb_x = self.random_row(self.BOARDCOMP) ##Chooses row at random.
                numb_y = self.random_col(self.BOARDCOMP) #Chooses column at random.
                positionchoice = random.choice(position) #Chooses position at random.
                if positionchoice == "h":
                    no_boat = self.no_intersection_horizontal(self.BOARDCOMP, self.SHIPS, boat, numb_x, numb_y) #Checks the existence of boats in horizontal position and  if they are put off the board
                    if no_boat != False:
                        self.placing_ship_horizon(self.BOARDCOMP, numb_x, numb_y, boat) #Place the boats.
                        condicion = True
                elif positionchoice == "v":
                    no_boat_vertical = self.no_exist_vertical(self.BOARDCOMP, self.SHIPS, boat, numb_x, numb_y) #Checks the existence of boats in vertical position and  if they are put off the board.
                    if no_boat_vertical != False:
                        self.placing_ship_vertical(self.BOARDCOMP, numb_x, numb_y, boat) #Place the boats.
                        condicion = True


    def entering_number_row(self):
            """Allows the user to enter a row number."""
            while True:
                print ""
                guessrow = raw_input("   >Enter row: ")
                if guessrow == "exit":
                    self.clear()
                    self.limpiar(self.USERBOARD, self.BOARDCOMP, self.VERSUSBOARD, self.PLAYER2, self.HIDEN1, self.HIDEN2)
                    self.first()
                    self.menu()
                    return guessrow
                    break
                else:
                    try:
                        guessrow = int(guessrow)
                        if guessrow >= 1 and guessrow <= 10:
                            self.OPTIONSOUND.play()
                            guessrow -= 1
                            return guessrow
                            break
                        else:
                            self.SOUNDINVALID.play()
                            print ""
                            print chr(27) + "[0;91m" + "     ✘ Please enter numbers in the range of 1 - 10." + chr(27) + "[0m"
                    except:
                        self.BADDATA.play()
                        print ""
                        print chr(27) + "[0;91m" + "     ✘ Please enter numbers!" + chr(27) + "[0m"



    def entering_number_col(self):
        """Allows the user to enter a column number."""
        while True:
            print ""
            guesscol = raw_input("   >Enter column: ")
            if guesscol == "exit":
                self.clear()
                self.limpiar(self.USERBOARD, self.BOARDCOMP, self.VERSUSBOARD, self.PLAYER2, self.HIDEN1, self.HIDEN2)
                self.first()
                self.menu()
                self.exit()
                return guesscol
                break
            else:
                try:
                    guesscol = int(guesscol)
                    if guesscol >= 1 and guesscol <= 10:
                        self.OPTIONSOUND.play()
                        guesscol -= 1
                        return guesscol
                        break
                    else:
                        self.SOUNDINVALID.play()
                        print ""
                        print chr(27) + "[0;91m" + "     ✘ Please enter numbers in the range of 1 - 10." + chr(27) + "[0m"
                except:
                    self.BADDATA.play()
                    print ""
                    print chr(27) + "[0;91m" + "     ✘ Please enter numbers!" + chr(27) + "[0m"



    def statistics(self, board):
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


    def statistics_user(self, board):
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


    def count_damage(self, board):
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
            self.VICTORY.play()

            if board == self.PLAYER2:
                print ""
                print "                     Player 1 wins!"
                print ""

            elif board == self.USERBOARD:
                print ""
                print "                     Player 2 wins!"
                print ""

            elif board == self.BOARDCOMP:
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


    def count_damage_comp(self, board):
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



    def game_alone(self):
        """allows the user to guess where are the enemy ships."""
        self.print_tablero(self.VERSUSBOARD)
        self.statistics(self.BOARDCOMP)
        adivina_row = self.entering_number_row()
        adivina_col = self.entering_number_col()
        self.clear()
        view_board = self.hit_boat(self.BOARDCOMP, self.VERSUSBOARD, adivina_row, adivina_col)
        return view_board



    def game_multiplayer(self, hiden_board, show_board):
        """allows the user to guess where are the enemy ships in a multiplayer session."""
        self.print_tablero(show_board)
        self.statistics(hiden_board)
        adivina_row = self.entering_number_row()
        adivina_col = self.entering_number_col()
        self.clear()
        view_board = self.hit_boat(hiden_board, show_board, adivina_row, adivina_col)
        return view_board



    def computer_turn(self):
        """The computer tries to guess where are the boats."""
        hitrow = self.random_row(self.USERBOARD)
        hitcol = self.random_col(self.USERBOARD)
        view_board = self.hit_boat_computer(self.USERBOARD, hitrow, hitcol)
        return view_board



    def hit_boat_computer(self, board, hitrow, hitcol):
        """This function checks if the computer has impacted."""
        if "|   " in board[hitrow][hitcol]:
            board[hitrow][hitcol] = "| o "
            print "                  Poor shooting!"
            print ""
            self.print_tablero(board)
            self.statistics_user(board)
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
                self.EXPlOSION.play()
                board[hitrow][hitcol] = "| x "
                print "                  Impact!"
                print ""
                self.print_tablero(board)
                insulto = random.choice(self.COMPUTER_INSULTS)
                print ""
                print "   Enemy message: " + str(insulto)
                print ""
                self.statistics_user(board)
                print "   The enemy has impacted your boat."
                time.sleep(0.4)
                self.TAUNTS[insulto].play()
                raw_input("   Press enter...")
                return 1


    def turnos(self):
        """Manage shifts for a single player session."""
        self.create(self.VERSUSBOARD)
        turn = 0
        destruction = False
        while destruction == False:
            if turn == 0:
                self.clear()
                print "                  Your turn"
                print ""
                print ""
                print ""
                turn = self.game_alone()
                destruction = self.count_damage(self.BOARDCOMP)
            elif turn == 1:
                self.clear()
                print "                  Enemy's turn"
                print ""
                turn = self.computer_turn()
                destruction = self.count_damage_comp(self.USERBOARD)



    def turnos_multiplayer(self):
        """Manage shifts for a multi player session."""
        turn = 0
        destruction = False
        while destruction == False:
            if turn == 0:
                self.clear()
                print "                  Shoot Player 1"
                print ""
                print ""
                print ""
                turn = self.game_multiplayer(self.PLAYER2, self.HIDEN2)
                destruction = self.count_damage(self.PLAYER2)
            elif turn == 1:
                self.clear()
                print "                  Shoot Player 2"
                print ""
                print ""
                print ""
                turn = self.game_multiplayer(self.USERBOARD, self.HIDEN1)
                destruction = self.count_damage(self.USERBOARD)



    def hit_boat(self, hiden_board, board, hitrow, hitcol):
        """This function checks the user impacts."""
        if "|   " in hiden_board[hitrow][hitcol]:
            hiden_board[hitrow][hitcol] = "| o "
            board[hitrow][hitcol] = "| o "
            self.clear()
            if hiden_board == self.PLAYER2:
                print "                  Shoot Player 1"
            elif hiden_board == self.USERBOARD:
                print "                  Shoot Player 2"
            else:
                print "                  Your Turn"

            print ""
            print "                  Poor shooting!"
            print ""
            self.print_tablero(hiden_board)
            self.statistics(hiden_board)
            print ""
            print "      You failed"

            if hiden_board == self.PLAYER2:
                print "      It's turn of player 2"
            elif hiden_board == self.USERBOARD:
                print "      It's turn of player 1"
            else:
                print "      It's the enemy's turn!"

            raw_input("      Press enter...")

            if hiden_board == self.USERBOARD:
                return 0
            else:
                return 1

        else:
            if "| o " in hiden_board[hitrow][hitcol]:

                if hiden_board == self.PLAYER2:
                    print "                  Shoot Player 1"
                elif hiden_board == self.USERBOARD:
                    print "                  Shoot Player 2"
                else:
                    print "                  Your Turn"
                print ""
                print "                    Not again!"
                print ""
                self.print_tablero(board)
                self.statistics(hiden_board)
                print ""
                print "   You've already shot that position. Try again."
                raw_input("   Press enter and try again...")

                if hiden_board == self.USERBOARD:
                    return 1
                else:
                    return 0

            elif "| x " in hiden_board[hitrow][hitcol]:

                if hiden_board == self.PLAYER2:
                    print "                  Shoot Player 1"
                elif hiden_board == self.USERBOARD:
                    print "                  Shoot Player 2"
                else:
                    print "                  Your Turn"

                print ""
                print "                    Not again!"
                print ""
                self.print_tablero(board)
                self.statistics(hiden_board)
                print ""
                print "   You've already shot that position. Try again."
                raw_input("   Press enter and try again...")
                if hiden_board == self.USERBOARD:
                    return 1
                else:
                    return 0
            else:
                self.IMPACT.play()
                hiden_board[hitrow][hitcol] = "| x "
                board[hitrow][hitcol] = "| x "

                if hiden_board == self.PLAYER2:
                    print "                  Shoot Player 1"
                elif hiden_board == self.USERBOARD:
                    print "                  Shoot Player 2"
                else:
                    print "                  Your Turn"

                print ""
                print "                  Impact!"
                print ""
                self.print_tablero(board)
                self.statistics(hiden_board)
                print ""
                print "   You've hit the enemy ship!"
                raw_input("   Press enter...")
                if hiden_board == self.USERBOARD:
                    return 1
                else:
                    return 0




    def new_game_single(self):
        """This function asks the user to play again."""
        while True:
            playAgain = raw_input("    Play again? y/n ")
            playAgain = playAgain.lower()
            if playAgain == "y" or playAgain == "yes":
                self.limpiar(self.USERBOARD, self.BOARDCOMP, self.VERSUSBOARD, self.PLAYER2, self.HIDEN1, self.HIDEN2)
                self.clear()
                self.single_secion()
                break
            elif playAgain == "n" or playAgain == "no" or playAgain == "not":
                self.limpiar(self.USERBOARD, self.BOARDCOMP, self.VERSUSBOARD, self.PLAYER2, self.HIDEN1, self.HIDEN2)
                self.clear()
                self.first()
                self.menu()
                break
            else:
                print ""
                print chr(27) + "[0;91m" + "   ✘ Please enter 'y' or 'n' " + chr(27) + "[0m"



    def new_game_multiplayer(self):
        """This function asks the user to play a multiplayer secion again."""
        while True:
            new_game = raw_input("    Play again? y/n ")
            new_game = new_game.lower()
            if new_game == "y" or new_game == "yes":
                selfself.limpiar(self.USERBOARD, self.BOARDCOMP, self.VERSUSBOARD, self.PLAYER2, self.HIDEN1, self.HIDEN2)
                self.clear()
                multiplayer()
                break
            elif new_game == "n" or new_game == "no" or new_game == "not":
                self.limpiar(self.USERBOARD, self.BOARDCOMP, self.VERSUSBOARD, self.PLAYER2, self.HIDEN1, self.HIDEN2)
                self.clear()
                self.first()
                self.menu()
                break
            else:
                print ""
                print chr(27) + "[0;91m" + "   ✘ Please enter 'y' or 'n' " + chr(27) + "[0m"



    def limpiar(self, board1, board2, board3, board4, board5, board6):
        """This function cleans the lists where the boards are contained."""
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



    def multiplayer(self):
        self.loading()
        print ""
        print ""
        print "          Player 1 places your ships"
        print ""
        raw_input("          Press enter to continue...")
        self.clear()
        print "     It's time to deploy your ships."
        print "     Enter the coordinates."
        self.user_decision(self.USERBOARD)
        self.create(self.HIDEN1)
        print ""
        print "         All ships in position."
        raw_input("         Press enter to continue...")
        self.clear()
        print ""
        print "          Player 2 places your ships"
        print ""
        raw_input("         Press enter to continue...")
        self.clear()
        print "     It's time to deploy your ships."
        print "     Enter the coordinates."
        self.user_decision(self.PLAYER2)
        self.create(self.HIDEN2)
        print ""
        print "         All ships in position."
        print "         It's time to fight!"
        print ""
        raw_input("         Press enter to continue...")
        self.clear()
        self.atacar_image()
        time.sleep(2)
        self.clear()
        self.turnos_multiplayer()
        self.new_game_multiplayer()


    def single_secion(self):
        print """
                 
                 
                 
        """
        raw_input("         Press enter to continue...")
        self.clear()
        print ""
        print "     It's time to deploy your ships."
        print "     Enter the coordinates."
        self.user_decision(self.USERBOARD)
        print ""
        print "         All ships in position."
        print ""
        raw_input("         Press enter to continue...")
        self.clear()
        self.computer_ships()
        self.clear()
        self.atacar_image()
        time.sleep(2)
        self.turnos()
        self.new_game_single()

        pass


    def first(self):
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
        self.OTHERVALID.play()
        print chr(27) + "[3;33m" + "   >Press 1 for single player session."
        time.sleep(0.5)
        self.OTHERVALID.play()
        print "   >Press 2 for multiplayer session."
        time.sleep(0.5)
        self.OTHERVALID.play()
        print "   >Press 3 to see the game instructions."
        time.sleep(0.5)
        self.OTHERVALID.play()
        print "   >Press 4 to exit the program." + chr(27) + "[0m"
        time.sleep(0.5)
        print ""
        self.OTHERVALID.play()

    def atacar_image(self):
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


    def image_skull(self):
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



    def loading(self):
        """Function that displays a load message at the start of the game."""
        print """
                                                           
                                                           
                                      |  _  _  _|. _  _    
                                      |_(_)(_|(_||| |(_|...
                                                      _|   """
        time.sleep(2)



    def clear(self):
        """This function clears the screen at the terminal. Works on windows and ubuntu."""
        if os.name == "posix":
            os.system("reset")
        elif os.name == "nt":
            os.system("cls")



    def exit(self):
        os.system("exit")



    def method_exists(self, option):
        dici = {"1": self.single_secion,  "2": self.multiplayer, "3": self.instruccions_single}
        count = 0

        if option == "4":
            return "exit"
        elif option in dici:
            self.clear()
            return dici[option]
        else:
            print ""
            print chr(27) + "[0;91m" + "   ✘ Please enter NUMBERS from 1 to 4." + chr(27) + "[0m"
            print ""
            return self.menu



    def menu(self):
        cosa = False
        while cosa == False:
            option = raw_input(   ">* Choose an option: ")
            cosa = self.method_exists(option)
            if cosa != "exit":
                cosa()
                break
            else:
                sys.exit(0)
                self.exit()
                break



    def instruccions_single(self):
        print chr(27) + "[0;93m" + """

            ____           __                  __  _                     
           /  _/___  _____/ /________  _______/ /_(_)___  ____  _____    
           / // __ \/ ___/ __/ ___/ / / / ___/ __/ / __ \/ __ \/ ___/    
         _/ // / / (__  ) /_/ /  / /_/ / /__/ /_/ / /_/ / / / (__  )     
        /___/_/ /_/____/\__/_/   \__,_/\___/\__/_/\____/_/ /_/____/
""" + chr(27) + "[0m"

        time.sleep(0.1)
        print "        Before the battle you should place the ships on the board."
        time.sleep(0.1)
        print "        The measures of ships are:"
        time.sleep(0.1)

        print chr(27) + "[1;91m" + """
                Ship                          Measure """ + chr(27) + "[0m"
        time.sleep(0.1)
        print chr(27) + "[3;92m" + """
               Aircraft......................5 squares"""
        time.sleep(0.1)
        print "               Battleship....................4 squares"
        time.sleep(0.1)
        print "               Frigate.......................3 squares"
        time.sleep(0.1)
        print "               Submarine.....................3 squares"
        time.sleep(0.1)
        print "               Minesweeper...................2 squares" + chr(27) + "[0m"
        print ""
        time.sleep(0.1)
        print "        Enter the row number and column number where you want to place your boat."
        time.sleep(0.1)
        print "        You must enter numbers in the range of 1 - 10."
        print ""
        time.sleep(0.1)
        print "        You must enter the orientation of your boat. It can be vertical or horizontal."
        time.sleep(0.1)
        print "        You should enter the letter 'V' for vertical, or the letter 'H' for horizontal."
        print ""
        time.sleep(0.1)
        print "        When you hit the enemy ship you get one more chance."
        time.sleep(0.1)
        print "        When the enemy hit your ship, the enemy gets one more chance."
        time.sleep(0.1)
        print "        The game ends when all boats of any opponent, are destroyed."
        time.sleep(0.1)
        print ""
        raw_input(chr(27) + "[3;98m" + "       >Press enter to return to Main Menu... " + chr(27) + "[0m")
        self.clear()
        self.first()
        self.menu()


    def arranque(self):
        self.clear()
        self.image_skull()
        self.loading()
        self.clear()
        pygame.mixer.music.play(-1)
        self.first()
        self.menu()

jugar = battleship()
jugar.arranque()
