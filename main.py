import uvicorn
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from data import get_chessboard_initialized, Color, Movement, Position, Chessboard, PieceInfo, PieceType
from drawer import draw_chessboard_with_labels

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def get_chessboard():
    chessboard = get_chessboard_initialized()
    draw_chessboard_with_labels(chessboard)

    with open("chessboard_with_labels.svg", "r") as file:
        svg_content = file.read()
    mv_suggested = Movement.from_strs('a2', 'a3')
    return f"""
        <html>
            <body>
                {svg_content}
                <form action="/update" method="post">
                    <input type="text" name="movement" placeholder="Mouvement" value="{mv_suggested.to_string()}">
                    <input type="hidden" name="chessboard" value="{chessboard.to_string()}"/>
                    <input type="hidden" name="next_player" value="{Color.WHITE.value}"/>
                    <button type="submit">Update Board</button>
                </form>
            </body>
        </html>
        """



@app.post("/update", response_class=HTMLResponse)
async def update_chessboard(
        chessboard_str: str = Form(..., alias='chessboard'),
        movement_str: str = Form(..., alias='movement'),
        next_player_str: str = Form(..., alias='next_player')):
    chessboard = Chessboard.from_str(chessboard_str)
    movement = Movement.from_str(movement_str)
    next_player = Color.from_str(next_player_str)

    print(f"aaaaaaaaaaaaaaaaaaaa {chessboard.to_string()}")

    chessboard, error_msg = do_movement(chessboard, movement, next_player)
    draw_chessboard_with_labels(chessboard)
    with open("chessboard_with_labels.svg", "r") as file:
        svg_content = file.read()

    if error_msg == "":
        if next_player == Color.WHITE:
            next_player = Color.BLACK
        else:
            next_player = Color.WHITE

    return f"""
    <html>
        <body>
            {svg_content}
            <form action="/update" method="post">
                <input type="text" name="mouvement_requested" placeholder="Mouvement">
                <input type="hidden" name="chessboard" value="{chessboard.to_string()}"/>
                <input type="hidden" name="next_player" value="{next_player.value}"/>
                <button type="submit">Update Board</button>
            </form>
            <div style='color: red'>{error_msg}</div>
            <div style='color: purple'>Trait aux {next_player.toLabel()}s</div>
        </body>
    </html>
    """


def do_movement(chessboard, movement, player):
    new_piece_list = []

    if movement.target.col < 0 or movement.target.col > 7 or movement.target.row < 0 or movement.target.row > 7:
        return chessboard, f"La position de destination est hors du plateau: {movement.target.to_string()}"

    piece = chessboard.pieces_list[movement.init]

    if piece is None:
        return new_piece_list, f"La pièce {movement.init.to_string()} n'a pas été trouvée"

    if piece.color != player:
        return chessboard, f"C'est au joueur {player.toLabel()} de jouer"
    if not is_movement_authorized(piece, movement):
        return chessboard, f"Ce coup n'est pas autorisé: {movement.target.to_string()}"

    del chessboard.pieces_list[piece.position]
    piece.position = movement.target
    chessboard.pieces_list[movement.target] = piece

    return chessboard, ""


def is_movement_authorized(piece: PieceInfo, movement: Movement, chessboard: Chessboard) -> bool:
    if piece.type == PieceType.PAWN:
        direction_value = 1 if piece.color == Color.WHITE else -1
        is_initial_position = (
                (piece.color == Color.WHITE and piece.position.row == 1) or
                (piece.color == Color.BLACK and piece.position.row == 6)
        )
        authorized_squares = [piece.position.offset(0, direction_value)]
        if is_initial_position:
            authorized_squares.append(piece.position.offset(0, direction_value * 2))

        left_diag_piece = chessboard.getPiece(piece.position.offset(-1, direction_value))
        right_diag_piece = chessboard.getPiece(piece.position.offset(-1, direction_value))
        if left_diag_piece is not None and left_diag_piece.color != piece.color:
            authorized_squares.append(left_diag_piece.position)
        if right_diag_piece is not None and right_diag_piece.color != piece.color:
            authorized_squares.append(right_diag_piece.position)

        return movement.target in authorized_squares

    return True


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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
