from dataclasses import dataclass
from enum import Enum
from typing import Optional


class PieceColor(Enum):
    BLACK = 0
    WHITE = 1

    def opposite_color(self):
        return PieceColor.BLACK if self == PieceColor.WHITE else PieceColor.WHITE


def piece_color_from_str(value: str) -> PieceColor:
    return PieceColor.BLACK if value == 'b' else PieceColor.WHITE


class PieceName(Enum):
    PAWN = 0
    NIGHT = 1
    BISHOP = 2
    ROOK = 3
    QUEEN = 4
    KING = 5

    def __str__(self):
        if self == PieceName.PAWN:
            return 'p'
        elif self == PieceName.NIGHT:
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
        return PieceName.NIGHT
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
        return chr(self.col + 97) + str(self.row + 1)

    def offset(self, col: int = 0, row: int = 0):
        return Position(self.col + col, self.row + row)

    def belong_to_board(self) -> bool:
        return BOARD_SIZE > self.col >= 0 and BOARD_SIZE > self.row >= 0

    def is_last_position(self, color):
        return (self.row == 7 and color == PieceColor.WHITE) or (self.row == 0 and color == PieceColor.BLACK)


def position_factory(info: str):
    return Position(
        col=ord(info[0]) - ord('a'),
        row=int(info[1]) - 1
    )


@dataclass(frozen=True)
class Piece:
    color: PieceColor
    name: PieceName

    def icon(self):
        return self.name.name[0].upper()

    def __str__(self):
        return f"{self.name.name} {self.color.name}"


@dataclass(frozen=True)
class Move:
    source: Position
    target: Position
    piece_moved: Piece
    piece_taken_position: Optional[Position] = None
    piece_taken: Optional[Piece] = None
    is_two_step_pawn_move: bool = False
    is_left_castling_broken: bool = False
    is_right_casting_broken: bool = False
    is_left_castling: bool = False
    is_right_castling: bool = False


def piece_factory(info: str):
    return Piece(
        color=piece_color_from_str(info[0]),
        name=piece_name_from_str(info[1])
    )


BOARD_SIZE = 8
SQUARE_SIZE = 60

INITIAL_PAWN_ROW_BY_COLOR = {PieceColor.BLACK: 6, PieceColor.WHITE: 1}
INITIAL_KING_ROW_BY_COLOR = {PieceColor.BLACK: 7, PieceColor.WHITE: 0}
