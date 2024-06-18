import tkinter as tk
from tkinter import messagebox

# Dimensions de l'échiquier
BOARD_SIZE = 8
SQUARE_SIZE = 60

# Initialisation de la fenêtre principale
root = tk.Tk()
root.title("Échiquier avec Tkinter")

# Création du canevas pour l'échiquier
canvas = tk.Canvas(root, width=BOARD_SIZE*SQUARE_SIZE, height=BOARD_SIZE*SQUARE_SIZE)
canvas.pack()

# Dictionnaire des positions initiales des pièces
initial_positions = {
    'a1': 'wr', 'b1': 'wn', 'c1': 'wb', 'd1': 'wq', 'e1': 'wk', 'f1': 'wb', 'g1': 'wn', 'h1': 'wr',
    'a2': 'wp', 'b2': 'wp', 'c2': 'wp', 'd2': 'wp', 'e2': 'wp', 'f2': 'wp', 'g2': 'wp', 'h2': 'wp',
    'a7': 'bp', 'b7': 'bp', 'c7': 'bp', 'd7': 'bp', 'e7': 'bp', 'f7': 'bp', 'g7': 'bp', 'h7': 'bp',
    'a8': 'br', 'b8': 'bn', 'c8': 'bb', 'd8': 'bq', 'e8': 'bk', 'f8': 'bb', 'g8': 'bn', 'h8': 'br'
}
selected_case = None

# Fonction pour dessiner l'échiquier
def draw_board():
    canvas.delete("all")
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            case = chr(col + 97) + str(BOARD_SIZE - row)
            color = "white" if (row + col) % 2 == 0 else "gray"
            color = "blue" if selected_case == case else color
            x1 = col * SQUARE_SIZE
            y1 = row * SQUARE_SIZE
            x2 = x1 + SQUARE_SIZE
            y2 = y1 + SQUARE_SIZE
            canvas.create_rectangle(x1, y1, x2, y2, fill=color)
            # Calcul de l'adresse de la case

            if case in initial_positions:
                piece = initial_positions[case]
                draw_piece(x1, y1, piece)

# Fonction pour dessiner une pièce sur l'échiquier
def draw_piece(x1, y1, piece):
    color = "white" if piece[0] == 'w' else "black"
    piece_type = piece[1].upper()
    radius = SQUARE_SIZE // 3
    x_center = x1 + SQUARE_SIZE / 2
    y_center = y1 + SQUARE_SIZE / 2
    canvas.create_oval(x_center - radius, y_center - radius, x_center + radius, y_center + radius, fill=color)
    canvas.create_text(x_center, y_center, text=piece_type, font=("Arial", 24), fill="black" if color == "white" else "white")

# Fonction pour gérer le clic sur une case
def on_square_click(event):
    col = event.x // SQUARE_SIZE
    row = event.y // SQUARE_SIZE
    case = chr(col + 97) + str(BOARD_SIZE - row)
    global selected_case
    piece = initial_positions[selected_case] if selected_case in initial_positions else None

    if selected_case is None or piece is None:
        selected_case = case
    else:
        del initial_positions[selected_case]
        initial_positions[case] = piece
        selected_case = None
    draw_board()
    print(f"Clic sur la case {case}")

# Fonction pour gérer la soumission du formulaire
def on_form_submit():
    entered_text = entry.get()
    print(f"Texte saisi : {entered_text}")
    messagebox.showinfo("Formulaire soumis", f"Vous avez saisi : {entered_text}")

# Dessiner l'échiquier
draw_board()

# Associer le clic de souris à la fonction on_square_click
canvas.bind("<Button-1>", on_square_click)

# Ajouter un cadre pour le formulaire en dessous de l'échiquier
form_frame = tk.Frame(root)
form_frame.pack(pady=10)

# Ajouter un label, un champ de saisie et un bouton de validation dans le cadre
label = tk.Label(form_frame, text="Saisir du texte :")
label.pack(side=tk.LEFT, padx=5)

entry = tk.Entry(form_frame)
entry.pack(side=tk.LEFT, padx=5)

submit_button = tk.Button(form_frame, text="Valider", command=on_form_submit)
submit_button.pack(side=tk.LEFT, padx=5)

# Démarrer la boucle principale Tkinter
root.mainloop()
