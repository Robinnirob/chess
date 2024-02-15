import unittest
from typing import List

from data import PieceInfo, Movement, Chessboard, Color
from main import is_movement_authorized


class MovementTest(unittest.TestCase):
    def test_should_unauthorize_white_pawn_to_not_move(self):
        move, piece, chessboard = self.init(init_pos='a3', target_pos='a3')
        actual = is_movement_authorized(piece, move, chessboard)
        self.assertFalse(actual)

    def test_should_unauthorize_white_pawn_to_move_to_unauthorized_square(self):
        move, piece, chessboard = self.init(init_pos='a3', target_pos='a6')
        actual = is_movement_authorized(piece, move, chessboard)
        self.assertFalse(actual)

    def test_should_authorize_white_pawn_to_move_to_the_next_square(self):
        move, piece, chessboard = self.init(init_pos='a2', target_pos='a3')
        actual = is_movement_authorized(piece, move, chessboard)
        self.assertTrue(actual)

    def test_should_authorize_white_pawn_to_move_to_2_next_square(self):
        move, piece, chessboard = self.init(init_pos='a2', target_pos='a4')
        actual = is_movement_authorized(piece, move, chessboard)
        self.assertTrue(actual)

    def test_should_unauthorize_white_pawn_to_move_to_2_next_square_if_has_already_moved(self):
        move, piece, chessboard = self.init(init_pos='a3', target_pos='a5')
        actual = is_movement_authorized(piece, move, chessboard)
        self.assertFalse(actual)

    def test_should_unauthorize_white_pawn_to_eat_right_diag_if_no_enemy_piece_present(self):
        move, piece, chessboard = self.init(init_pos='a3', target_pos='b4')
        actual = is_movement_authorized(piece, move, chessboard)
        self.assertFalse(actual)

    def test_should_authorize_white_pawn_to_eat_right_diag_if_enemy_piece_present(self):
        move, piece, chessboard = self.init(init_pos='a3', target_pos='b4', enemy_positions=['b4'])
        actual = is_movement_authorized(piece, move, chessboard)
        self.assertTrue(actual)

    def test_should_unauthorize_white_pawn_to_advance_if_enemy_is_over(self):
        move, piece, chessboard = self.init(init_pos='a3', target_pos='a4', enemy_positions=['a4'])
        actual = is_movement_authorized(piece, move, chessboard)
        self.assertFalse(actual)

    def test_should_authorize_white_pawn_to_advance_if_enemy_is_2_square_over(self):
        move, piece, chessboard = self.init(init_pos='g4', target_pos='g5', enemy_positions=['g6'])
        actual = is_movement_authorized(piece, move, chessboard)
        self.assertTrue(actual)

    def test_should_authorize_white_pawn_to_capture_en_passant(self):
        move, piece, chessboard = self.init(init_pos='a5', target_pos='b6', hystory=['b7-b5'])
        actual = is_movement_authorized(piece, move, chessboard)
        self.assertTrue(actual)


    def init(self, type='P', color='W', init_pos='a3', target_pos='a3', enemy_positions: List[str] = []):
        piece = PieceInfo.from_str(type, color, init_pos)
        other_color = Color.BLACK if piece.color == Color.WHITE else Color.WHITE
        other_pieces = [PieceInfo.from_str('P', other_color.value, position) for position in enemy_positions]
        move = Movement.from_str(f'{init_pos}-{target_pos}')

        pieces_list = {_piece.position: _piece for _piece in other_pieces}
        pieces_list[piece.position] = piece

        chessboard = Chessboard(pieces_list=pieces_list)
        return move, piece, chessboard


if __name__ == '__main__':
    unittest.main()
