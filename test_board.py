import unittest, random
from eight_queens import MyBoard, gen_arrays, validate, def_queens_pos


class BoardTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(BoardTest, self).__init__(*args, **kwargs)
        self.sqr_size = random.randrange(4, 10)

        self.board = MyBoard(self.sqr_size)
        self.board.generate_board()
        self.test_set = [{0, 0}]

        self.my_array = gen_arrays(self.sqr_size)

    def test_board(self):
        self.assertEqual(self.board.get_value(self.sqr_size - 1, self.sqr_size - 1), 0)

    def test_board_fail(self):
        myError = "Index {0} is out of bound for axis 0 with size {0}".format(self.sqr_size)

        with self.assertRaises(IndexError) as idxErr:
            self.board.get_value(self.sqr_size, self.sqr_size)
        self.assertEqual(myError, str(idxErr.exception))

    def test_validate_false_diag(self):
        self.assertFalse(validate({self.sqr_size - 1, self.sqr_size - 1}, self.test_set, self.my_array))

    def test_validate_false_row(self):
        self.assertFalse(validate({0, self.sqr_size - 1}, self.test_set, self.my_array))

    def test_validate_false_col(self):
        self.assertFalse(validate({self.sqr_size - 1, 0}, self.test_set, self.my_array))

    def test_validate(self):
        self.assertTrue(validate({self.sqr_size + 2, self.sqr_size}, self.test_set, self.my_array))

    def test_array_size(self):
        self.assertEqual(len(self.my_array), (self.sqr_size - 1) + 6)

    def test_put_queens(self):
        array_order = [x for x in self.my_array]
        res_test = []
        count = 0
        while len(res_test) < self.sqr_size and count < len(array_order):
            res_test += def_queens_pos(array_order, res_test, self.my_array)
            count += 1

        error_msg = "This coordinates can'g be fullfil with {} queens.\n{}".format(self.sqr_size, res_test)
        self.assertEqual(len(res_test), self.sqr_size, msg=error_msg)

    def test_get_queens(self):
        count = 0
        while count < self.sqr_size:
            self.board.set_queen(count, count)
            count += 1

        while count > 0:
            count -= 1
            self.assertEqual(self.board.get_value(count, count), 1)


if __name__ == "__init__":
    unittest.main()
