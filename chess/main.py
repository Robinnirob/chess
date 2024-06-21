from chess.board import Board, board_factory
from chess.game_manager import GameManager
from chess.ui_manager import MainWindow

board = board_factory()
game_manager = GameManager(board)
ui_manager = MainWindow(board, game_manager)
ui_manager.show()
