#
# Luc Garabrant 04/25/2019
#
# This program will simulate battleship.
#
#
def gameboard(level): #this function creates our initial board
    boardsize = 10 + (level - 1) * 2
    board = []
    for i in range(boardsize):
        rowB = []
        for g in range(boardsize):
            if boardsize // 2 > i:
                rowB.append('.')
            else:
                rowB.append('*')
        board.append(rowB)
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
        
def computerS(gboard):
    
    import random
    shipSize = [5,4,3,3,2]
    shipCode = ['a','b','c','s','d']
    col = len(gboard)
    rowN = (col // 2)
    finalBoard = gboard
    
    for ship in shipCode:
        
        placed = False
        
        while placed == False:
            
            x = random.randint(1,50)
            cordS = []                      #creating a list of two random numbers corresponding to the column numer and row number
            rCol = random.randint(1,col)
            cordS.append(rCol)
            rRow = (random.randint(1,rowN)) + rowN  
            cordS.append(rRow)
            
            if x > 25: #place vertically
                
                availableSpace = finalBoard[cordS[1]-1:]    #checking the space between the first row in our list and the last row (inclusive) since were placing the ship vertically 
                y = len(availableSpace)

                  
                if (y) == shipSize[shipCode.index(ship)]:  #check if our available space is equal to the current ship size that were on. 

                    collision = False         # if so create a variable to check for collision. 
                    
                    for tRow in finalBoard[cordS[1]-1:]:    # for each row in the available space
                            
                            if tRow[rCol-1] != '*':             # check if the item representing the column number in the list is empty
                                    collision = True            # if it is not empty, we have collision. 
                                
                                
                    if not collision:                           # if we done have collision, place our ship and iterate to the next ship.
                        for i in range(cordS[1],col+1):
                            finalBoard[i-1][rCol-1] = ship
                            
                        placed = True
                
                    else:
                        continue


            else:       #place horizontally
                
                 availableSpace = finalBoard[cordS[1]-1][cordS[0]-1:]   #calculate the amount of avilable space from our start index till the end. 
                 y = len(availableSpace)
                
                 if (y) == shipSize[shipCode.index(ship)]:
                     
                    collision = False

                    for item in finalBoard[cordS[1]-1][cordS[0]-1:]: #checking each item in our row to see if its empty. 

                        if item != '*':
                            collision = True

                    if collision != True:
                        for i in range(cordS[0],col+1):
                            finalBoard[cordS[1]-1][i-1] = ship

                        placed = True
                        
                    else:
                        continue         
                
    return(finalBoard)

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
                


def main():
    ships = ['aircraft carrier','battleship','cruiser','submarine','destroyer']
    shipCode = ['a','b','c','s','d']
    shiplen = [5,4,3,3,2]
    cont = True

    while cont == True:
        
        print('This program will play the game of Battleship against an opponent.\nNine levels of play are provided.')
        print()
        level = input('Enter level of play (1-9): ')
        while not level.isdigit() or int(level)<1 or int(level)>9:
            level = input('Invalid input. Enter level of play (1-9): ')
        level = int(level)
        gBoard = gameboard(level)
        computerShips = computerS(gBoard)
        display(computerShips)
        
        print()
        print('Enter the loaction of each ship of specified size (e.g., A1:A5)')

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
            
                    
                    

        
        
