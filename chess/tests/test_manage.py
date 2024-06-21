import unittest

from chess.board import Board, board_factory
from chess.data import PieceColor, Position, position_factory
from chess.game_manager import GameManager


class TestManage(unittest.TestCase):
    def test_00_should_current_player_is_white_on_init(self):
        board = board_factory(situation={})
        manager = GameManager(board=board)
        self.assertEqual(PieceColor.WHITE, manager.get_current_player())

    def test_01_should_return_no_move_when_select_position_without_piece(self):
        board = board_factory(situation={'a2': 'wp'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('a3'))
        self.assertCountEqual([], manager.get_authorized_target_position())

    def test_02_should_return_white_pawn_authorized_moves_when_pawn_has_never_been_moved(self):
        board = board_factory(situation={'a2': 'wp'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('a2'))
        self.assertCountEqual([position_factory('a3'), position_factory('a4')], manager.get_authorized_target_position())

    def test_03_should_return_white_pawn_authorized_moves_when_pawn_has_moved_once(self):
        board = board_factory(situation={'a3': 'wp'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('a3'))
        self.assertCountEqual([position_factory('a4')], manager.get_authorized_target_position())

    def test_04_should_return_black_pawn_authorized_moves_when_pawn_has_never_been_moved(self):
        board = board_factory(situation={'a7': 'bp'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('a7'))
        self.assertCountEqual([position_factory('a6'), position_factory('a5')], manager.get_authorized_target_position())

    def test_05_should_return_black_pawn_authorized_moves_when_pawn_has_moved_once(self):
        board = board_factory(situation={'a6': 'bp'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('a6'))
        self.assertCountEqual([position_factory('a5')], manager.get_authorized_target_position())

    def test_06_should_return_white_pawn_authorized_moves_when_pawn_has_white_pawn_on_diag(self):
        board = board_factory(situation={'a3': 'wp', 'b4': 'wp'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('a3'))
        self.assertCountEqual([position_factory('a4')], manager.get_authorized_target_position())

    def test_07_should_return_black_pawn_authorized_moves_when_en_passant_capture_available(self):
        board = board_factory(situation={'b2': 'wp', 'a4': 'bp', 'c4': 'bp'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('b2'))
        manager.move(position_factory('b4'))
        manager.select_position(position_factory('a4'))
        self.assertCountEqual([position_factory('a3'), position_factory('b3')], manager.get_authorized_target_position())
        manager.select_position(position_factory('c4'))
        self.assertCountEqual([position_factory('c3'), position_factory('b3')], manager.get_authorized_target_position())
        manager.move(position_factory('b3'))
        self.assertIsNone(board.get_piece(position_factory('b4')))

    def test_08_should_return_white_pawn_authorized_moves_when_en_passant_capture_available(self):
        board = board_factory(situation={'b7': 'bp', 'a5': 'wp', 'c5': 'wp'})
        manager = GameManager(board=board, current_player=PieceColor.BLACK)
        manager.select_position(position_factory('b7'))
        manager.move(position_factory('b5'))
        manager.select_position(position_factory('a5'))
        self.assertCountEqual([position_factory('a6'), position_factory('b6')], manager.get_authorized_target_position())
        manager.select_position(position_factory('c5'))
        self.assertCountEqual([position_factory('c6'), position_factory('b6')], manager.get_authorized_target_position())
        manager.move(position_factory('b6'))
        self.assertIsNone(board.get_piece(position_factory('b5')))

    def test_09_should_return_white_pawn_authorized_moves_when_pawn_has_black_pawn_on_diag(self):
        board = board_factory(situation={'b3': 'wp', 'c4': 'bp', 'a4': 'bp', })
        manager = GameManager(board=board)
        manager.select_position(position_factory('b3'))
        self.assertCountEqual([position_factory('b4'), position_factory('c4'), position_factory('a4')],
                              manager.get_authorized_target_position())

    def test_10_should_not_authorize_white_in_front_position_when_this_position_has_opponent_piece(self):
        board = board_factory(situation={'b2': 'wp', 'b3': 'bp'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('b2'))
        self.assertCountEqual([], manager.get_authorized_target_position())

    def test_11_should_not_authorize_white_in_front_position_when_this_position_has_current_player_piece(self):
        board = board_factory(situation={'b2': 'wp', 'b3': 'wp'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('b2'))
        self.assertCountEqual([], manager.get_authorized_target_position())

    def test_12_should_not_authorize_white_next_to_the_in_front_position_when_this_position_has_opponent_piece(self):
        board = board_factory(situation={'b2': 'wp', 'b4': 'bp'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('b2'))
        self.assertCountEqual([position_factory('b3')], manager.get_authorized_target_position())

    def test_13_should_not_authorize_white_next_to_the_in_front_position_when_this_position_has_current_player_piece(
            self):
        board = board_factory(situation={'b2': 'wp', 'b4': 'wp'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('b2'))
        self.assertCountEqual([position_factory('b3')], manager.get_authorized_target_position())

    def test_14_should_not_authorize_black_in_front_position_when_this_position_has_opponent_piece(self):
        board = board_factory(situation={'b7': 'bp', 'b6': 'bp'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('b7'))
        self.assertCountEqual([], manager.get_authorized_target_position())

    def test_15_should_not_authorize_black_in_front_position_when_this_position_has_current_player_piece(self):
        board = board_factory(situation={'b7': 'bp', 'b6': 'wp'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('b7'))
        self.assertCountEqual([], manager.get_authorized_target_position())

    def test_16_should_not_authorize_black_next_to_the_in_front_position_when_this_position_has_opponent_piece(self):
        board = board_factory(situation={'b7': 'bp', 'b5': 'bp'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('b7'))
        self.assertCountEqual([position_factory('b6')], manager.get_authorized_target_position())

    def test_17_should_not_authorize_black_next_to_the_in_front_position_when_this_position_has_current_player_piece(
            self):
        board = board_factory(situation={'b7': 'bp', 'b5': 'wp'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('b7'))
        self.assertCountEqual([position_factory('b6')], manager.get_authorized_target_position())

    def test_18_should_return_white_knight_authorized_moves_when_position_empty(self):
        board = board_factory(situation={'e4': 'wn'})
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
        ], manager.get_authorized_target_position())

    def test_19_should_return_white_knight_authorized_moves_when_position_filled_with_opponent_piece(self):
        board = board_factory(situation={
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
        ], manager.get_authorized_target_position())

    def test_20_should_return_white_knight_authorized_moves_when_position_filled_with_current_player_piece(self):
        board = board_factory(situation={
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
        self.assertCountEqual([], manager.get_authorized_target_position())

    def test_21_should_return_black_knight_authorized_moves_when_position_filled_with_current_player_piece(self):
        board = board_factory(situation={
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
        self.assertCountEqual([], manager.get_authorized_target_position())

    def test_22_should_return_rook_authorized_moves_when_position_empty(self):
        board = board_factory(situation={'e4': 'wr'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('e4'))
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
        ], manager.get_authorized_target_position())

    def test_23_should_return_rook_authorized_moves_when_surrounded_by_opponent_pieces(self):
        board = board_factory(situation={'e4': 'wr', 'e3': 'bp', 'e5': 'bp', 'd4': 'bp', 'f4': 'bp', })
        manager = GameManager(board=board)
        manager.select_position(position_factory('e4'))
        self.assertCountEqual([
            position_factory('e3'),
            position_factory('e5'),
            position_factory('d4'),
            position_factory('f4'),
        ], manager.get_authorized_target_position())

    def test_24_should_return_rook_authorized_moves_when_surrounded_by_current_player_pieces(self):
        board = board_factory(situation={'e4': 'br', 'e3': 'bp', 'e5': 'bp', 'd4': 'bp', 'f4': 'bp', })
        manager = GameManager(board=board)
        manager.select_position(position_factory('e4'))
        self.assertCountEqual([], manager.get_authorized_target_position())

    def test_25_should_return_bishop_authorized_moves_when_position_empty(self):
        board = board_factory(situation={'e4': 'wb'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('e4'))
        self.assertCountEqual([
            position_factory('b1'),
            position_factory('c2'),
            position_factory('d3'),
            position_factory('f5'),
            position_factory('g6'),
            position_factory('h7'),
            position_factory('h1'),
            position_factory('g2'),
            position_factory('f3'),
            position_factory('d5'),
            position_factory('c6'),
            position_factory('b7'),
            position_factory('a8'),
        ], manager.get_authorized_target_position())

    def test_26_should_return_bishop_authorized_moves_when_surrounded_by_opponent_pieces(self):
        board = board_factory(situation={'e4': 'wb', 'd3': 'bp', 'd5': 'bp', 'f3': 'bp', 'f5': 'bp', })
        manager = GameManager(board=board)
        manager.select_position(position_factory('e4'))
        self.assertCountEqual([
            position_factory('d3'),
            position_factory('d5'),
            position_factory('f3'),
            position_factory('f5'),
        ], manager.get_authorized_target_position())

    def test_27_should_return_bishop_authorized_moves_when_surrounded_by_current_player_pieces(self):
        board = board_factory(situation={'e4': 'bb', 'd3': 'bp', 'd5': 'bp', 'f3': 'bp', 'f5': 'bp', })
        manager = GameManager(board=board)
        manager.select_position(position_factory('e4'))
        self.assertCountEqual([], manager.get_authorized_target_position())

    def test_28_should_return_queen_authorized_moves_when_position_empty(self):
        board = board_factory(situation={'e4': 'wq'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('e4'))
        self.assertCountEqual([
            position_factory('b1'),
            position_factory('c2'),
            position_factory('d3'),
            position_factory('f5'),
            position_factory('g6'),
            position_factory('h7'),
            position_factory('h1'),
            position_factory('g2'),
            position_factory('f3'),
            position_factory('d5'),
            position_factory('c6'),
            position_factory('b7'),
            position_factory('a8'),
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
        ], manager.get_authorized_target_position())

    def test_29_should_return_queen_authorized_moves_when_surrounded_by_opponent_pieces(self):
        board = board_factory(
            situation={'e4': 'wq', 'd3': 'bp', 'd5': 'bp', 'f3': 'bp', 'f5': 'bp', 'e3': 'bp', 'e5': 'bp', 'd4': 'bp',
                       'f4': 'bp'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('e4'))
        self.assertCountEqual([
            position_factory('d3'),
            position_factory('e3'),
            position_factory('f3'),
            position_factory('d5'),
            position_factory('e5'),
            position_factory('f5'),
            position_factory('d4'),
            position_factory('f4'),
        ], manager.get_authorized_target_position())

    def test_30_should_return_queen_authorized_moves_when_surrounded_by_current_player_pieces(self):
        board = board_factory(
            situation={'e4': 'bq', 'd3': 'bp', 'd5': 'bp', 'f3': 'bp', 'f5': 'bp', 'e3': 'bp', 'e5': 'bp', 'd4': 'bp',
                       'f4': 'bp', })
        manager = GameManager(board=board)
        manager.select_position(position_factory('e4'))
        self.assertCountEqual([], manager.get_authorized_target_position())

    def test_31_should_return_king_authorized_moves_when_position_empty(self):
        board = board_factory(situation={'e4': 'wk'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('e4'))
        self.assertCountEqual([
            position_factory('d3'),
            position_factory('e3'),
            position_factory('f3'),
            position_factory('d5'),
            position_factory('e5'),
            position_factory('f5'),
            position_factory('d4'),
            position_factory('f4'),
        ], manager.get_authorized_target_position())

    def test_32_should_return_king_authorized_moves_when_surrounded_by_opponent_pieces(self):
        board = board_factory(
            situation={'e4': 'wk', 'd3': 'bn', 'd5': 'bn', 'f3': 'bn', 'f5': 'bn', 'e3': 'bn', 'e5': 'bn', 'd4': 'bn',
                       'f4': 'bn'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('e4'))
        self.assertCountEqual([], manager.get_authorized_target_position())

    def test_33_should_return_king_authorized_moves_when_surrounded_by_current_player_pieces(self):
        board = board_factory(
            situation={'e4': 'bk', 'd3': 'bp', 'd5': 'bp', 'f3': 'bp', 'f5': 'bp', 'e3': 'bp', 'e5': 'bp', 'd4': 'bp',
                       'f4': 'bp', })
        manager = GameManager(board=board)
        manager.select_position(position_factory('e4'))
        self.assertCountEqual([], manager.get_authorized_target_position())

    def test_33_should_return_moves_that_not_let_the_king_threated_when_king_threated(self):
        board = board_factory(
            situation={'e4': 'wk', 'f4': 'wp', 'g6': 'bb'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('f4'))
        self.assertCountEqual([
            position_factory('f5'),
        ], manager.get_authorized_target_position())

    def test_33_should_return_moves_that_not_let_the_king_threated_when_king_not_threated(self):
        board = board_factory(
            situation={'e4': 'wk', 'f5': 'wp', 'g6': 'bb'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('f5'))
        self.assertCountEqual([
            position_factory('g6'),
        ], manager.get_authorized_target_position())

    def test_33_fix_bug_when_threat_is_from_same_color1(self):
        board = board_factory(
            situation={'e4': 'wk', 'f5': 'wp', 'g6': 'wb'})
        manager = GameManager(board=board)
        manager.select_position(position_factory('f5'))
        self.assertCountEqual([
            position_factory('f6'),
        ], manager.get_authorized_target_position())

    def test_34_should_position_not_threated_when_board_empty(self):
        board = board_factory(situation={})
        manager = GameManager(board=board)
        position = position_factory('e4')

        self.assertEqual((set(), {position}), manager.filter_position_threated(board=board, positions=[position], color=PieceColor.WHITE))
        self.assertEqual((set(), {position}), manager.filter_position_threated(board=board, positions=[position], color=PieceColor.BLACK))

    def test_35_should_position_threated_when_pawn_threated_position(self):
        board = board_factory(situation={'d5': 'bp', 'd3': 'wp'})
        manager = GameManager(board=board)
        position = position_factory('e4')
        self.assertEqual(({position}, set()), manager.filter_position_threated(board=board, positions=[position], color=PieceColor.WHITE))
        self.assertEqual(({position}, set()), manager.filter_position_threated(board=board, positions=[position], color=PieceColor.BLACK))

    def test_36_should_position_threated_when_knight_threated_position(self):
        board = board_factory(situation={'d6': 'bn', 'f6': 'wn'})
        manager = GameManager(board=board)
        position = position_factory('e4')
        self.assertEqual(({position}, set()), manager.filter_position_threated(board=board, positions=[position], color=PieceColor.WHITE))
        self.assertEqual(({position}, set()), manager.filter_position_threated(board=board, positions=[position], color=PieceColor.BLACK))

    def test_37_should_position_threated_when_rook_threated_position(self):
        board = board_factory(situation={'e6': 'br', 'a4': 'wr'})
        manager = GameManager(board=board)
        position = position_factory('e4')
        self.assertEqual(({position}, set()), manager.filter_position_threated(board=board, positions=[position], color=PieceColor.WHITE))
        self.assertEqual(({position}, set()), manager.filter_position_threated(board=board, positions=[position], color=PieceColor.BLACK))

    def test_38_should_position_threated_when_bishop_threated_position(self):
        board = board_factory(situation={'f5': 'bb', 'f3': 'wb'})
        manager = GameManager(board=board)
        position = position_factory('e4')
        self.assertEqual(({position}, set()), manager.filter_position_threated(board=board, positions=[position], color=PieceColor.WHITE))
        self.assertEqual(({position}, set()), manager.filter_position_threated(board=board, positions=[position], color=PieceColor.BLACK))

    def test_39_should_position_threated_when_queen_threated_position(self):
        board = board_factory(situation={'e6': 'bq', 'a4': 'wq'})
        manager = GameManager(board=board)
        position = position_factory('e4')
        self.assertEqual(({position}, set()), manager.filter_position_threated(board=board, positions=[position], color=PieceColor.WHITE))
        self.assertEqual(({position}, set()), manager.filter_position_threated(board=board, positions=[position], color=PieceColor.BLACK))

    def test_40_should_position_threated_when_king_threated_position(self):
        board = board_factory(situation={'f5': 'bk', 'f3': 'wk'})
        manager = GameManager(board=board)
        position = position_factory('e4')
        self.assertEqual(({position}, set()), manager.filter_position_threated(board=board, positions=[position], color=PieceColor.WHITE))
        self.assertEqual(({position}, set()), manager.filter_position_threated(board=board, positions=[position], color=PieceColor.BLACK))
