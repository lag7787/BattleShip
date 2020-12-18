import sys
import random
from typing import *
from Ship import Ship
from Coordinate import Coordinate
from Orientation import Orientation

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
        
#may be able to condense place_computer_ships and place_user_ships into the same func
def place_computer_ships(gboard: list, ships_dict: dict):
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
                placed_ships.append(ship)
                append_ship(gboard,ship)
                placed = True

def place_user_ships(gboard, ships_dict: dict):

    #get user to input valid coordinates
    #validate coordinates (making sure they're in the board and have no collision)
    #if valid, place the ships
    #should i retreive the ships one at a time? 

    placed_ships = []

    for ship in ships_dict.values():

        placed = False

        while not placed:

            ship_coords = get_coords(ship, len(gboard))
            ship.set_start(ship_coords[0])
            ship.set_end(ship_coords[1])
            ship.set_orientation(ship_coords[2])

            if not collision(ship,placed_ships):
                placed_ships.append(ship)
                append_ship(gboard,ship)
                placed = True
                display(gboard)
            
#need to make sure that our convention of start coord being the smaller one is maintained
def get_coords(ship: Ship, board_size: int):

    flag = True
    prompt_string = f"\nPlease enter valid starting and ending coordiantes (X#:Y#) for a ship of size {ship.size}: "

    while flag:
        
        user_input = input(prompt_string)
        if is_valid(user_input,ship.size, board_size):

           start,end = user_input.split(':')
           start = Coordinate.fromAlpha(start[0],int(start[1]))
           end = Coordinate.fromAlpha(end[0],int(end[1]))
           orientation = Coordinate.get_orientation(start,end)
           flag = False

        else:

            print("Invalid input. Please try agian.")

    return (start,end,orientation)

def append_ship(gboard: list, ship: Ship):

    #only need start code and size 
    #well treat horizontal ships and vertical ships differently
    #can we place in constant time? probably
    #use the start pos as an offset an iterate x times 
    

    if ship.orientation == Orientation.VERTICAL:

        start_index = ship.start_coord.row - 1
        column = ord(ship.start_coord.column) - 65
        
        for offset in range(ship.size):

            gboard[start_index + offset][column] = ship.code


    else:

        start_index = ord(ship.start_coord.column) - 65
        row = ship.start_coord.row - 1

        for offset in range(ship.size):

            gboard[row][start_index + offset] = ship.code

def collision(new_ship: Ship, placed_ships: list) -> bool:

    collision = False
    #print(f"New Attempt:\n{new_ship}")

    for placed_ship in placed_ships: 

        #print(f"checking against:\n{placed_ship}")

        if new_ship.orientation == Orientation.HORIZONTAL and placed_ship.orientation == Orientation.HORIZONTAL:
            #print("both ships are horizontal")
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

        elif new_ship.orientation == Orientation.VERTICAL and placed_ship.orientation == Orientation.VERTICAL:
            #print("both ships are vertical")
    #two cases for overlap in 

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

          #  print("ships have different orientations")

            target_coord = Coordinate()

            vertical_ship = None
            horizontal_ship = None

            if new_ship.orientation == Orientation.VERTICAL:

                vertical_ship = new_ship
                horizontal_ship = placed_ship

            else:

                vertical_ship = placed_ship
                horizontal_ship = new_ship

            target_coord.column = vertical_ship.start_coord.column
            target_coord.row = horizontal_ship.start_coord.row

            #check if target coord in contained within new_ship
            #if they intersect then they both share this coordinate
            #which would be the row of the horizontal ship and col of vertical ship

            if  (target_coord.column == vertical_ship.start_coord.column and \
                vertical_ship.start_coord.row <= target_coord.row and \
                vertical_ship.end_coord.row >= target_coord.row):

                if  (target_coord.row == horizontal_ship.start_coord.row and \
                    horizontal_ship.end_coord.column >= target_coord.column and \
                    horizontal_ship.start_coord.column <= target_coord.column):

                    collision = True
                    break


   # if collision:
   #     print("failed to place ships\n")
   # else:
   #     print("ship placed succesfully\n")

    return collision

def generate_coords(board_size: int, size: int) -> tuple:

    #make a radom choice, representing a selciton beteween two differnet orientations.
    orientation = random.choice([Orientation.VERTICAL,Orientation.HORIZONTAL])

    if orientation == Orientation.HORIZONTAL:

        x1 = random.randrange(1,board_size + 1)
        x2 = x1 + (int(size) - 1)
        
        if x2 > board_size:
            diff = x2 - board_size
            x1 = x1 - diff
            x2 = x2 - diff

        y = random.randrange((board_size // 2) + 1, board_size + 1)

        return (Coordinate(x1,y),Coordinate(x2,y),orientation)

    else:

        y1 = random.randrange((board_size // 2) + 1, board_size + 1) 
        y2 = y1 + (int(size) - 1)

        if y2 > board_size:
            #shoft both of the coordiantes y can be equal to the board size 
            diff = y2 - board_size
            y1 = y1 - diff
            y2 = y2 - diff

        x = random.randrange(1,board_size + 1)

        return (Coordinate(x,y1),Coordinate(x,y2),orientation)

def is_valid(user_input: str,ship_size: int,board_size: int):

    #need to make sure its within the board range and that it fills the number
    #of appropriate spaces

    valid = True

    try:
        start,end = user_input.split(':')
        start = Coordinate.fromAlpha(start[0],int(start[1]))
        end = Coordinate.fromAlpha(end[0],int(end[1]))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return False

    orientation = Coordinate.get_orientation(start,end)
    max_column = chr(board_size + 64)
    min_column = chr(65)
    max_row = board_size // 2
    min_row = 1
    count = 0

    if orientation == Orientation.VERTICAL:


        #checking that its within range

        if start.column < min_column or start.column > max_column:

            valid = False

        elif start.row < min_row or end.row > max_row:

            valid = False

        elif end.row - start.row != (ship_size - 1):

            valid = False
        

    elif orientation == Orientation.HORIZONTAL:

        if start.column < min_column or end.column > max_column:

            valid = False

        elif start.row < min_row or start.row > max_row:

            valid = False

        elif ord(end.column) - ord(start.column) != (ship_size - 1):

            valid = False

    else:
        valid = False


    return valid

def in_available(gboard):

    size = len(gboard)
    rows = [index + 1 for index in range(size // 2, size)]
    cols = [chr(index + 65) for index in range(size)]

    return rows,cols
    
def user_bombing(gameboard):

    rowsAvailable, colsAvailable = in_available(gameboard)
    bombLoc = input('Enter grid location to bomb (e.g., A4): ')
    col, row = bombLoc[0], bombLoc[1:]          
    hit = False

    while (not col.isalpha()) or (not row.isdigit()) or (col not in colsAvailable) or (int(row) not in rowsAvailable) :
        bombLoc = input('Invalid Input. Enter grid location to bomb (e.g., A4): ')
        col, row = bombLoc[0], bombLoc[1:]
        
    if gameboard[int(row) - 1][ord(col) - 65] == '*' :
        print('\n --- NO HIT --- \n')
        
        
    elif str(gameboard[int(row) - 1][ord(col) - 65]) in ['a','b','c','s','d']:                              
        print('\n *** DIRECT HIT *** \n')
        gameboard[int(row) - 1][ord(col) - 65] = ('-'+gameboard[int(row) - 1][ord(col) - 65]+'-')
        hit = True
        
    else:
        print('\n *** ALREADY HIT *** \n')
    
    return hit
        
def computer_bombing(gameboard):
    import random

    computerRowsAvailable = []
    playerRowsAvailable, colsAvailable = in_available(gameboard)
    hit = False

    for element in playerRowsAvailable:
        computerRowsAvailable.append(int(element) - len(gameboard) // 2)
    
    randCol = chr(random.randint(65,len(colsAvailable)+64))
    randRow = random.randint(1,len(computerRowsAvailable) )
       
    if gameboard[int(randRow) - 1][ord(randCol) - 65] in ['a','b','c','d','s']:
       gameboard[int(randRow) - 1][ord(randCol) - 65] = '-'+gameboard[int(randRow) - 1][ord(randCol) - 65]+'-'
       hit = True

    return hit

def is_input(level: str) -> bool:

    #Check if the input is between 1 and 9. If its not, return False, else return true

    try:
        if int(level) >= 0 and int(level) <= 9:
            return True
        else:
            return False
    except:
        return False

def get_input() -> str:

    print("Welcome to Battleship!\n")
    input_str = input("Which level would you like to play on? Levels range between 0-9: ")
    if not is_input(input_str):
        input_str = input("Invalid Input. Please try again: ")

    return input_str

def main():

    ships_dict = {'a' : Ship(5,'a'), 'b': Ship(4,'b'),'c':Ship(3,'c'),'s':Ship(3,'s'),"d":Ship(2,'d')}
    level = int(get_input())
    myGameBoard = gameboard(level)
    place_computer_ships(myGameBoard, ships_dict)
    display(myGameBoard)
    place_user_ships(myGameBoard,ships_dict)
    totalShipSize = 17
    computerShipsHit = 0
    playerShipsHit = 0
    gameover = False

    while not gameover:

        if user_bombing(myGameBoard):
            computerShipsHit += 1

        if computer_bombing(myGameBoard):
            playerShipsHit += 1

        if computerShipsHit == totalShipSize:
            gameover = True
            print("---YOU WIN!---")

        elif playerShipsHit == totalShipSize:
            gameover = True
            print("---YOU LOSE!---")

        display(myGameBoard)


if __name__ == "__main__":
    main()