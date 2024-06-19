import unittest

from chess.board import Board
from chess.data import Position, PieceName, PieceColor, Piece, position_factory


class TestBoard(unittest.TestCase):

    def test_should_return_piece_from_position_when_board_initialized_with_this_piece_in_this_position(self):
        board = Board(situation={'a1': 'wp'})
        piece = board.get_piece(position_factory('a1'))
        self.assert_piece_equals('PAWN WHITE', piece)

    def test_should_return_white_queen_when_board_default_initialized(self):
        board = Board()
        piece = board.get_piece(position_factory('d1'))
        self.assert_piece_equals('QUEEN WHITE', piece)

    def test_should_return_black_queen_when_board_default_initialized(self):
        board = Board()
        piece = board.get_piece(position_factory('d8'))
        self.assert_piece_equals('QUEEN BLACK', piece)

    def assert_piece_equals(self, expected: str, actual: Piece):
        self.assertEqual(expected, str(actual))


if __name__ == '__main__':
    unittest.main()





