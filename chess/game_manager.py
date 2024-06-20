from typing import List, Optional

from chess.board import Board
from chess.data import PieceColor, Position, PieceName, Piece, Move

INITIAL_PAWN_ROW_BY_COLOR = {PieceColor.BLACK: 6, PieceColor.WHITE: 1}


class GameManager:
    board: Board
    current_player: PieceColor
    selected_position: Position = None
    selected_piece: Piece = None
    move_history: List[Move] = []
    piece_to_promote_position: Position = None

    def __init__(self, board: Board, current_player: PieceColor = PieceColor.WHITE):
        self.current_player = current_player
        self.board = board

    def get_selected_position(self):
        return self.selected_position

    def get_current_player(self) -> PieceColor:
        return self.current_player

    def get_selected_piece(self) -> Piece:
        return self.selected_piece

    def do_action(self, position: Position):
        is_move_action = position in self.get_authorized_target_position() and self.get_selected_piece().color == self.current_player
        if is_move_action:
            self.move(position)
        else:
            self.select_position(position)

    def move(self, position):
        move = None
        for authorized_move in self.get_authorized_moves():
            if authorized_move.target == position:
                move = authorized_move
                break

        if move is None:
            raise ValueError("Target position is not in authorized moves")

        self.board.move(move=move)
        self.move_history.append(move)
        self.select_position(None)
        if move.piece_moved.name == PieceName.PAWN and move.target.is_last_position(move.piece_moved.color):
            self.piece_to_promote_position = move.target
        self.current_player = PieceColor.BLACK if self.current_player == PieceColor.WHITE else PieceColor.WHITE

    def select_position(self, position: Optional[Position]):
        self.selected_position = position
        self.selected_piece = self.board.get_piece(self.selected_position)

    def get_authorized_target_position(self) -> List[Position]:
        return [move.target for move in self.get_authorized_moves()]

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

    def manage_pawn_moves(self) -> List[Move]:
        selected_piece = self.get_selected_piece()
        selected_position = self.get_selected_position()
        direction = 1 if selected_piece.color == PieceColor.WHITE else -1
        is_initial_position = INITIAL_PAWN_ROW_BY_COLOR[selected_piece.color] == self.selected_position.row
        result = []
        self.add_if_offset_position_has_no_piece(result=result, row=direction)
        if is_initial_position: self.add_if_offset_position_has_no_piece(result=result, row=direction * 2, is_two_step_pawn_move=True)
        self.add_if_offset_position_has_opponent_piece(result=result, row=direction, col=1)
        self.add_if_offset_position_has_opponent_piece(result=result, row=direction, col=-1)
        previous_move = self.move_history[-1] if len(self.move_history) > 0 else None
        if previous_move is not None and previous_move.is_two_step_pawn_move:
            en_passant_position = previous_move.target.offset(row=direction)
            if (selected_position.offset(row=direction, col=1) == en_passant_position or
                    selected_position.offset(row=direction, col=-1) == en_passant_position):
                result.append(self.move_factory(
                    target=en_passant_position,
                    piece_taken=previous_move.piece_moved,
                    piece_taken_position=previous_move.target,
                ))
        return result

    def manage_knight_moves(self) -> List[Move]:
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

    def manage_rook_moves(self) -> List[Move]:
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

    def manage_bishop_moves(self) -> List[Move]:
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

    def keep_two_step_information(self, col: int, color: PieceColor):
        self.en_passant_info_of_previous_move = (col, color)

    def add_if_offset_position_has_no_piece(self, result: List[Move], row: int = 0, col: int = 0, is_two_step_pawn_move: bool = False) -> bool:
        if (self.is_offset_belong_to_board(row=row, col=col) and
                not self.is_offset_position_has_piece_between(row=row, col=col)):
            target_position = self.selected_position.offset(row=row, col=col)
            result.append(self.move_factory(target=target_position, piece_taken=self.board.get_piece(target_position), is_two_step_pawn_move=is_two_step_pawn_move))
        return (self.is_offset_position_has_piece(row=row, col=col) or
                not self.is_offset_belong_to_board(row=row, col=col))

    def add_if_offset_position_has_not_current_color_piece(self, result: List[Move], row: int = 0, col: int = 0, is_two_step_pawn_move: bool = False) -> bool:
        if (self.is_offset_belong_to_board(row=row, col=col) and
                self.is_offset_belong_to_board(row=row, col=col) and
                not self.is_offset_position_has_current_color_piece(row=row, col=col)):
            target_position = self.selected_position.offset(row=row, col=col)
            result.append(self.move_factory(target_position, self.board.get_piece(target_position), is_two_step_pawn_move=is_two_step_pawn_move))
        return (self.is_offset_position_has_piece(row=row, col=col) or
                not self.is_offset_belong_to_board(row=row, col=col))

    def add_if_offset_position_has_opponent_piece(self, result: List[Move], row: int = 0, col: int = 0, is_two_step_pawn_move: bool = False) -> bool:
        if (self.is_offset_belong_to_board(row=row, col=col) and
                self.is_offset_position_has_opponent_piece(row=row, col=col)):
            target_position = self.selected_position.offset(row=row, col=col)
            result.append(self.move_factory(target_position, self.board.get_piece(target_position), is_two_step_pawn_move=is_two_step_pawn_move))
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

    def move_factory(self, target: Position, piece_taken: Piece, piece_taken_position: Optional[Position] = None, is_two_step_pawn_move: bool = False) -> Move:
        my_piece_taken_position = None if piece_taken is None else target
        my_piece_taken_position = piece_taken_position if piece_taken_position is not None else my_piece_taken_position
        return Move(
            source=self.get_selected_position(),
            target=target,
            piece_moved=self.get_selected_piece(),
            piece_taken=piece_taken,
            piece_taken_position=my_piece_taken_position,
            is_two_step_pawn_move=is_two_step_pawn_move
        )

    def is_waiting_promotion_info(self):
        return self.piece_to_promote_position is not None

    def promote_to(self, piece_name):
        self.board.promote(self.piece_to_promote_position, Piece(self.current_player.opposite_color(), piece_name))
        self.piece_to_promote_position = None
