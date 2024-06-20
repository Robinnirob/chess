import tkinter as tk
from tkinter import messagebox

from chess.board import Board
from chess.data import BOARD_SIZE, SQUARE_SIZE, Position, Piece, PieceColor
from chess.game_manager import GameManager


class MainWindow:
    board: Board
    game_manager: GameManager
    entry: tk.Entry

    def __init__(self, board: Board, game_manager: GameManager):
        self.board = board
        self.game_manager = game_manager

        self.root = tk.Tk()
        self.root.title("Échiquier avec Tkinter")

        # Création du canevas pour l'échiquier
        self.canvas = tk.Canvas(self.root, width=BOARD_SIZE * SQUARE_SIZE, height=BOARD_SIZE * SQUARE_SIZE)
        self.canvas.pack()

    def show(self):
        # Dessiner l'échiquier
        self.draw_board()

        # Associer le clic de souris à la fonction on_square_click
        self.canvas.bind("<Button-1>", self.on_square_click)

        # Ajouter un cadre pour le formulaire en dessous de l'échiquier
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=10)

        # Ajouter un label, un champ de saisie et un bouton de validation dans le cadre
        label = tk.Label(form_frame, text="Saisir du texte :")
        label.pack(side=tk.LEFT, padx=5)

        self.entry = tk.Entry(form_frame)
        self.entry.pack(side=tk.LEFT, padx=5)

        submit_button = tk.Button(form_frame, text="Valider", command=self.on_form_submit)
        submit_button.pack(side=tk.LEFT, padx=5)

        info_frame = tk.Frame(self.root)
        info_frame.pack(pady=10)
        info = tk.Label(info_frame, text="")
        info.pack(side=tk.LEFT, padx=5)

        # Démarrer la boucle principale Tkinter
        self.root.mainloop()

    def draw_board(self):
        self.canvas.delete("all")
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                row = BOARD_SIZE - x - 1
                col = y
                position = Position(row=row, col=col)
                selected_position = self.game_manager.get_selected_position()
                authorized_positions = self.game_manager.get_authorized_moves()

                color = "white" if (x + y) % 2 == 0 else "gray"
                color = "green" if position in authorized_positions else color
                color = "blue" if selected_position == position else color
                x1 = y * SQUARE_SIZE
                y1 = x * SQUARE_SIZE
                x2 = x1 + SQUARE_SIZE
                y2 = y1 + SQUARE_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

                piece = self.board.get_piece(position)
                if piece is not None:
                    self.draw_piece(x1, y1, piece)

    # Fonction pour dessiner une pièce sur l'échiquier
    def draw_piece(self, x1, y1, piece: Piece):
        color = "white" if piece.color == PieceColor.WHITE else "black"
        radius = SQUARE_SIZE // 3
        x_center = x1 + SQUARE_SIZE / 2
        y_center = y1 + SQUARE_SIZE / 2
        self.canvas.create_oval(x_center - radius, y_center - radius, x_center + radius, y_center + radius, fill=color)
        self.canvas.create_text(x_center, y_center, text=piece.icon(), font=("Arial", 24),
                                fill="black" if color == "white" else "white")

    def on_square_click(self, event):
        y = event.x // SQUARE_SIZE
        x = event.y // SQUARE_SIZE
        row = BOARD_SIZE - x - 1
        col = y
        position = Position(row=row, col=col)
        self.game_manager.do_action(position)
        # info['text'] = "Ce coup n'est pas autorisé"
        self.draw_board()
        print(f"Clic sur la case {position}")

    # Fonction pour gérer la soumission du formulaire
    def on_form_submit(self):
        entered_text = self.entry.get()
        print(f"Texte saisi : {entered_text}")
        messagebox.showinfo("Formulaire soumis", f"Vous avez saisi : {entered_text}")
