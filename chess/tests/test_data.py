import unittest

from chess.data import position_factory


class TestPosition(unittest.TestCase):

    def test_serialization_deserialization(self):
        self.assertEqual('a1', str(position_factory('a1')))
