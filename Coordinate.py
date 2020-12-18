from Orientation import Orientation
class Coordinate:

    def __init__(self,column = 0,row = 0):
        self.column = chr(column + 64)
        self.row = row #numeric datae

    @staticmethod
    def get_orientation(start, end):

        orientation = None

        if start.column == end.column:
            orientation = Orientation.VERTICAL
        elif start.row == end.row:
            orientation = Orientation.HORIZONTAL
        else:
            orientation = Orientation.ERROR

        return orientation



    @classmethod
    def fromAlpha(cls,column,row):
        column = ord(column) - 64
        return cls(column,row)


    def __str__(self):

        return f"({self.column},{self.row})"


        
