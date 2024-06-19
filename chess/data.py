from dataclasses import dataclass
from enum import Enum

BOARD_SIZE = 8


class PieceColor(Enum):
    BLACK = 0
    WHITE = 1


def piece_color_from_str(value: str) -> PieceColor:
    return PieceColor.BLACK if value == 'b' else PieceColor.WHITE


class PieceName(Enum):
    PAWN = 0
    KNIGHT = 1
    BISHOP = 2
    ROOK = 3
    QUEEN = 4
    KING = 5

    def __str__(self):
        if self == PieceName.PAWN:
            return 'p'
        elif self == PieceName.KNIGHT:
            return 'n'
        elif self == PieceName.BISHOP:
            return 'b'
        elif self == PieceName.ROOK:
            return 'r'
        elif self == PieceName.QUEEN:
            return 'q'
        elif self == PieceName.KING:
            return 'k'


def piece_name_from_str(value: str):
    if value == 'p':
        return PieceName.PAWN
    elif value == 'n':
        return PieceName.KNIGHT
    elif value == 'b':
        return PieceName.BISHOP
    elif value == 'r':
        return PieceName.ROOK
    elif value == 'q':
        return PieceName.QUEEN
    elif value == 'k':
        return PieceName.KING
    raise ValueError(f'{value} is not a valid piece name')

@dataclass(frozen=True)
class Position:
    col: int
    row: int

    def __str__(self):
        return chr(self.col + 97) + str(self.row)

    def offset(self, col: int = 0, row: int = 0):
        return Position(self.col + col, self.row + row)


def position_factory(info: str):
    return Position(
        col=ord(info[0]) - ord('a'),
        row=int(info[1])
    )


@dataclass(frozen=True)
class Piece:
    color: PieceColor
    name: PieceName

    def __str__(self):
        return f"{self.name.name} {self.color.name}"


def piece_factory(info: str):
    return Piece(
        color=piece_color_from_str(info[0]),
        name=piece_name_from_str(info[1])
    )
