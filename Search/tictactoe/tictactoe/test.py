import unittest

from tictactoe import *
from util import *

class Tictactoe_Test(unittest.TestCase):

    # Terminal State Tests
    def horizontal_x_win(self):
        self.assertTrue(horizontal_check([[X, X, X],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]], X))

if __name__ == '__main__':
    unittest.main()