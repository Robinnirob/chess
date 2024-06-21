from typing import List, Optional, Set

from chess.board import Board
from chess.data import PieceColor, Position, PieceName, Piece, Move

INITIAL_PAWN_ROW_BY_COLOR = {PieceColor.BLACK: 6, PieceColor.WHITE: 1}


class GameManager:
    board: Board
    current_player: PieceColor
    selected_position: Position = None
    selected_piece: Piece = None
    move_history: List[Move] = []
    piece_to_promote_position: Optional[Position] = None

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

    def move(self, position: Position):
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
        moves = self.get_authorized_moves()
        for move in moves.copy():
            cloned_board = self.board.copy()
            cloned_board.move(move)
            if self.is_king_threated(cloned_board, king_color=self.current_player):
                moves.remove(move)
        return [move.target for move in moves]

    def get_authorized_moves(self):
        selected_piece = self.get_selected_piece()
        if selected_piece is None:
            return []
        elif selected_piece.name == PieceName.PAWN:
            return self.manage_pawn_moves(self.board)
        elif selected_piece.name == PieceName.NIGHT:
            return self.manage_knight_moves(self.board)
        elif selected_piece.name == PieceName.ROOK:
            return self.manage_rook_moves(self.board)
        elif selected_piece.name == PieceName.BISHOP:
            return self.manage_bishop_moves(self.board)
        elif selected_piece.name == PieceName.QUEEN:
            return self.manage_queen_moves(self.board)
        elif selected_piece.name == PieceName.KING:
            return self.manage_king_moves(self.board)
        raise ValueError(f"Unknown piece {selected_piece}")

    def manage_pawn_moves(self, board: Board, position: Position = None) -> List[Move]:
        my_position = position if position is not None else self.selected_position
        selected_piece = self.board.get_piece(my_position)
        direction = 1 if selected_piece.color == PieceColor.WHITE else -1
        is_initial_position = INITIAL_PAWN_ROW_BY_COLOR[selected_piece.color] == self.selected_position.row
        result = []
        self.add_if_offset_position_has_no_piece(board=board, position=my_position, result=result, row=direction)
        if is_initial_position: self.add_if_offset_position_has_no_piece(board=board, position=my_position, result=result, row=direction * 2, is_two_step_pawn_move=True)
        self.add_if_offset_position_has_opponent_piece(board=board, position=my_position, result=result, row=direction, col=1)
        self.add_if_offset_position_has_opponent_piece(board=board, position=my_position, result=result, row=direction, col=-1)
        previous_move = self.move_history[-1] if len(self.move_history) > 0 else None
        if previous_move is not None and previous_move.is_two_step_pawn_move:
            en_passant_position = previous_move.target.offset(row=direction)
            if (my_position.offset(row=direction, col=1) == en_passant_position or
                    my_position.offset(row=direction, col=-1) == en_passant_position):
                result.append(self.move_factory(
                    target=en_passant_position,
                    piece_taken=previous_move.piece_moved,
                    piece_taken_position=previous_move.target,
                ))
        return result

    def manage_pawn_threats(self, position: Position, color: PieceColor) -> List[Position]:
        direction = 1 if color == PieceColor.WHITE else -1
        return [
            position.offset(row=direction, col=1),
            position.offset(row=direction, col=-1),
        ]

    def manage_knight_moves(self, board: Board, position: Position = None) -> List[Move]:
        my_position = position if position is not None else self.selected_position
        result = []
        self.add_if_offset_position_has_not_current_color_piece(board=board, position=my_position, result=result, row=-1, col=-2)
        self.add_if_offset_position_has_not_current_color_piece(board=board, position=my_position, result=result, row=1, col=-2)
        self.add_if_offset_position_has_not_current_color_piece(board=board, position=my_position, result=result, row=-2, col=-1)
        self.add_if_offset_position_has_not_current_color_piece(board=board, position=my_position, result=result, row=2, col=-1)
        self.add_if_offset_position_has_not_current_color_piece(board=board, position=my_position, result=result, row=-2, col=1)
        self.add_if_offset_position_has_not_current_color_piece(board=board, position=my_position, result=result, row=2, col=1)
        self.add_if_offset_position_has_not_current_color_piece(board=board, position=my_position, result=result, row=-1, col=2)
        self.add_if_offset_position_has_not_current_color_piece(board=board, position=my_position, result=result, row=1, col=2)
        return result

    def manage_knight_threats(self, position: Position) -> List[Position]:
        positions = [
            position.offset(row=-1, col=-2),
            position.offset(row=1, col=-2),
            position.offset(row=-2, col=-1),
            position.offset(row=2, col=-1),
            position.offset(row=-2, col=1),
            position.offset(row=2, col=1),
            position.offset(row=-1, col=2),
            position.offset(row=1, col=2),
        ]
        print(f"knight threats ({str(position)}): {[str(pos) for pos in positions]}")
        return positions

    def manage_rook_moves(self, board: Board, position: Position = None) -> List[Move]:
        my_position = position if position is not None else self.selected_position
        result = []
        for row_offset in range(1, 8):
            has_found_piece_or_edge = self.add_if_offset_position_has_not_current_color_piece(
                board=board,
                position=my_position,
                result=result,
                row=row_offset)
            if has_found_piece_or_edge: break
        for row_offset in range(-1, -8, -1):
            has_found_piece_or_edge = self.add_if_offset_position_has_not_current_color_piece(
                board=board,
                position=my_position,
                result=result,
                row=row_offset)
            if has_found_piece_or_edge: break
        for col_offset in range(1, 8):
            has_found_piece_or_edge = self.add_if_offset_position_has_not_current_color_piece(
                board=board,
                position=my_position,
                result=result,
                col=col_offset)
            if has_found_piece_or_edge: break
        for col_offset in range(-1, -8, -1):
            has_found_piece_or_edge = self.add_if_offset_position_has_not_current_color_piece(
                board=board,
                position=my_position,
                result=result,
                col=col_offset)
            if has_found_piece_or_edge: break

        return result

    def manage_rook_threat(self, board: Board, position: Position = None) -> List[Position]:
        result = []
        for row_offset in range(1, 8):
            offset_position = position.offset(row=row_offset)
            if not offset_position.belong_to_board():
                break
            result.append(offset_position)
            if board.get_piece(offset_position) is not None:
                break
        for row_offset in range(-1, -8, -1):
            offset_position = position.offset(row=row_offset)
            if not offset_position.belong_to_board():
                break
            result.append(offset_position)
            if board.get_piece(offset_position) is not None:
                break
        for col_offset in range(1, 8):
            offset_position = position.offset(col=col_offset)
            if not offset_position.belong_to_board():
                break
            result.append(offset_position)
            if board.get_piece(offset_position) is not None:
                break
        for col_offset in range(-1, -8, -1):
            offset_position = position.offset(col=col_offset)
            if not offset_position.belong_to_board():
                break
            result.append(offset_position)
            if board.get_piece(offset_position) is not None:
                break

        return result

    def manage_bishop_moves(self, board: Board, position: Position = None) -> List[Move]:
        my_position = position if position is not None else self.selected_position
        result = []
        for diag_offset in range(1, 8):
            has_found_piece_or_edge = self.add_if_offset_position_has_not_current_color_piece(
                board=board,
                position=my_position,
                result=result,
                row=diag_offset,
                col=diag_offset)
            if has_found_piece_or_edge: break
        for diag_offset in range(1, 8):
            has_found_piece_or_edge = self.add_if_offset_position_has_not_current_color_piece(
                board=board,
                position=my_position,
                result=result,
                row=diag_offset,
                col=-diag_offset)
            if has_found_piece_or_edge: break
        for diag_offset in range(1, 8):
            has_found_piece_or_edge = self.add_if_offset_position_has_not_current_color_piece(
                board=board,
                position=my_position,
                result=result,
                row=-diag_offset,
                col=diag_offset)
            if has_found_piece_or_edge: break
        for diag_offset in range(1, 8):
            has_found_piece_or_edge = self.add_if_offset_position_has_not_current_color_piece(
                board=board,
                position=my_position,
                result=result,
                row=-diag_offset,
                col=-diag_offset)
            if has_found_piece_or_edge: break
        return result

    def manage_bishop_threat(self, board: Board, position: Position = None) -> List[Position]:
        result = []
        for offset in range(1, 8):
            offset_position = position.offset(col=offset, row=offset)
            if not offset_position.belong_to_board():
                break
            result.append(offset_position)
            if board.get_piece(offset_position) is not None:
                break
        for offset in range(1, 8):
            offset_position = position.offset(col=offset, row=-offset)
            if not offset_position.belong_to_board():
                break
            result.append(offset_position)
            if board.get_piece(offset_position) is not None:
                break
        for offset in range(1, 8):
            offset_position = position.offset(col=-offset, row=offset)
            if not offset_position.belong_to_board():
                break
            result.append(offset_position)
            if board.get_piece(offset_position) is not None:
                break
        for offset in range(1, 8):
            offset_position = position.offset(col=-offset, row=-offset)
            if not offset_position.belong_to_board():
                break
            result.append(offset_position)
            if board.get_piece(offset_position) is not None:
                break

        return result

    def manage_queen_moves(self, board: Board, position: Position = None) -> List[Move]:
        my_position = position if position is not None else self.selected_position
        result = []
        result.extend(self.manage_bishop_moves(board=board, position=my_position))
        result.extend(self.manage_rook_moves(board=board, position=my_position))
        return result

    def manage_queen_threat(self, board: Board, position: Position = None) -> List[Position]:
        result = []
        result.extend(self.manage_bishop_threat(board=board, position=position))
        result.extend(self.manage_rook_threat(board=board, position=position))
        return result

    def manage_king_moves(self, board: Board, position: Position = None) -> List[Move]:
        my_position = position if position is not None else self.selected_position
        selected_piece = self.board.get_piece(my_position)
        result = []
        self.add_if_offset_position_has_not_current_color_piece(board=board, position=my_position, result=result, row=1, col=0)
        self.add_if_offset_position_has_not_current_color_piece(board=board, position=my_position, result=result, row=-1, col=0)
        self.add_if_offset_position_has_not_current_color_piece(board=board, position=my_position, result=result, row=0, col=1)
        self.add_if_offset_position_has_not_current_color_piece(board=board, position=my_position, result=result, row=0, col=-1)
        self.add_if_offset_position_has_not_current_color_piece(board=board, position=my_position, result=result, row=1, col=1)
        self.add_if_offset_position_has_not_current_color_piece(board=board, position=my_position, result=result, row=1, col=-1)
        self.add_if_offset_position_has_not_current_color_piece(board=board, position=my_position, result=result, row=-1, col=1)
        self.add_if_offset_position_has_not_current_color_piece(board=board, position=my_position, result=result, row=-1, col=-1)
        _, filtered_position = self.filter_position_threated(
            board=self.board,
            positions=[move.target for move in result],
            color=selected_piece.color.opposite_color()
        )
        return [move for move in result if move.target in filtered_position]

    def manage_king_threat(self, position: Position = None) -> List[Position]:
        result = [
            position.offset(row=1, col=0),
            position.offset(row=-1, col=0),
            position.offset(row=0, col=1),
            position.offset(row=0, col=-1),
            position.offset(row=1, col=1),
            position.offset(row=1, col=-1),
            position.offset(row=-1, col=1),
            position.offset(row=-1, col=-1),
        ]
        return result

    def keep_two_step_information(self, col: int, color: PieceColor):
        self.en_passant_info_of_previous_move = (col, color)

    def add_if_offset_position_has_no_piece(self, board: Board, position: Position, result: List[Move], row: int = 0, col: int = 0, is_two_step_pawn_move: bool = False) -> bool:
        if (self.is_offset_belong_to_board(position=position, row=row, col=col) and
                not self.is_offset_position_has_piece_between(board=board, position=position, row=row, col=col)):
            target_position = position.offset(row=row, col=col)
            result.append(self.move_factory(
                target=target_position,
                piece_taken=self.board.get_piece(target_position),
                is_two_step_pawn_move=is_two_step_pawn_move
            ))
        return (self.is_offset_position_has_piece(board=board, position=position, row=row, col=col) or
                not self.is_offset_belong_to_board(position=position, row=row, col=col))

    def add_if_offset_position_has_not_current_color_piece(self, board: Board, position: Position, result: List[Move], row: int = 0, col: int = 0, is_two_step_pawn_move: bool = False) -> bool:
        if (self.is_offset_belong_to_board(position=position, row=row, col=col) and
                self.is_offset_belong_to_board(position=position, row=row, col=col) and
                not self.is_offset_position_has_current_color_piece(board=board, position=position, row=row, col=col)):
            target_position = position.offset(row=row, col=col)
            result.append(self.move_factory(target_position, self.board.get_piece(target_position), is_two_step_pawn_move=is_two_step_pawn_move))
        return (self.is_offset_position_has_piece(board=board, position=position, row=row, col=col) or
                not self.is_offset_belong_to_board(position=position, row=row, col=col))

    def add_if_offset_position_has_opponent_piece(self, board: Board, position: Position, result: List[Move], row: int = 0, col: int = 0, is_two_step_pawn_move: bool = False) -> bool:
        if (self.is_offset_belong_to_board(position=position, row=row, col=col) and
                self.is_offset_position_has_opponent_piece(board=board, position=position, row=row, col=col)):
            target_position = position.offset(row=row, col=col)
            result.append(self.move_factory(target_position, self.board.get_piece(target_position), is_two_step_pawn_move=is_two_step_pawn_move))
        return (self.is_offset_position_has_piece(board=board, position=position, row=row, col=col) or
                not self.is_offset_belong_to_board(position=position, row=row, col=col))

    def is_offset_position_has_piece_between(self, board: Board, position: Position, row: int = 0, col: int = 0) -> bool:
        if row != 0:
            step = 1 if row > 0 else -1
            for i in range(0, row, step):
                if board.get_piece(position.offset(row=i + step, col=col)) is not None: return True
        if col != 0:
            step = 1 if col > 0 else -1
            for i in range(0, col, step):
                if board.get_piece(position.offset(row=row, col=i + step)) is not None: return True
        return False

    def is_offset_position_has_selected_color_piece(self, board: Board, position: Position, row: int = 0, col: int = 0) -> bool:
        piece = board.get_piece(position)
        piece_on_offset_position = board.get_piece(position.offset(row=row, col=col))
        return piece_on_offset_position is not None and piece_on_offset_position.color == piece.color

    def is_offset_position_has_opponent_piece(self, board: Board, position: Position, row: int = 0, col: int = 0) -> bool:
        piece = board.get_piece(position)
        piece_on_offset_position = board.get_piece(position.offset(row=row, col=col))
        return piece_on_offset_position is not None and piece_on_offset_position.color != piece.color

    def is_offset_position_has_current_color_piece(self, board: Board, position: Position, row: int = 0, col: int = 0) -> bool:
        piece = board.get_piece(position)
        piece_on_offset_position = board.get_piece(position.offset(row=row, col=col))
        return piece_on_offset_position is not None and piece_on_offset_position.color == piece.color

    def is_offset_position_has_piece(self, board: Board, position: Position, row: int = 0, col: int = 0) -> bool:
        piece_on_offset_position = board.get_piece(position.offset(row=row, col=col))
        return piece_on_offset_position is not None

    def is_offset_belong_to_board(self, position: Position, row: int = 0, col: int = 0):
        return position.offset(row=row, col=col).belong_to_board()

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

    def filter_position_threated(self, positions: List[Position], color: PieceColor, board: Board) -> tuple[Set[Position], Set[Position]]:
        final_threated_positions = set()
        final_unthreated_positions = set(positions)
        pieces_position = board.get_pieces_position(color)
        for position, piece in pieces_position.items():
            threat_positions = None
            if piece.name == PieceName.PAWN:
                threat_positions = self.manage_pawn_threats(position, piece.color)
            elif piece.name == PieceName.NIGHT:
                threat_positions = self.manage_knight_threats(position)
            elif piece.name == PieceName.ROOK:
                threat_positions = self.manage_rook_threat(board, position)
            elif piece.name == PieceName.BISHOP:
                threat_positions = self.manage_bishop_threat(board, position)
            elif piece.name == PieceName.QUEEN:
                threat_positions = self.manage_queen_threat(board, position)
            elif piece.name == PieceName.KING:
                threat_positions = self.manage_king_threat(position)

            for unthreated_position in final_unthreated_positions.copy():
                if unthreated_position in threat_positions:
                    final_threated_positions.add(unthreated_position)
                    final_unthreated_positions.remove(unthreated_position)
            if len(final_unthreated_positions) == 0:
                break
        return final_threated_positions, final_unthreated_positions

    def is_king_threated(self, board: Board, king_color: PieceColor):
        positions = board.get_piece_position_by_name(PieceName.KING, king_color)
        threated_positions, _ = self.filter_position_threated(board=board, positions=positions, color=king_color.opposite_color())
        return len(threated_positions) != 0
