import unittest

from chess.board import Board
from chess.data import PieceColor, Position, position_factory
from chess.game_manager import GameManager


class TestManage(unittest.TestCase):
    def test_00_should_current_player_is_white_on_init(self):
        board = Board(situation={'a1': 'wp'})
        manager = GameManager(board=board)
        self.assertEqual(PieceColor.WHITE, manager.get_current_player())

    def test_01_should_return_no_move_when_select_position_without_piece(self):
        board = Board(situation={'a2': 'wp'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('a3'))
        self.assertCountEqual([], manager.get_authorized_moves())

    def test_02_should_return_white_pawn_authorized_moves_when_pawn_has_never_been_moved(self):
        board = Board(situation={'a2': 'wp'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('a2'))
        self.assertCountEqual([position_factory('a3'), position_factory('a4')], manager.get_authorized_moves())

    def test_03_should_return_white_pawn_authorized_moves_when_pawn_has_moved_once(self):
        board = Board(situation={'a3': 'wp'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('a3'))
        self.assertCountEqual([position_factory('a4')], manager.get_authorized_moves())

    def test_04_should_return_black_pawn_authorized_moves_when_pawn_has_never_been_moved(self):
        board = Board(situation={'a7': 'bp'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('a7'))
        self.assertCountEqual([position_factory('a6'), position_factory('a5')], manager.get_authorized_moves())

    def test_05_should_return_black_pawn_authorized_moves_when_pawn_has_moved_once(self):
        board = Board(situation={'a6': 'bp'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('a6'))
        self.assertCountEqual([position_factory('a5')], manager.get_authorized_moves())

    def test_06_should_return_white_pawn_authorized_moves_when_pawn_has_white_pawn_on_diag(self):
        board = Board(situation={'a3': 'wp', 'b4': 'wp'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('a3'))
        self.assertCountEqual([position_factory('a4')], manager.get_authorized_moves())

    def test_07_should_return_white_pawn_authorized_moves_when_pawn_has_black_pawn_on_diag(self):
        board = Board(situation={'b3': 'wp', 'c4': 'bp', 'a4': 'bp', })
        manager = GameManager(board=board)
        manager.select_position(position_factory('b3'))
        self.assertCountEqual([position_factory('b4'), position_factory('c4'), position_factory('a4')],
                              manager.get_authorized_moves())

    def test_08_should_not_authorize_white_in_front_position_when_this_position_has_opponent_piece(self):
        board = Board(situation={'b2': 'wp', 'b3': 'bp'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('b2'))
        self.assertCountEqual([], manager.get_authorized_moves())

    def test_09_should_not_authorize_white_in_front_position_when_this_position_has_current_player_piece(self):
        board = Board(situation={'b2': 'wp', 'b3': 'wp'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('b2'))
        self.assertCountEqual([], manager.get_authorized_moves())

    def test_10_should_not_authorize_white_next_to_the_in_front_position_when_this_position_has_opponent_piece(self):
        board = Board(situation={'b2': 'wp', 'b4': 'bp'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('b2'))
        self.assertCountEqual([position_factory('b3')],  manager.get_authorized_moves())

    def test_11_should_not_authorize_white_next_to_the_in_front_position_when_this_position_has_current_player_piece(self):
        board = Board(situation={'b2': 'wp', 'b4': 'wp'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('b2'))
        self.assertCountEqual([position_factory('b3')],  manager.get_authorized_moves())

    def test_12_should_not_authorize_black_in_front_position_when_this_position_has_opponent_piece(self):
        board = Board(situation={'b7': 'bp', 'b6': 'bp'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('b7'))
        self.assertCountEqual([], manager.get_authorized_moves())

    def test_13_should_not_authorize_black_in_front_position_when_this_position_has_current_player_piece(self):
        board = Board(situation={'b7': 'bp', 'b6': 'wp'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('b7'))
        self.assertCountEqual([], manager.get_authorized_moves())

    def test_14_should_not_authorize_black_next_to_the_in_front_position_when_this_position_has_opponent_piece(self):
        board = Board(situation={'b7': 'bp', 'b5': 'bp'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('b7'))
        self.assertCountEqual([position_factory('b6')],  manager.get_authorized_moves())

    def test_15_should_not_authorize_black_next_to_the_in_front_position_when_this_position_has_current_player_piece(self):
        board = Board(situation={'b7': 'bp', 'b5': 'wp'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('b7'))
        self.assertCountEqual([position_factory('b6')],  manager.get_authorized_moves())

    def test_16_should_return_white_knight_authorized_moves_when_position_empty(self):
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

    def test_17_should_return_white_knight_authorized_moves_when_position_filled_with_opponent_piece(self):
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

    def test_18_should_return_white_knight_authorized_moves_when_position_filled_with_current_player_piece(self):
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

    def test_19_should_return_black_knight_authorized_moves_when_position_filled_with_current_player_piece(self):
        board = Board(situation={
            'e4': 'bn',
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
        self.assertCountEqual([], manager.get_authorized_moves())

    def test_20_should_return_rook_authorized_moves_when_position_empty(self):
        board = Board(situation={'e4': 'wr'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('e4'))
        print(str(manager.get_authorized_moves()))
        self.assertCountEqual([
            position_factory('e1'),
            position_factory('e2'),
            position_factory('e3'),
            position_factory('e5'),
            position_factory('e6'),
            position_factory('e7'),
            position_factory('e8'),
            position_factory('a4'),
            position_factory('b4'),
            position_factory('c4'),
            position_factory('d4'),
            position_factory('f4'),
            position_factory('g4'),
            position_factory('h4'),
        ], manager.get_authorized_moves())
    def test_21_should_return_rook_authorized_moves_when_surrounded_by_opponent_pieces(self):
        board = Board(situation={'e4': 'wr', 'e3': 'bp', 'e5': 'bp', 'd4': 'bp', 'f4': 'bp', })
        manager = GameManager(board=board)
        manager.select_position(position_factory('e4'))
        self.assertCountEqual([
            position_factory('e3'),
            position_factory('e5'),
            position_factory('d4'),
            position_factory('f4'),
        ], manager.get_authorized_moves())
    def test_22_should_return_rook_authorized_moves_when_surrounded_by_current_player_pieces(self):
        board = Board(situation={'e4': 'br', 'e3': 'bp', 'e5': 'bp', 'd4': 'bp', 'f4': 'bp', })
        manager = GameManager(board=board)
        manager.select_position(position_factory('e4'))
        self.assertCountEqual([], manager.get_authorized_moves())
