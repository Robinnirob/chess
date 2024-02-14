from enum import Enum
from typing import Dict, List

from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    col: int
    row: int

    def to_string(self):
        col_as_str = chr(ord('a') + self.col)
        return f"{col_as_str}{self.row}"

    @classmethod
    def from_str(cls, position_as_str):
        col = ord(position_as_str[0]) - ord("a")
        row = int(position_as_str[1:])
        return Position(col, row)


@dataclass(frozen=True)
class Movement:
    init: Position
    target: Position

    def to_string(self):
        return f"{self.init.to_string()}-{self.target.to_string()}"

    @classmethod
    def from_str(cls, movement_as_str: str):
        movement = movement_as_str.split('-')
        return Movement(
            init=Position.from_str(movement[0]),
            target=Position.from_str(movement[1])
        )

    @classmethod
    def from_strs(cls, init, target):
        return Movement(
            init=Position.from_str(init),
            target=Position.from_str(target)
        )


class PieceType(Enum):
    KING = 'K'
    QUEEN = 'Q'
    ROOKS = 'R'
    BISHOPS = 'B'
    KNIGHTS = 'N'
    PAWN = 'P'

    @classmethod
    def from_str(cls, type_as_str):
        if type_as_str == 'K':
            return PieceType.KING
        elif type_as_str == 'Q':
            return PieceType.QUEEN
        elif type_as_str == 'R':
            return PieceType.ROOKS
        elif type_as_str == 'B':
            return PieceType.BISHOPS
        elif type_as_str == 'N':
            return PieceType.KNIGHTS
        elif type_as_str == 'P':
            return PieceType.PAWN
        raise Exception('Unknown piece type')


class Color(Enum):
    WHITE = 'W'
    BLACK = 'B'

    def toLabel(self):
        if self == Color.WHITE:
            return 'Blanc'
        elif self == Color.BLACK:
            return 'Noir'
        raise Exception(f'Unknown color {self.value}')

    @classmethod
    def from_str(cls, color_str):
        if color_str == 'W':
            return Color.WHITE
        elif color_str == 'B':
            return Color.BLACK
        raise Exception('Unknown color')


@dataclass
class PieceInfo:
    type: PieceType
    color: Color
    position: Position

    @classmethod
    def from_str(cls, type_as_str, color_as_str, position_as_str):
        return PieceInfo(
            PieceType.from_str(type_as_str),
            Color.from_str(color_as_str),
            Position.from_str(position_as_str)
        )


@dataclass
class Chessboard:
    pieces_list: dict[Position, PieceInfo]

    def to_string(self):
        pieces_str = ""
        for piece in self.pieces_list.values():
            pieces_str += f"{piece.type.value},{piece.color.value},{piece.position.to_string()};"
        return pieces_str

    @classmethod
    def from_str(cls, pieces_as_str: str):
        result = {}
        for item in pieces_as_str.split(';'):
            if item.strip() != "":
                type, color, position = item.split(',')
                piece = PieceInfo.from_str(type, color, position)
                result[piece.position] = piece
        return Chessboard(result)

    @classmethod
    def from_tuples(cls, list: List[tuple]):
        result = {}
        for item in list:
            piece = PieceInfo.from_str(item[0], item[1], item[2])
            result[piece.position] = piece
        return Chessboard(result)


def get_chessboard_initialized():
    return Chessboard.from_tuples([
        ('R', 'W', 'a1'),
        ('N', 'W', 'b1'),
        ('B', 'W', 'c1'),
        ('Q', 'W', 'd1'),
        ('K', 'W', 'e1'),
        ('B', 'W', 'f1'),
        ('N', 'W', 'g1'),
        ('R', 'W', 'h1'),
        ('P', 'W', 'a2'),
        ('P', 'W', 'b2'),
        ('P', 'W', 'c2'),
        ('P', 'W', 'd2'),
        ('P', 'W', 'e2'),
        ('P', 'W', 'f2'),
        ('P', 'W', 'g2'),
        ('P', 'W', 'h2'),
        ('P', 'B', 'a7'),
        ('P', 'B', 'b7'),
        ('P', 'B', 'c7'),
        ('P', 'B', 'd7'),
        ('P', 'B', 'e7'),
        ('P', 'B', 'f7'),
        ('P', 'B', 'g7'),
        ('P', 'B', 'h7'),
        ('R', 'B', 'a8'),
        ('N', 'B', 'b8'),
        ('B', 'B', 'c8'),
        ('Q', 'B', 'd8'),
        ('K', 'B', 'e8'),
        ('B', 'B', 'f8'),
        ('N', 'B', 'g8'),
        ('R', 'B', 'h8'),
    ])
