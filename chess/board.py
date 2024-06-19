from typing import Dict

from chess.data import Position, Piece, position_factory, piece_factory


class Board:
    piece_positions: Dict[Position, Piece]

    def __init__(self, situation: Dict[str, str] = None):
        self.piece_positions = _to_piece_positions({
            'a1': 'wr', 'b1': 'wn', 'c1': 'wb', 'd1': 'wq', 'e1': 'wk', 'f1': 'wb', 'g1': 'wn', 'h1': 'wr',
            'a2': 'wp', 'b2': 'wp', 'c2': 'wp', 'd2': 'wp', 'e2': 'wp', 'f2': 'wp', 'g2': 'wp', 'h2': 'wp',
            'a7': 'bp', 'b7': 'bp', 'c7': 'bp', 'd7': 'bp', 'e7': 'bp', 'f7': 'bp', 'g7': 'bp', 'h7': 'bp',
            'a8': 'br', 'b8': 'bn', 'c8': 'bb', 'd8': 'bq', 'e8': 'bk', 'f8': 'bb', 'g8': 'bn', 'h8': 'br'
        }) if situation is None else _to_piece_positions(situation)

    def get_piece(self, position: Position):
        return self.piece_positions[position] if position in self.piece_positions else None

    def move(self, source: Position, target: Position):
        if source not in self.piece_positions:
            raise ValueError(f'Source {source} is not in board')

        piece = self.piece_positions[source]
        del self.piece_positions[source]
        self.piece_positions[target] = piece

    def move_as_str(self, source: str, target: str):
        self.move(position_factory(source), position_factory(target))


def _to_piece_positions(situation: Dict[str, str]):
    return {position_factory(k): piece_factory(v) for k, v in situation.items()}
