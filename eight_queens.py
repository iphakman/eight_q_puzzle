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
        self.board = self.board.reshape(self.b_size, self.b_size)
        return self.board

    def set_queen(self, x, y):
        """
        We use this function to set a queen into our board
        :param x: X position
        :param y: Y position
        :return: None
        """
        self.board[x][y] = 1

    def get_value(self, x, y):
        """
        This will check weather a queen is or not at the provided coordinate
        :param x: X position
        :param y: Y positio
        :return: None
        """
        return self.board[x][y]

    def print_board(self):
        """
        This will the board each coordinate
        """
        print(self.board)


def def_queens_pos(ordered, values, directions):
    """
    This will generate a set of coordinates for each n queen
    :param ordered: list of possible values to be added
    :param values: the lst of the coordinates currently in final list
    :param directions: the list of the coordinates for each directions
    :return: set generated with the new coordinates
    """
    result = set()

    a = random.randrange(len(ordered))
    for tmp_lsit in ordered:
        new_co = validate(tmp_lsit, values, directions)
        if new_co:
            result.add(tmp_lsit)
            break

    return result


def validate(nxy, vector, board):
    """
    This will validate if the new coordinate can be added to our results
    :param nxy: X and Y position
    :param vector: Our current coordinates
    :param board: The list of valid directions ( will go through this and validate each one)
    :return: Boolean, if True we will add to our results
    """
    if nxy in vector:
        check = 0
    else:
        check = len((vector))

        # we will loop over board and validate new values aren't in same vector of any other in our current values
        for row in board:
            for row in board:
                for val in vector:
                    if val in row and nxy in row:
                        check -= 1
                        break
                if check < len(vector):
                    return False

            return True


def gen_arrays(s):
    """
    This function will create a list of sets, containing coordinates for each element in the directions
    :param s: we need to pass the size of the square
    :return: this will return the list of vectors created
    """
    my_arrays = []
    # Generating rows and lines
    for x in range(s):
        tmp_arr_x = set()
        tmp_arr_y = set()
        for y in range(s):
            tmp_arr_x.add((x, y))
            tmp_arr_y.add((y, x))
        if tmp_arr_x not in my_arrays:
            my_arrays.append(tmp_arr_x)
        if __name__ == '__main__':
            if tmp_arr_y not in my_arrays:
                my_arrays.append(tmp_arr_y)

    # Adding diagonal lines..
    for cnt in range(s):
        arr_x = set()
        arr_y = set()
        arr_rx = set()
        arr_ry = set()
        x = cnt
        y = 0
        while x < s and y < s:
            arr_x.add((x, y))
            arr_y.add((y, x))
            ry = s - y - 1
            arr_rx.add((x, ry))
            arr_ry.add((x - cnt, ry - cnt))
            x += 1
            y += 1
        if len(arr_x) > 1 and arr_x not in my_arrays:
            my_arrays.append(arr_x)
        if len(arr_y) > 1 and arr_y not in my_arrays:
            my_arrays.append(arr_y)
        if len(arr_rx) > 1 and arr_rx not in my_arrays:
            my_arrays.append(arr_rx)
        if len(arr_ry) > 1 and arr_ry not in my_arrays:
            my_arrays.append(arr_ry)

    return my_arrays


if __name__ == "__main__":
    n = 5

    while n < 4:
        print("We need a value grater than 3, you passed {}".format(n))
        n = int(input("Insert new value:"))

    # Get a list of lists containing our coordinates
    valid = gen_arrays(n)

    results = []
    r_order = valid.copy()
    random.shuffle(r_order)
    print("No valid vectors:", len(valid))

    while len(results) < n and len(r_order) > 0:
        next_list = r_order[0]
        del r_order[0]
        results += def_queens_pos(next_list, results, valid)

    print("My results:", results)

    myBoard = MyBoard(n)
    myBoard.generate_board()

    myBoard.print_board()

