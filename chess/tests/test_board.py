import unittest

from chess.board import Board
from chess.data import Position, PieceName, PieceColor, Piece, position_factory


class TestBoard(unittest.TestCase):

    def test_should_return_piece_from_position_when_board_initialized_with_this_piece_in_this_position(self):
        board = Board(situation={'a1': 'wp'})
        piece = board.get_piece(position_factory('a1'))
        self.assertEqual('PAWN WHITE', str(piece))

    def test_should_return_white_queen_when_board_default_initialized(self):
        board = Board()
        piece = board.get_piece(position_factory('d1'))
        self.assertEqual('QUEEN WHITE', str(piece))

    def test_should_return_black_queen_when_board_default_initialized(self):
        board = Board()
        self.assertEqual('QUEEN BLACK', str(board.get_piece(position_factory('d8'))))

    def test_should_get_b7_black_pawn_in_b6_when_moved(self):
        board = Board(situation={'b7': 'bp'})
        board.move_as_str('b7', 'b6')
        self.assertIsNone(board.get_piece(position_factory('b7')))
        self.assertEqual('PAWN BLACK', str(board.get_piece(position_factory('b6'))))


if __name__ == '__main__':
    unittest.main()
