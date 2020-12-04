import logging
import random
from typing import *
from Ship import Ship
from Coordinate import Coordinate

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

    """
    placed_ships = []

    for ship in ships_dict.values():

        placed = False

        while not placed:

           random_coords = generate_coords(len(gboard),ship.size)
           ship.set_start(random_coords[0])
           ship.set_end(random_coords[1])
           ship.set_orientation(random_coords[2])
           
           if not collision(ship,placed_ships):
                #placeships
                placed_ships.append(ship)
                placed = True


    print("Displaying ships for manual verification: ")
    for ship in placed_ships:
        print(ship)

def collision(new_ship: Ship, placed_ships: list) -> bool:

    collision = False

    for placed_ship in placed_ships: 

        if new_ship.isHorizontal and placed_ship.isHorizontal:
            #check of horizonta collison
            if new_ship.start_coord.row == placed_ship.start_coord.row:

                if new_ship.end_coord.column >= placed_ship.end_coord.column and \
                    new_ship.start_coord.column <= placed_ship.end_coord.column:
                    collision = True
                    break

                elif placed_ship.end_coord.column >= new_ship.end_coord.column and \
                    placed_ship.start_coord.column <= new_ship.end_coord.column:
                    collision = True
                    break

        elif new_ship.isVertical and placed_ship.isVertical:

            if new_ship.start_coord.column == placed_ship.start_coord.column:

                if new_ship.start_coord.row <= placed_ship.start_coord.row and \
                    new_ship.end_coord.row >= placed_ship.start_coord.row:
                    collision = True
                    break
        
                elif placed_ship.start_coord.row <= new_ship.start_coord.row and \
                    placed_ship.end_coord.row >= new_ship.start_coord.row:
                    collision = True
                    break

        else:
            #iterate over all using a dictionary to store 
            #do we know where the interseciton will be? 
            #there is only a single point, which we can locate in constant time 
            #can we check if a cell is in a line in constant time? 
            #yes the coordinates just have to be within the range of both lines

            target_coord = Coordinate()

            vertical_ship = None
            horizontal_ship = None

            if new_ship.isVertical:

                vertical_ship = new_ship
                horizontal_ship = placed_ship

                target_coord.column = new_ship.start_coord.column
                target_coord.row = placed_ship.start_coord.row

            else:

                vertical_ship = placed_ship
                horizontal_ship = vertical_ship

                target_coord.column = placed_ship.start_coord.column
                target_coord.row = new_ship.start_coord.row

            #check if target coord in contained within new_ship

            if not (target_coord.column == vertical_ship.start_coord.column and \
                vertical_ship.start_coord.row <= target_coord.row and \
                vertical_ship.end_coord.row >= target_coord.row):

                collision = True
                break

            elif not (target_coord.row == horizontal_ship.start_coord.row and \
                horizontal_ship.end_coord.column >= target_coord.column and \
                horizontal_ship.start_coord.column <= target_coord.column):

                collision = True
                break

    return collision

def generate_coords(board_size: int, size: int) -> tuple:

    #make a radom choice, representing a selciton beteween two differnet orientations.
    isHorizontal = bool(random.choice([0,1]))

    if isHorizontal:

        x1 = random.randrange(1,board_size + 1)
        x2 = x1 + (int(size) - 1)
        
        if x2 > board_size:
            diff = x2 - board_size
            x1 = x1 - diff
            x2 = x2 - diff

        y = random.randrange((board_size // 2) + 1, board_size + 1)

        return (Coordinate(x1,y),Coordinate(x2,y),isHorizontal)

    else:

        y1 = random.randrange((board_size // 2) + 1, board_size + 1) 
        y2 = y1 + (int(size) - 1)

        #this code can encroach into the opponenets territory

        if y2 > board_size:
            #shoft both of the coordiantes y can be equal to the board size 
            diff = y2 - board_size
            y1 = y1 - diff
            y2 = y2 - diff

        x = random.randrange(1,board_size + 1)

        return (Coordinate(x,y1),Coordinate(x,y2),isHorizontal)

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

    #Create a dictionary of ship objects
    ships_dict = {'a' : Ship(5,'a'), 'b': Ship(4,'b'),'c':Ship(3,'c'),'s':Ship(3,'s'),"d":Ship(2,'d')}

    myGameBoard = gameboard(0)
    display(myGameBoard)

##    for ship in ships_dict.values():
##
##        temp_coords = generate_coords(len(myGameBoard), ship.size)
##        start = temp_coords[0]
##        end = temp_coords[1]
##        orientation = temp_coords[2]
##
##        #print(f"Ship info:\nsize: {ship.size}\ncode: {ship.code}\nstart_pos: {start.column}{start.row}\nend_pos {end.column}{end.row}\nisHoriztonal: {orientation}\n")

    place_computer_ships(myGameBoard, ships_dict)


if __name__ == "__main__":
    main()

    

