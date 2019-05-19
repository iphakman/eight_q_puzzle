import unittest, random
from eight_q_puzzle import MyBoard


class BoardTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(BoardTest, self).__init__(*args, **kwargs)
        self.sqr_size = random.randrange(4, 10)

        self.board = MyBoard(self.sqr_size)
        self.board.generate_board()


if __name__ == "__init__":
    unittest.main()
