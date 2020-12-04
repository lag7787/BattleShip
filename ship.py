class Ship:

    def __init__(self,size: int, code: str):
        self.size = size
        self.code = code
        self.start_coord = None
        self.end_coord = None
        self.isHorizontal = None
        self.isVertical = None

    def set_orientation(self,orientation):
        self.isHorizontal = orientation

    def set_start(self,coordinate):
        self.start_coord = coordinate

    def set_end(self,coordinate):
        self.end_coord = coordinate

    def __str__(self):

        output = (f"size: {self.size}\n" +
                 f"code: {self.code}\n" + 
                 f"start coord: {self.start_coord}\n" + 
                 f"end coord: {self.end_coord}\n")

        return output






    



