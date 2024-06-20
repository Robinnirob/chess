from typing import List, Optional

from chess.board import Board
from chess.data import PieceColor, Position, PieceName, Piece

INITIAL_PAWN_ROW_BY_COLOR = {PieceColor.BLACK: 6, PieceColor.WHITE: 1}


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

    def do_action(self, position: Position):
        is_move_action = position in self.get_authorized_moves() and self.get_selected_piece().color == self.current_player
        if is_move_action:
            self.move(position)
        else:
            self.select_position(position)

    def move(self, position):
        self.board.move(source=self.get_selected_position(), target=position)
        self.select_position(None)
        self.current_player = PieceColor.BLACK if self.current_player == PieceColor.WHITE else PieceColor.WHITE

    def select_position(self, position: Optional[Position]):
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
        elif selected_piece.name == PieceName.ROOK:
            return self.manage_rook_moves()
        elif selected_piece.name == PieceName.BISHOP:
            return self.manage_bishop_moves()
        elif selected_piece.name == PieceName.QUEEN:
            return self.manage_queen_moves()
        elif selected_piece.name == PieceName.KING:
            return self.manage_king_moves()
        raise ValueError(f"Unknown piece {selected_piece}")

    def manage_pawn_moves(self) -> List[Position]:
        selected_piece = self.get_selected_piece()
        direction = 1 if selected_piece.color == PieceColor.WHITE else -1
        is_initial_position = INITIAL_PAWN_ROW_BY_COLOR[selected_piece.color] == self.selected_position.row
        result = []
        self.add_if_offset_position_has_no_piece(result=result, row=direction)
        if is_initial_position: self.add_if_offset_position_has_no_piece(result=result, row=direction * 2)
        self.add_if_offset_position_has_opponent_piece(result=result, row=direction, col=1)
        self.add_if_offset_position_has_opponent_piece(result=result, row=direction, col=-1)
        return result

    def manage_knight_moves(self) -> List[Position]:
        result = []
        self.add_if_offset_position_has_not_current_color_piece(result=result, row=-1, col=-2)
        self.add_if_offset_position_has_not_current_color_piece(result=result, row=1, col=-2)
        self.add_if_offset_position_has_not_current_color_piece(result=result, row=-2, col=-1)
        self.add_if_offset_position_has_not_current_color_piece(result=result, row=2, col=-1)
        self.add_if_offset_position_has_not_current_color_piece(result=result, row=-2, col=1)
        self.add_if_offset_position_has_not_current_color_piece(result=result, row=2, col=1)
        self.add_if_offset_position_has_not_current_color_piece(result=result, row=-1, col=2)
        self.add_if_offset_position_has_not_current_color_piece(result=result, row=1, col=2)
        return result

    def manage_rook_moves(self):
        result = []
        for row_offset in range(1, 8):
            has_found_piece_or_edge = self.add_if_offset_position_has_not_current_color_piece(
                result=result,
                row=row_offset)
            if has_found_piece_or_edge: break
        for row_offset in range(-1, -8, -1):
            has_found_piece_or_edge = self.add_if_offset_position_has_not_current_color_piece(
                result=result,
                row=row_offset)
            if has_found_piece_or_edge: break
        for col_offset in range(1, 8):
            has_found_piece_or_edge = self.add_if_offset_position_has_not_current_color_piece(
                result=result,
                col=col_offset)
            if has_found_piece_or_edge: break
        for col_offset in range(-1, -8, -1):
            has_found_piece_or_edge = self.add_if_offset_position_has_not_current_color_piece(
                result=result,
                col=col_offset)
            if has_found_piece_or_edge: break

        return result

    def manage_bishop_moves(self):
        result = []
        for diag_offset in range(1, 8):
            has_found_piece_or_edge = self.add_if_offset_position_has_not_current_color_piece(
                result=result,
                row=diag_offset,
                col=diag_offset)
            if has_found_piece_or_edge: break
        for diag_offset in range(1, 8):
            has_found_piece_or_edge = self.add_if_offset_position_has_not_current_color_piece(
                result=result,
                row=diag_offset,
                col=-diag_offset)
            if has_found_piece_or_edge: break
        for diag_offset in range(1, 8):
            has_found_piece_or_edge = self.add_if_offset_position_has_not_current_color_piece(
                result=result,
                row=-diag_offset,
                col=diag_offset)
            if has_found_piece_or_edge: break
        for diag_offset in range(1, 8):
            has_found_piece_or_edge = self.add_if_offset_position_has_not_current_color_piece(
                result=result,
                row=-diag_offset,
                col=-diag_offset)
            if has_found_piece_or_edge: break
        return result

    def manage_queen_moves(self):
        result = []
        result.extend(self.manage_bishop_moves())
        result.extend(self.manage_rook_moves())
        return result

    def manage_king_moves(self):
        result = []
        self.add_if_offset_position_has_not_current_color_piece(result=result, row=1, col=0)
        self.add_if_offset_position_has_not_current_color_piece(result=result, row=-1, col=0)
        self.add_if_offset_position_has_not_current_color_piece(result=result, row=0, col=1)
        self.add_if_offset_position_has_not_current_color_piece(result=result, row=0, col=-1)
        self.add_if_offset_position_has_not_current_color_piece(result=result, row=1, col=1)
        self.add_if_offset_position_has_not_current_color_piece(result=result, row=1, col=-1)
        self.add_if_offset_position_has_not_current_color_piece(result=result, row=-1, col=1)
        self.add_if_offset_position_has_not_current_color_piece(result=result, row=-1, col=-1)
        return result

    def add_if_offset_position_has_no_piece(self, result: List[Position], row: int = 0, col: int = 0) -> bool:
        if (self.is_offset_belong_to_board(row=row, col=col) and
                not self.is_offset_position_has_piece_between(row=row, col=col)):
            result.append(self.selected_position.offset(row=row, col=col))
        return (self.is_offset_position_has_piece(row=row, col=col) or
                not self.is_offset_belong_to_board(row=row, col=col))

    def add_if_offset_position_has_not_current_color_piece(self, result: List[Position], row: int = 0,
                                                           col: int = 0) -> bool:
        if (self.is_offset_belong_to_board(row=row, col=col) and
                self.is_offset_belong_to_board(row=row, col=col) and
                not self.is_offset_position_has_current_color_piece(row=row, col=col)):
            result.append(self.selected_position.offset(row=row, col=col))
        return (self.is_offset_position_has_piece(row=row, col=col) or
                not self.is_offset_belong_to_board(row=row, col=col))

    def add_if_offset_position_has_opponent_piece(self, result: List[Position], row: int = 0, col: int = 0) -> bool:
        if (self.is_offset_belong_to_board(row=row, col=col) and
                self.is_offset_position_has_opponent_piece(row=row, col=col)):
            result.append(self.selected_position.offset(row=row, col=col))
        return (self.is_offset_position_has_piece(row=row, col=col) or
                not self.is_offset_belong_to_board(row=row, col=col))

    def is_offset_position_has_piece_between(self, row: int = 0, col: int = 0) -> bool:
        if row != 0:
            step = 1 if row > 0 else -1
            for i in range(0, row, step):
                if self.board.get_piece(self.selected_position.offset(row=i + step, col=col)) is not None: return True
        if col != 0:
            step = 1 if col > 0 else -1
            for i in range(0, col, step):
                if self.board.get_piece(self.selected_position.offset(row=row, col=i + step)) is not None: return True
        return False

    def is_offset_position_has_selected_color_piece(self, row: int = 0, col: int = 0) -> bool:
        selected_piece = self.get_selected_piece()
        piece_on_offset_position = self.board.get_piece(self.selected_position.offset(row=row, col=col))
        return piece_on_offset_position is not None and piece_on_offset_position.color == selected_piece.color

    def is_offset_position_has_opponent_piece(self, row: int = 0, col: int = 0) -> bool:
        selected_piece = self.get_selected_piece()
        piece_on_offset_position = self.board.get_piece(self.selected_position.offset(row=row, col=col))
        return piece_on_offset_position is not None and piece_on_offset_position.color != selected_piece.color

    def is_offset_position_has_current_color_piece(self, row: int = 0, col: int = 0) -> bool:
        selected_piece = self.get_selected_piece()
        piece_on_offset_position = self.board.get_piece(self.selected_position.offset(row=row, col=col))
        return piece_on_offset_position is not None and piece_on_offset_position.color == selected_piece.color

    def is_offset_position_has_piece(self, row: int = 0, col: int = 0) -> bool:
        piece_on_offset_position = self.board.get_piece(self.selected_position.offset(row=row, col=col))
        return piece_on_offset_position is not None

    def is_offset_belong_to_board(self, row: int = 0, col: int = 0):
        return self.selected_position.offset(row=row, col=col).belong_to_board()
