import database_connection as dbc
import numpy as np
import random, os
import psycopg2


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


def get_solutions():
    pass


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
    full_coordinates = []
    my_arrays = []
    # Generating rows and lines
    for x in range(s):
        tmp_arr_x = set()
        tmp_arr_y = set()
        for y in range(s):
            full_coordinates.append((x, y))
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

    return my_arrays, full_coordinates


def get_db_values(b_size):
    """
    This functions will get all possibilities based on the size
    :param b_size: size of the board
    :return: list of positions list
    """
    vector_arr = []

    conn = None
    try:
        params = dbc.config()
        print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        print('Select query:')
        cur.execute("SELECT * FROM public.vectors")

        tmp_list = []
        for row in cur.fetchall:
            cnt = 0
            while cnt <= b_size:
                tmp_list.append(row[cnt])
                cnt += 1
            vector_arr.append(tmp_list)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

    return vector_arr


def insert_into(b_size, coordinates):
    """
    This function will insert a possible solutions for our square
    :param coordinates: the list of lists contains coordinates for each queen
    :return: None
    """
    columns = ""
    values = "{}".format(b_size)
    # values = [b_size]
    val = ""
    for x, y in coordinates:
        values += (", '{}, {}'".format(x, y))
        val += ", %s"

    for c in range(1, b_size + 1):
        columns += "vector{},".format(c)

    # INSERT into VECTORS (size, """ + columns[:-1] + """) values (%s""" + val + """)"""
    query_insert = """INSERT into cuenca.VECTORS (size, """ + columns[:-1] + """) values (""" + values + """)"""

    print(query_insert)
    insert = input("> ")

    if insert == 'Y':
        conn = None
        try:
            params = dbc.config()

            print("Connecting to the PostgreSQL database...")
            conn = psycopg2.connect(**params)

            cur = conn.cursor()

            print('Insert query:')
            cur.execute(query_insert)

            db_version = cur.fetchone()
            print(db_version)

            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')
    else:
        print("Nothing to insert...")


def insert_record(array_result, res_file):
    res = ""
    array_result.sort()
    for k in array_result:
        res += "{}|".format(k)
    insert = True
    if res[:-1] in open(res_file).read():
        insert = False
    if insert:
        fn = open(res_file, 'a+')
        fn.write(res[:-1])
        fn.write('\n')
        fn.close()


def get_full_poss(values, chk, board, c, file_name):
    values_org = values[:]
    for row in board:
        for coord in row:
            if coord in chk:
                continue
            else:
                chk.append(coord)
                test = validate(coord, values, board)
                if test:
                    values.append(coord)
                    if len(values) == c:
                        print(values)
                        insert_record(values, file_name)
                        values = values_org[:]
                    else:
                        get_full_poss(values, values, board, c, file_name)
                else:
                    values = values_org[:]


def get_all_possibilities(c, val, values, val_checked, board, file_name):
    origin_values = values[:]
    for row in board:
        print("CHECK ROW:", row)
        if len(values) > 0:
            if val in row:
                continue
            else:
                for coord in row:
                    if coord not in val_checked:
                        val_checked.append(coord)
                        new_co = validate(coord, values, board)
                        if new_co:
                            values.append(coord)
                            if len(values) == c:
                                res = ""
                                values.sort()
                                for k in values:
                                    res += "{}|".format(k)
                                insert = True
                                if res[:-1] in open(file_name).read():
                                    insert = False
                                if insert:
                                    fn = open(file_name, 'a+')
                                    fn.write(res[:-1])
                                    fn.write('\n')
                                    fn.close()
                            else:
                                try:
                                    values += get_all_possibilities(c, coord, values, val_checked, board, file_name)
                                except TypeError as myerror:
                                    print("These positions aren't suitable.", myerror, values)
                    values = origin_values[:]
        else:
            values.append(val)
            continue


if __name__ == "__main__":
    n = 4

    while n < 4:
        print("We need a value grater than 3, you passed {}".format(n))
        n = int(input("Insert new value:"))

    filename = os.path.join('output', 'coordinates_full_list.csv')
    print(filename)

    # Get a list of lists containing valid coordinates
    valid, all_coordinates = gen_arrays(n)

    # To get all possibilities
    arr = valid[0]

    for g in all_coordinates:
        results = [g]
        checked = []
        print("#### checking for {}".format(g))
        # get_all_possibilities(n, g, results, checked, valid, filename)

        get_full_poss(results, checked, valid, n, filename)

    # #######################################################################
    # This will provide us a single board and print with the queens position.
    # rows = get_db_values(n)
    # for r in rows:
    #     print(r)
    # Generate a board...
    # r_order = valid.copy()
    # random.shuffle(r_order)
    # print("Number valid vectors:", len(valid))
    #
    # while len(results) < n and len(r_order) > 0:
    #     next_list = r_order[0]
    #     del r_order[0]
    #     results += def_queens_pos(next_list, results, valid)
    #
    # print("My results:", results)
    #
    # myBoard = MyBoard(n)
    # myBoard.generate_board()
    #
    # for x, y in results:
    #     myBoard.set_queen(x, y)
    #
    # myBoard.print_board()

    # To insert values:
    # results = [(1, 2), (4, 1), (2, 0), (0, 4), (3, 3)]
    # insert_into(n, results)
