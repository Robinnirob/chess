from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from drawer import draw_chessboard_with_labels

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

initial_positions = [
    ('R', 'W', 'a1'), ('N', 'W', 'b1'), ('B', 'W', 'c1'), ('K', 'W', 'd1'),
    ('Q', 'W', 'e1'), ('B', 'W', 'f1'), ('N', 'W', 'g1'), ('R', 'W', 'h1'),
    ('P', 'W', 'a2'), ('P', 'W', 'b2'), ('P', 'W', 'c2'), ('P', 'W', 'd2'),
    ('P', 'W', 'e2'), ('P', 'W', 'f2'), ('P', 'W', 'g2'), ('P', 'W', 'h2'),
    ('P', 'B', 'a7'), ('P', 'B', 'b7'), ('P', 'B', 'c7'), ('P', 'B', 'd7'),
    ('P', 'B', 'e7'), ('P', 'B', 'f7'), ('P', 'B', 'g7'), ('P', 'B', 'h7'),
    ('R', 'B', 'a8'), ('N', 'B', 'b8'), ('B', 'B', 'c8'), ('K', 'B', 'd8'),
    ('Q', 'B', 'e8'), ('B', 'B', 'f8'), ('N', 'B', 'g8'), ('R', 'B', 'h8')
]

COLOR_LABEL = {
    'W': "Blanc",
    'B': "Noir",
}


@app.get("/", response_class=HTMLResponse)
async def get_chessboard():
    draw_chessboard_with_labels(initial_positions)
    chess_positions = to_pieces_input(initial_positions)

    with open("chessboard_with_labels.svg", "r") as file:
        svg_content = file.read()
    return f"""
        <html>
            <body>
                {svg_content}
                <form action="/update" method="post">
                    <input type="text" name="mouvement_requested" placeholder="Mouvement" value="a2-a3">
                    <input type="hidden" name="chess_positions" value="{chess_positions}"/>
                    <input type="hidden" name="next_player" value="W"/>
                    <button type="submit">Update Board</button>
                </form>
            </body>
        </html>
        """


@app.post("/update", response_class=HTMLResponse)
async def update_chessboard(
        mouvement_requested: str = Form(...),
        chess_positions: str = Form(...),
        next_player: str = Form(...)):
    pieces_list = parse_pieces_input(chess_positions)
    pieces_list, error_msg = do_movement(pieces_list, mouvement_requested, next_player)
    chess_positions = to_pieces_input(pieces_list)
    draw_chessboard_with_labels(pieces_list)
    with open("chessboard_with_labels.svg", "r") as file:
        svg_content = file.read()

    if error_msg == "":
        if next_player == 'W':
            next_player = 'B'
        else:
            next_player = 'W'

    return f"""
    <html>
        <body>
            {svg_content}
            <form action="/update" method="post">
                <input type="text" name="mouvement_requested" placeholder="Mouvement">
                <input type="hidden" name="chess_positions" value="{chess_positions}"/>
                <input type="hidden" name="next_player" value="{next_player}"/>
                <button type="submit">Update Board</button>
            </form>
            <div style='color: red'>{error_msg}</div>
            <div style='color: purple'>Trait aux {COLOR_LABEL[next_player]}s</div>
        </body>
    </html>
    """


def do_movement(pieces_list, movement_requested, current_player):
    new_piece_list = []

    positions = movement_requested.split('-')
    initial_position = positions[0]
    target_position = positions[1]

    if ord(target_position[0]) < ord("a") or ord(target_position[0]) > ord("h"):
        return pieces_list, f"La position de destination est hors du plateau: {target_position}"

    if int(target_position[1:]) < 1 or int(target_position[1:]) > 8:
        return pieces_list, f"La position de destination est hors du plateau: {target_position}"

    is_piece_found = False

    for piece, color, position in pieces_list:
        if position == initial_position:
            if color != current_player:
                return pieces_list, f"C'est au joueur {COLOR_LABEL[current_player]}({current_player}) de jouer: {piece}/{color}/{position}"
            if piece == "P":
                if color == "B":
                    authorized_move = f"{position[0]}{int(position[1:]) - 1}"
                else:
                    authorized_move = f"{position[0]}{int(position[1:]) + 1}"

                if target_position != authorized_move:
                    return pieces_list, f"Ce coup n'est pas autorisé ({authorized_move}): {target_position}"

            new_piece_list.append((piece, color, target_position))
            is_piece_found = True
        else:
            new_piece_list.append((piece, color, position))
    if is_piece_found:
        error_msg = ""
    else:
        error_msg = f"La pièce {initial_position} n'a pas été trouvée"
    return new_piece_list, error_msg


def parse_pieces_input(pieces_str):
    pieces_list = []
    for piece_str in pieces_str.split(';'):
        piece_info = piece_str.split(',')
        if len(piece_info) == 3:
            pieces_list.append((piece_info[0], piece_info[1], piece_info[2]))
    return pieces_list


def to_pieces_input(pieces_data):
    pieces_str = ""
    for piece in pieces_data:
        pieces_str += f"{piece[0]},{piece[1]},{piece[2]};"
    return pieces_str
