from typing import List
from chess.board import Board
from chess.data import PieceColor, Position, position_factory, PieceName, Piece

INITIAL_PAWN_ROW_BY_COLOR = {PieceColor.BLACK: 7, PieceColor.WHITE: 2}


class GameManager:
    board: Board
    current_player = PieceColor.WHITE
    authorized_moves: List[Position] = []
    selected_position: Position = None
    selected_piece: Piece = None

    def __init__(self, board: Board):
        self.board = board

    def get_selected_position(self):
        return self.selected_position

    def get_current_player(self) -> PieceColor:
        return self.current_player

    def get_selected_piece(self) -> Piece:
        return self.selected_piece

    def select_position(self, position: Position):
        self.selected_position = position
        self.selected_piece = self.board.get_piece(self.selected_position)

    def get_authorized_moves(self):
        selected_piece = self.get_selected_piece()
        if selected_piece is None:
            return []
        elif selected_piece.name == PieceName.PAWN:
            return self.manage_pawn_moves()
        elif selected_piece.name == PieceName.NIGHT:
            return self.manage_knight_moves()
        return []

    def manage_pawn_moves(self) -> List[Position]:
        selected_piece = self.get_selected_piece()
        direction = 1 if selected_piece.color == PieceColor.WHITE else -1
        is_initial_position = INITIAL_PAWN_ROW_BY_COLOR[selected_piece.color] == self.selected_position.row
        result = [self.selected_position.offset(row=direction)]
        if is_initial_position: result.append(self.selected_position.offset(row=direction * 2))
        if self.is_offset_position_has_opponent_piece(row=direction, col=1): result.append(
            self.selected_position.offset(row=direction, col=1))
        if self.is_offset_position_has_opponent_piece(row=direction, col=-1): result.append(
            self.selected_position.offset(row=direction, col=-1))
        return result

    def manage_knight_moves(self) -> List[Position]:
        result = []
        self.add_if_offset_position_has_opponent_piece(result=result, row=-1, col=-2)
        self.add_if_offset_position_has_opponent_piece(result=result, row=1, col=-2)
        self.add_if_offset_position_has_opponent_piece(result=result, row=-2, col=-1)
        self.add_if_offset_position_has_opponent_piece(result=result, row=2, col=-1)
        self.add_if_offset_position_has_opponent_piece(result=result, row=-2, col=1)
        self.add_if_offset_position_has_opponent_piece(result=result, row=2, col=1)
        self.add_if_offset_position_has_opponent_piece(result=result, row=-1, col=2)
        self.add_if_offset_position_has_opponent_piece(result=result, row=1, col=2)
        return result

    def add_if_offset_position_has_opponent_piece(self, result: List[Position], row: int, col: int):
        if not self.is_offset_position_has_current_player_piece(row=row, col=col):
            result.append(self.selected_position.offset(row=row, col=col))

    def is_offset_position_has_current_player_piece(self, row: int, col: int) -> bool:
        selected_piece = self.get_selected_piece()
        piece_on_offset_position = self.board.get_piece(self.selected_position.offset(row=row, col=col))
        return piece_on_offset_position is not None and piece_on_offset_position.color == selected_piece.color

    def is_offset_position_has_opponent_piece(self, row: int, col: int) -> bool:
        selected_piece = self.get_selected_piece()
        piece_on_offset_position = self.board.get_piece(self.selected_position.offset(row=row, col=col))
        return piece_on_offset_position is not None and piece_on_offset_position.color != selected_piece.color
