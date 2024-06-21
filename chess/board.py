from typing import Dict, List

from chess.data import Position, Piece, position_factory, piece_factory, PieceColor, Move, PieceName, INITIAL_KING_ROW_BY_COLOR


class Board:
    piece_positions: Dict[Position, Piece]
    pieces_taken: List[Piece]

    def __init__(self, positions: Dict[Position, Piece], pieces_taken: List[Piece] = []):
        self.piece_positions = positions
        self.pieces_taken = pieces_taken

    def copy(self):
        return Board(self.piece_positions.copy(), self.pieces_taken)

    def get_piece(self, position: Position):
        return self.piece_positions[position] if position in self.piece_positions else None

    def move(self, move: Move):
        if move.source not in self.piece_positions:
            raise ValueError(f'No piece found in {move.source} on the board')

        piece = self.piece_positions[move.source]
        if move.piece_taken_position is not None: del self.piece_positions[move.piece_taken_position]
        del self.piece_positions[move.source]
        if move.target in self.piece_positions: self.pieces_taken.append(self.piece_positions[move.target])
        self.piece_positions[move.target] = piece

        if move.is_left_castling:
            del self.piece_positions[Position(col=0, row=INITIAL_KING_ROW_BY_COLOR[piece.color])]
            self.piece_positions[Position(col=3, row=INITIAL_KING_ROW_BY_COLOR[piece.color])] = Piece(piece.color, PieceName.ROOK)

        if move.is_right_castling:
            del self.piece_positions[Position(col=7, row=INITIAL_KING_ROW_BY_COLOR[piece.color])]
            self.piece_positions[Position(col=5, row=INITIAL_KING_ROW_BY_COLOR[piece.color])] = Piece(piece.color, PieceName.ROOK)

    def get_pieces_taken(self, color: PieceColor):
        return [piece for piece in self.pieces_taken if piece.color == color]

    def promote(self, position, piece_name):
        if self.piece_positions[position] is None:
            raise ValueError(f'Position {position} as no piece')
        self.piece_positions[position] = piece_name

    def get_pieces_position(self, color: PieceColor) -> Dict[Position, Piece]:
        return {k: v for k, v in self.piece_positions.items() if v.color == color}

    def get_piece_position_by_name(self, piece_name: PieceName, color: PieceColor) -> List[Position]:
        return [position for position, piece in self.piece_positions.items() if piece.name == piece_name and piece.color == color]


def to_piece_positions(situation: Dict[str, str]) -> Dict[Position, Piece]:
    return {position_factory(k): piece_factory(v) for k, v in situation.items()}


def board_factory(situation: Dict[str, str] = None):
    my_situation = to_piece_positions({
        'a1': 'wr', 'b1': 'wn', 'c1': 'wb', 'd1': 'wq', 'e1': 'wk', 'f1': 'wb', 'g1': 'wn', 'h1': 'wr',
        'a2': 'wp', 'b2': 'wp', 'c2': 'wp', 'd2': 'wp', 'e2': 'wp', 'f2': 'wp', 'g2': 'wp', 'h2': 'wp',
        'a7': 'bp', 'b7': 'bp', 'c7': 'bp', 'd7': 'bp', 'e7': 'bp', 'f7': 'bp', 'g7': 'bp', 'h7': 'bp',
        'a8': 'br', 'b8': 'bn', 'c8': 'bb', 'd8': 'bq', 'e8': 'bk', 'f8': 'bb', 'g8': 'bn', 'h8': 'br'
    }) if situation is None else to_piece_positions(situation)
    return Board(positions=my_situation)
