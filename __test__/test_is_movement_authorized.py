import unittest

from main import do_movement, is_movement_authorized


class MovementTest(unittest.TestCase):
    def test_should_unauthorize_white_pawn_to_not_move(self):
        actual = is_movement_authorized('P', 'W', 'a3-a3')
        self.assertFalse(actual)

    def test_should_unauthorize_white_pawn_to_move_to_unauthorized_square(self):
        actual = is_movement_authorized('P', 'W', 'a3-a6')
        self.assertFalse(actual)

    def test_should_authorize_white_pawn_to_move_to_the_next_square(self):
        actual = is_movement_authorized('P', 'W', 'a2-a3')
        self.assertFalse(actual)

    def test_should_authorize_white_pawn_to_move_to_2_next_square(self):
        actual = is_movement_authorized('P', 'W', 'a2-a4')
        self.assertFalse(actual)

    def test_should_unauthorize_white_pawn_to_move_to_2_next_square_if_has_already_moved(self):
        actual = is_movement_authorized('P', 'W', 'a3-a5')
        self.assertFalse(actual)



if __name__ == '__main__':
    unittest.main()
