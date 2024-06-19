from typing import List
from chess.board import Board
from chess.data import PieceColor, Position, position_factory, PieceName, Piece

INITIAL_PAWN_ROW_BY_COLOR = {PieceColor.BLACK: 7, PieceColor.WHITE: 2}


class GameManager:
    board: Board
    current_player = PieceColor.WHITE
    authorized_moves: List[Position] = []
    selected_position: Position = None

    def __init__(self, board: Board):
        self.board = board

    def get_current_player(self) -> PieceColor:
        return self.current_player

    def get_selected_piece(self) -> Piece:
        return self.board.get_piece(self.selected_position)

    def select_position(self, position: Position):
        self.selected_position = position

    def get_authorized_moves(self):
        selected_piece = self.board.get_piece(self.selected_position)
        if selected_piece is None:
            return []
        elif selected_piece.name == PieceName.PAWN:
            return self.manage_pawn_moves(selected_piece)
        raise ValueError("")

    def manage_pawn_moves(self, selected_piece) -> List[Position]:
        direction = 1 if selected_piece.color == PieceColor.WHITE else -1
        is_initial_position = INITIAL_PAWN_ROW_BY_COLOR[selected_piece.color] == self.selected_position.row
        result = [self.selected_position.offset(row=direction)]
        if is_initial_position: result.append(self.selected_position.offset(row=direction * 2))
        if self.is_offset_position_has_opponent_piece(row=direction, col=1): result.append(self.selected_position.offset(row=direction, col=1))
        if self.is_offset_position_has_opponent_piece(row=direction, col=-1): result.append(self.selected_position.offset(row=direction, col=-1))
        return result

    def is_offset_position_has_opponent_piece(self, row: int, col: int) -> bool:
        piece_on_offset_position = self.board.get_piece(self.selected_position.offset(row=row, col=col))
        return piece_on_offset_position is not None and piece_on_offset_position.color != self.current_player
