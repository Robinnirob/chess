import unittest

from chess.board import Board, to_piece_positions, board_factory
from chess.data import PieceColor, position_factory, piece_factory, Move


class TestBoard(unittest.TestCase):

    def test_should_return_piece_from_position_when_board_initialized_with_this_piece_in_this_position(self):
        board = board_factory(situation={'a1': 'wp'})
        piece = board.get_piece(position_factory('a1'))
        self.assertEqual('PAWN WHITE', str(piece))

    def test_should_return_white_queen_when_board_default_initialized(self):
        board = board_factory()
        piece = board.get_piece(position_factory('d1'))
        self.assertEqual('QUEEN WHITE', str(piece))

    def test_should_return_black_queen_when_board_default_initialized(self):
        board = board_factory()
        self.assertEqual('QUEEN BLACK', str(board.get_piece(position_factory('d8'))))

    def test_should_get_b7_black_pawn_in_b6_when_moved(self):
        board = board_factory(situation={'b7': 'bp'})
        board.move(Move(position_factory('b7'), position_factory('b6'), piece_factory('bp')))
        self.assertIsNone(board.get_piece(position_factory('b7')))
        self.assertEqual('PAWN BLACK', str(board.get_piece(position_factory('b6'))))


    def test_should_return_no_piece_taken_on_init(self):
        board = board_factory()
        pieces = board.get_pieces_taken(PieceColor.WHITE)
        self.assertEqual([], pieces)

    def test_should_return_no_piece_taken_when_move_not_take_piece(self):
        board = board_factory(situation={'b7': 'bp'})
        board.move(Move(position_factory('b7'), position_factory('b6'), piece_factory('bp')))
        pieces = board.get_pieces_taken(PieceColor.WHITE)
        self.assertEqual([], pieces)

    def test_should_return_piece_taken_when_move_take_piece(self):
        board = board_factory(situation={'b7': 'bp', 'c5': 'wp'})
        board.move(Move(position_factory('b7'), position_factory('c5'), piece_factory('bp')))
        pieces = board.get_pieces_taken(PieceColor.WHITE)
        self.assertEqual([piece_factory('wp')], pieces)


    def test_should_return_all_black_pieces_position(self):
        board = board_factory(situation={'b7': 'bp', 'c5': 'wp'})
        self.assertEqual(to_piece_positions({'b7': 'bp'}), board.get_pieces_position(PieceColor.BLACK))
        self.assertEqual(to_piece_positions({'c5': 'wp'}), board.get_pieces_position(PieceColor.WHITE))


if __name__ == '__main__':
    unittest.main()
