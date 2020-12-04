class Coordinate:

    def __init__(self,column = 0,row = 0):
        self.column = chr(column + 64)
        self.row = row #numeric datae


    def __str__(self):

        return f"({self.column},{self.row})"


        
