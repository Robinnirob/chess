from typing import List

import uvicorn
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from data import get_chessboard_initialized, Color, Movement, Chessboard, PieceInfo, PieceType, Position
from drawer import draw_chessboard_with_labels

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

suggestion_js_script = """
    <script>
        function add_suggestion_behavior(items) {
            for (var i = 0; i < items.length; i++) {
                classes = items[i].classList
                for (var j = 0; j < classes.length; j++) {
                    var cls = classes[j]
                    if (cls.startsWith('pos-')) {
                       let pos = cls.substr('pos-'.length)
                       items[i].onclick = () => gotoSuggestion(pos)
                    }
                } 
            }
        }
        function gotoSuggestion(pos) {
            form = document.getElementById("chess-suggestion-form")
            input = document.getElementById("chess-suggestion-input")
            input.value = pos
            form.submit()
        }

        let elements = document.getElementsByClassName('chess-square')
        add_suggestion_behavior(elements)
        elements = document.getElementsByClassName('chess-piece')
        add_suggestion_behavior(elements)
        elements = document.getElementsByClassName('chess-piece-text')
        add_suggestion_behavior(elements)
        elements = document.getElementsByClassName('chess-suggestion')
        addOnlickOnItems(elements)
    </script>
"""


def form_suggestion(chessboard, color=Color.WHITE.value):
    return f"""
    <form id='chess-suggestion-form' action="/suggestion" method="post">
        <input id='chess-suggestion-input' type="text" name="position" placeholder="Position">
        <input type="hidden" name="chessboard" value="{chessboard.to_string()}"/>
        <input type="hidden" name="next_player" value="{color}"/>
        <button type="submit">Suggestion</button>
    </form>
"""


def form_move(chessboard, next_player, pos):
    return f"""
    <form action="/update" method="post">
        <input type="text" name="movement" placeholder="Mouvement" value="{pos}" autofocus>
        <input type="hidden" name="chessboard" value="{chessboard.to_string()}"/>
        <input type="hidden" name="next_player" value="{next_player}"/>
        <button type="submit">Update Board</button>
    </form> 
    """


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
                {form_move(chessboard, Color.WHITE.value, mv_suggested.to_string())}
                {form_suggestion(chessboard)}
            </body>
        {suggestion_js_script}
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

    chessboard, error_msg = do_movement(chessboard=chessboard, movement=movement, player=next_player)
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
            {form_move(chessboard, next_player.value, "")}
            {form_suggestion(chessboard, next_player.value)}
            <div style='color: red'>{error_msg}</div>
            <button onclick='window.location = "/";'>Nouvelle partie</button>
            <div style='color: purple'>Trait aux {next_player.toLabel()}s</div>
        </body>
        {suggestion_js_script}
    </html>
    """


@app.post("/suggestion", response_class=HTMLResponse)
async def update_chessboard(
        chessboard_str: str = Form(..., alias='chessboard'),
        position_str: str = Form(..., alias='position'),
        next_player_str: str = Form(..., alias='next_player')):
    chessboard = Chessboard.from_str(chessboard_str)
    position = Position.from_str(position_str)
    next_player = Color.from_str(next_player_str)

    piece_expected_to_move = chessboard.getPiece(position)
    if piece_expected_to_move is not None:
        print(f'piece_expected_to_move {piece_expected_to_move}')
        error_msg = ""
        suggestion_pos = "" if next_player != piece_expected_to_move.color else position_str
        moves = extract_authorized_squares(chessboard=chessboard, piece=piece_expected_to_move)
    else:
        error_msg = "Pas de pièce à cette position"
        suggestion_pos = ""
        moves = []

    print(f'suggestion_pos {suggestion_pos}')
    draw_chessboard_with_labels(chessboard, moves)
    with open("chessboard_with_labels.svg", "r") as file:
        svg_content = file.read()

    return f"""
    <html>
        <body>
            {svg_content}
            {form_move(chessboard, next_player.value, suggestion_pos)}
            {form_suggestion(chessboard, next_player.value)}
            <div>{[f'{position_str}-{move.to_string()}' for move in moves]}</div>
            <div style='color: red'>{error_msg}</div>
            <button onclick='window.location = "/";'>Nouvelle partie</button>
            <div style='color: purple'>Trait aux {next_player.toLabel()}s</div>
        </body>
        {suggestion_js_script}
        {suggestion_js_script}
    </html>
    """


def do_movement(chessboard: Chessboard, movement: Movement, player: Color):
    new_piece_list = []

    if movement.target.col < 0 or movement.target.col > 7 or movement.target.row < 0 or movement.target.row > 7:
        print("Out of board")
        return chessboard, f"La position de destination est hors du plateau: {movement.target.to_string()}"

    piece = chessboard.getPiece(movement.init)

    if piece is None:
        print("No piece found")
        return chessboard, f"La pièce {movement.init.to_string()} n'a pas été trouvée"

    if piece.color != player:
        print("Bad user has played")
        return chessboard, f"C'est au joueur {player.toLabel()} de jouer"
    if not is_movement_authorized(piece, movement, chessboard):
        print("Unauthorized move")
        return chessboard, f"Ce coup n'est pas autorisé: {movement.target.to_string()}"

    del chessboard.pieces_list[piece.position]
    piece.position = movement.target
    chessboard.pieces_list[movement.target] = piece

    return chessboard, ""


def is_movement_authorized(piece: PieceInfo, movement: Movement, chessboard: Chessboard) -> bool:
    if piece.type == PieceType.PAWN:
        authorized_squares = extract_authorized_squares(chessboard=chessboard, piece=piece)
        return movement.target in authorized_squares

    return True


def extract_authorized_squares(chessboard: Chessboard, piece: PieceInfo) -> List[Position]:
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
        right_diag_piece = chessboard.getPiece(piece.position.offset(1, direction_value))
        print(f"---left: {left_diag_piece}:{piece.position.offset(-1, direction_value)}")
        print(f"---right: {right_diag_piece}:{piece.position.offset(1, direction_value)}")
        if left_diag_piece is not None and left_diag_piece.color != piece.color:
            authorized_squares.append(left_diag_piece.position)
        if right_diag_piece is not None and right_diag_piece.color != piece.color:
            authorized_squares.append(right_diag_piece.position)
        return authorized_squares
    return []


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
