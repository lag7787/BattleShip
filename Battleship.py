import logging
import random

# Luc Garabrant 04/25/2019
#
# This program will simulate battleship.
#

def gameboard(level):
    """
    This function will generate a gameboard, determined by the level size parameter.

    To keep the rows equivalent for both the user and the player, the board_size is 
    guarenteed to be a multiple of two.

    Parameters:
    -----------
    level: required parameter. Level determines the size of the gameboard.
    """

    #To keep the number of rows symmetrical, we need to always increase the board size by a factor of 2
    board_size = 10 + level * 2
    board = []

    #Create each row of the gameboard by iterating through its size.
    for row_index in range(1,board_size + 1):

        #for half of the genereated rows, denote column entries with periods.
        #for the other half, user asterisks. 
        if row_index <= board_size / 2:
            board.append(["."] * board_size)
        else:
            board.append(["*"] * board_size) 

    return(board)

def display(gboard): #this function displays our board
    print()
    row = 1
    boardL = len(gboard)
    for i in range(65,65+boardL):
        if i == 65:
            print(format(' ','^4'),end = '')
        print(format(chr(i),'^4'),end = ' ')
    print()
    print()
    for rowL in gboard:
        print(format(row,'^4'), end ='')
        for col in rowL:
            #if row > boardL // 2:
                #print(format('*','^4'),end = ' ')  #this hides the computer's ships
            #else:
            print(format(col,'^4'),end = ' ')
        if row == boardL // 4 + 1:
            print(format('PLAYER\'S SHIPS','^12'),end = ' ')
        elif row == boardL-(boardL//5):
            print(format('COMPUTER\'S SHIPS','^12'),end = ' ')
        print()
        if row == boardL//2:
            print()
        row +=1
        
def place_computer_ships(gboard: list, ships_dict: dict) -> list:
    """
    The function will randomly place the computer's ships and return the final gameboard to the user.

    git

    """
    return None
   

def isValid(coordinates,gameboard,shiplen):

    alpha = 0
    colonC = 0
    x = len(gameboard)
    maxRow = x // 2
    col = []
    row = []
    for i in range(1,x+1):
        col.append(chr(i+64))
    for i in range(1,x+1):
        row.append(i)
        
    semiC = False
    for i in coordinates:
        if i == ':':
            semiC  = True
            colonC += 1
        elif i.isalpha() == True:
            alpha +=1
            
    if alpha > 2:
        return False
    elif semiC == False or colonC > 1:
        return False        
        
    start, end = coordinates.split(':')
    listCords = [start,end]
    
    
    if len(listCords[0]) < 2 or len(listCords[1]) < 2:
        return False
    elif listCords[0][1:].isdigit() != True:
        return False
    elif listCords[1][1:].isdigit() != True:
        return False
    elif (listCords[0][0] not in col) or (listCords[1][0]not in col) or (int(listCords[0][1:]) not in row) or (int(listCords[1][1:]) not in row) :
        return False
    elif ((int(listCords[1][1:])) - (int(listCords[0][1:])) + 1 != shiplen) and (ord(listCords[1][0]) - (ord(listCords[0][0])) + 1 != shiplen) :
        return False
    elif (listCords[0][0] != listCords[1][0]) and listCords[0][1] != listCords[1][1]:
        return False
    elif int(listCords[0][1:]) > maxRow or int(listCords[1][1]) > maxRow:
        return False
    
    else:
        return True

def inAvailable(board):
    rows = len(board) // 2
    cols = len(board)
    rowsL = []
    colL = []

    for rowNum in range(rows+1,(rows+1)+rows):
        rowsL.append(rowNum)
    for colNum in range(1,cols+1):
        colL.append(chr(colNum+64))

    return rowsL, colL

   
def userbombing(gameboard):

    rowsAvailable, colsAvailable = inAvailable(gameboard)
    
    bombLoc = input('Enter grid location to bomb (e.g., A4): ')
    col, row = bombLoc[0], bombLoc[1:]          

    # not checking for digits and alpha
    
    while (not col.isalpha()) or (not row.isdigit()) or (col not in colsAvailable) or (int(row) not in rowsAvailable) :
        bombLoc = input('Invalid Input.Enter grid location to bomb (e.g., A4): ')
        col, row = bombLoc[0], bombLoc[1:]
        
    
    if gameboard[int(row) - 1][ord(col) - 65] == '*' :
        print('\n --- NO HIT --- \n')
        
        
    elif str(gameboard[int(row) - 1][ord(col) - 65]) in ['a','b','c','s','d']:                              
        print('\n *** DIRECT HIT *** \n')
        gameboard[int(row) - 1][ord(col) - 65] = ('-'+gameboard[int(row) - 1][ord(col) - 65]+'-')
        

    else:
        print('\n *** ALREADY HIT *** \n')
        
        
def computerBombing(gameboard):
    import random

    computerRowsAvailable = []
    playerRowsAvailable, colsAvailable = inAvailable(gameboard)

    for element in playerRowsAvailable:
        computerRowsAvailable.append(int(element)-5)
    
    randCol = chr(random.randint(65,len(colsAvailable)+64))
    randRow = random.randint(1,len(computerRowsAvailable) )
       
    if gameboard[int(randRow) - 1][ord(randCol) - 65] in ['a','b','c','d','s']:
       gameboard[int(randRow) - 1][ord(randCol) - 65] = '-'+gameboard[int(randRow) - 1][ord(randCol) - 65]+'-'
       
    
def playerWin(gameboard):
    
    totalShipSize = 17
    computerShipsHit = 0
    rowStart = len(gameboard) // 2

    for row in gameboard[rowStart:]:
        for element in row:
            if element in ['-a-','-b-','-c-','-d-','-s-']:
                computerShipsHit += 1
                
    if computerShipsHit == totalShipSize:
        return True
    else:
        return False

def computerWin(gameboard):

    totalShipSize = 17
    playerShipsHit = 0
    rowEnd = len(gameboard) // 2

    for row in gameboard[:rowEnd]:
        for element in row:
            if element in ['-a-','-b-','-c-','-d-','-s-']:
                playerShipsHit += 1
                
    if playerShipsHit == totalShipSize:
        return True
    else:
        return False

def is_input(level: str) -> bool:

    #Check if the input is between 1 and 9. If its not, return False, else return true

    try:
        if int(level) >= 0 and int(level) <= 9:
            return True
        else:
            return False
    except:
        return False

def place_ships(ships: list):
    return None


def main():

    logging.basicConfig(level = logging.DEBUG,format = '%(asctime)s - %(levelname)s - %(message)s')

    #Created a dictionary, which will allow me to access data about a ship in constant time.
    ships_dict = {"aircraft carrier":("a",5), "battleship": ("b",4),"cruiser":("c",3),"submarine":("s",3),"destroyer":("d",2)}

    cont = True

    while cont == True:
        
        print('This program will play the game of Battleship against an opponent.\nNine levels of play are provided.\n')
        level = input('Enter level of play (0-9): ')

        while not is_input(level):
            level = input('Invalid input. Enter level of play (0-9): ')

        level = int(level)
        gBoard = gameboard(level)
        place_computer_ships(gBoard),ships_dict)
        display(computerShips)
        
        print("\nEnter the loaction of each ship of specified size (e.g., A1:A5)")

        shiploc = []
        for ship in ships:
            
            placed_without_col = False
            
            while placed_without_col == False:
                
                currentShip = input(ship+' ('+str(shiplen[ships.index(ship)])+'):')
                while not isValid(currentShip,computerShips,shiplen[ships.index(ship)]):                            #may change conditional
                    currentShip = input('Invalid Input.Try again.\n '+ship+' ('+str(shiplen[ships.index(ship)])+'):')
                    
                #initilization of variables
                start, end = currentShip.split(':')
                cordsL = [start,end]
                cShiplen = shiplen[ships.index(ship)]
                cShipCode = shipCode[ships.index(ship)]
                cols = len(computerShips) // 2

                if cordsL[0][0] == cordsL[1][0]:  #if the first letter of each list is the same were placing it verically

                    collision = False

                    for row in computerShips[(int(cordsL[0][1]) - 1):cols]:
                        if row[ord(cordsL[0][0]) - 65] != '.':                                                 #might have to change this later
                            collision = True
                            
                    if not collision:
                        for index in range(int(cordsL[0][1]),int(cordsL[1][1]) + 1):
                            computerShips[index-1][ord(cordsL[0][0]) - 65] = cShipCode
                            
                        placed_without_col = True
                        print(' * ship positioned * ')
                        print()
                    
        
                else:

                    collision = False

                    for item in computerShips[(int(cordsL[0][1])-1)][ord(cordsL[0][0])-65 : (ord(cordsL[1][0]) - 65) + 2]:
                        if item != '.':
                            collision = True

                    if not collision:
                        for index in range(ord(cordsL[0][0]) - 65, (ord(cordsL[1][0]) - 65) + 1 ):
                            computerShips[int(cordsL[0][1]) - 1][index] = cShipCode

                        placed_without_col = True
                        print(' * ship positioned * ')
                        print()
                        
        print('GAME STARTED.....\n')
        display(computerShips)
        gameover = False

        while gameover != True:

            
            userbombing(computerShips)
            computerBombing(computerShips)
            display(computerShips)

        

            if playerWin(computerShips) == True:
                gameover = True
                print(' *** YOU WIN!! *** \n')
                playAgain = input('Would you like to play again(y/n)? ')
                while not playAgain.isalpha() or (playAgain.capitalize() != 'Y' and playAgain.capitalize() != 'N'):
                    playAgain = input('Invalid Input. Would you like to play again(y/n)? ')
                if playAgain.capitalize() == 'N':
                    cont = False
                    
            elif computerWin(computerShips) == True:
                gameover = True
                print(' *** DEFEAT!! *** \n')
                playAgain = input('Would you like to play again(y/n)? ')
                while not playAgain.isalpha() or (playAgain.capitalize() != 'Y' and playAgain.capitalize() != 'N'):
                    playAgain = input('Invalid Input. Would you like to play again(y/n)? ')
                if playAgain.capitalize() == 'N':
                    cont = False
                
            else:
                continue

    print('THANKS FOR PLAYING')
            
                    
                    
if __name__ == "__main__":
    print("Hello, world!")
    main()
        
        
