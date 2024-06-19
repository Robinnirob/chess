from chess.board import Board
from chess.game_manager import GameManager
from chess.ui_manager import MainWindow

board = Board()
game_manager = GameManager(board)
ui_manager = MainWindow(board, game_manager)
ui_manager.show()
