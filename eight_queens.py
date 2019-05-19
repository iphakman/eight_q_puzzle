import numpy as np
import random


class MyBoard:
    """
    This Class will create the shape of the board.
    We pass the size when we instantiate
    """

    def __init__(self, b_size):
        self.b_size = b_size
        self.board = np.stack([0])

    def generate_board(self):
        self.board = np.stack([0 for x in range(self.b_size * self.b_size)])
        self.board = self.board.reshapt(self.b_size, self.b_size)
        return self.board

    def print_board(self):
        """
        This will the board each coordinate
        """
        print(self.board)


if __name__ == "__main__":
    n = 5

    while n < 4:
        print("We need a value grater than 3, you passed {}".format(n))
        n = int(input("Insert new value:"))

    valid = gen_arrays(n)

    myBoard = MyBoard(n)
    myBoard.generate_board()
    myBoard.print_board()

