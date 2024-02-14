import unittest

from data import get_chessboard_initialized, Position, position_from_str


class MyTestCase(unittest.TestCase):

    def test_should_have_black_and_white_pieces_on_init(self):
        chessboard = get_chessboard_initialized()
        keys = chessboard.pieces_list.keys()
        self.assertTrue(position_from_str('a1') in keys)
        self.assertTrue(position_from_str('b1') in keys)
        self.assertTrue(position_from_str('c1') in keys)
        self.assertTrue(position_from_str('d1') in keys)
        self.assertTrue(position_from_str('e1') in keys)
        self.assertTrue(position_from_str('f1') in keys)
        self.assertTrue(position_from_str('g1') in keys)
        self.assertTrue(position_from_str('h1') in keys)
        self.assertTrue(position_from_str('a2') in keys)
        self.assertTrue(position_from_str('b2') in keys)
        self.assertTrue(position_from_str('c2') in keys)
        self.assertTrue(position_from_str('d2') in keys)
        self.assertTrue(position_from_str('e2') in keys)
        self.assertTrue(position_from_str('f2') in keys)
        self.assertTrue(position_from_str('g2') in keys)
        self.assertTrue(position_from_str('h2') in keys)
        self.assertTrue(position_from_str('a7') in keys)
        self.assertTrue(position_from_str('b7') in keys)
        self.assertTrue(position_from_str('c7') in keys)
        self.assertTrue(position_from_str('d7') in keys)
        self.assertTrue(position_from_str('e7') in keys)
        self.assertTrue(position_from_str('f7') in keys)
        self.assertTrue(position_from_str('g7') in keys)
        self.assertTrue(position_from_str('h7') in keys)
        self.assertTrue(position_from_str('a8') in keys)
        self.assertTrue(position_from_str('b8') in keys)
        self.assertTrue(position_from_str('c8') in keys)
        self.assertTrue(position_from_str('d8') in keys)
        self.assertTrue(position_from_str('e8') in keys)
        self.assertTrue(position_from_str('f8') in keys)
        self.assertTrue(position_from_str('g8') in keys)
        self.assertTrue(position_from_str('h8') in keys)




if __name__ == '__main__':
    unittest.main()
