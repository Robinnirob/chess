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
    ('R', 'B', 'a1'), ('N', 'B', 'b1'), ('B', 'B', 'c1'), ('Q', 'B', 'd1'),
    ('K', 'B', 'e1'), ('B', 'B', 'f1'), ('N', 'B', 'g1'), ('R', 'B', 'h1'),
    ('P', 'B', 'a2'), ('P', 'B', 'b2'), ('P', 'B', 'c2'), ('P', 'B', 'd2'),
    ('P', 'B', 'e2'), ('P', 'B', 'f2'), ('P', 'B', 'g2'), ('P', 'B', 'h2'),
    ('P', 'N', 'a7'), ('P', 'N', 'b7'), ('P', 'N', 'c7'), ('P', 'N', 'd7'),
    ('P', 'N', 'e7'), ('P', 'N', 'f7'), ('P', 'N', 'g7'), ('P', 'N', 'h7'),
    ('R', 'N', 'a8'), ('N', 'N', 'b8'), ('B', 'N', 'c8'), ('Q', 'N', 'd8'),
    ('K', 'N', 'e8'), ('B', 'N', 'f8'), ('N', 'N', 'g8'), ('R', 'N', 'h8')
]


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
                    <button type="submit">Update Board</button>
                </form>
            </body>
        </html>
        """


@app.post("/update", response_class=HTMLResponse)
async def update_chessboard(mouvement_requested: str = Form(...), chess_positions: str = Form(...)):
    pieces_list = parse_pieces_input(chess_positions)
    pieces_list, has_error = do_mouvement(pieces_list, mouvement_requested)
    chess_positions = to_pieces_input(pieces_list)
    draw_chessboard_with_labels(pieces_list)
    with open("chessboard_with_labels.svg", "r") as file:
        svg_content = file.read()
    if has_error:
        message = "There's no piece at the starting point !"
    else:
        message = ""
    return f"""
    <html>
        <body>
            {svg_content}
            <form action="/update" method="post">
                <input type="text" name="mouvement_requested" placeholder="Mouvement">
                <input type="hidden" name="chess_positions" value="{chess_positions}"/>
                <button type="submit">Update Board</button>
            </form>
            <div style='color: red'>{message}</div>
        </body>
    </html>
    """

def do_mouvement(pieces_list, mouvement_requested):
    new_piece_list = []

    postions = mouvement_requested.split('-')
    initial_position = postions[0]
    target_position = postions[1]

    if ord(target_position[0]) < ord("a") or ord(target_position[0]) > ord("h"):
        return pieces_list, True

    if int(target_position[1:]) < 1 or int(target_position[1:]) > 8:
        return pieces_list, True

    is_piece_found = False

    for piece, color, position in pieces_list:
        if position == initial_position:
            new_piece_list.append((piece, color, target_position))
            is_piece_found = True
        else:
            new_piece_list.append((piece, color,position ))
    return new_piece_list, not is_piece_found


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
