import unittest

from chess.board import Board
from chess.data import PieceColor, Position, position_factory
from chess.game_manager import GameManager


class TestManage(unittest.TestCase):
    def test_should_current_player_is_white_on_init(self):
        board = Board(situation={'a1': 'wp'})
        manager = GameManager(board=board)
        self.assertEqual(PieceColor.WHITE, manager.get_current_player())

    def test_should_return_no_move_when_select_position_without_piece(self):
        board = Board(situation={'a2': 'wp'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('a3'))
        self.assertCountEqual([], manager.get_authorized_moves())

    def test_should_return_white_pawn_authorized_moves_when_pawn_has_never_been_moved(self):
        board = Board(situation={'a2': 'wp'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('a2'))
        self.assertCountEqual([position_factory('a3'), position_factory('a4')], manager.get_authorized_moves())

    def test_should_return_white_pawn_authorized_moves_when_pawn_has_moved_once(self):
        board = Board(situation={'a3': 'wp'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('a3'))
        self.assertCountEqual([position_factory('a4')], manager.get_authorized_moves())

    def test_should_return_white_pawn_authorized_moves_when_pawn_has_white_pawn_on_diag(self):
        board = Board(situation={'a3': 'wp', 'b4': 'wp'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('a3'))
        self.assertCountEqual([position_factory('a4')], manager.get_authorized_moves())

    def test_should_return_white_pawn_authorized_moves_when_pawn_has_black_pawn_on_diag(self):
        board = Board(situation={'b3': 'wp', 'c4': 'bp', 'a4': 'bp', })
        manager = GameManager(board=board)
        manager.select_position(position_factory('b3'))
        self.assertCountEqual([position_factory('b4'), position_factory('c4'), position_factory('a4')],
                              manager.get_authorized_moves())

    def test_should_return_white_knight_authorized_moves_when_position_empty(self):
        board = Board(situation={'e4': 'wn'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('e4'))
        self.assertCountEqual([
            position_factory('c3'),
            position_factory('c5'),
            position_factory('d2'),
            position_factory('d6'),
            position_factory('f2'),
            position_factory('f6'),
            position_factory('g3'),
            position_factory('g5')
        ], manager.get_authorized_moves())

    def test_should_return_white_knight_authorized_moves_when_position_filled_with_opponent_piece(self):
        board = Board(situation={
            'e4': 'wn',
            'c3': 'bp',
            'c5': 'bp',
            'd2': 'bp',
            'd6': 'bp',
            'f2': 'bp',
            'f6': 'bp',
            'g3': 'bp',
            'g5': 'bp',
        })
        manager = GameManager(board=board)
        manager.select_position(position_factory('e4'))
        self.assertCountEqual([
            position_factory('c3'),
            position_factory('c5'),
            position_factory('d2'),
            position_factory('d6'),
            position_factory('f2'),
            position_factory('f6'),
            position_factory('g3'),
            position_factory('g5')
        ], manager.get_authorized_moves())

    def test_should_return_white_knight_authorized_moves_when_position_filled_with_current_player_piece(self):
        board = Board(situation={
            'e4': 'wn',
            'c3': 'wp',
            'c5': 'wp',
            'd2': 'wp',
            'd6': 'wp',
            'f2': 'wp',
            'f6': 'wp',
            'g3': 'wp',
            'g5': 'wp',
        })
        manager = GameManager(board=board)
        manager.select_position(position_factory('e4'))
        self.assertCountEqual([], manager.get_authorized_moves())
