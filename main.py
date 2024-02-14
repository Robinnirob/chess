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

    with open("chessboard_with_labels.svg", "r") as file:
        svg_content = file.read()
    return f"""
        <html>
            <body>
                {svg_content}
                <form action="/update" method="post">
                    <input type="text" name="pieces" placeholder="Piece positions" value="R,B,c1;N,B,b2">
                    <button type="submit">Update Board</button>
                </form>
            </body>
        </html>
        """


@app.post("/update", response_class=HTMLResponse)
async def update_chessboard(pieces: str = Form(...)):
    pieces_list = parse_pieces_input(pieces)
    draw_chessboard_with_labels(pieces_list)
    with open("chessboard_with_labels.svg", "r") as file:
        svg_content = file.read()
    return f"""
    <html>
        <body>
            {svg_content}
            <form action="/update" method="post">
                <input type="text" name="pieces" placeholder="Piece positions">
                <button type="submit">Update Board</button>
            </form>
        </body>
    </html>
    """


def parse_pieces_input(pieces_str):
    pieces_list = []
    for piece_str in pieces_str.split(';'):
        piece_info = piece_str.split(',')
        if len(piece_info) == 3:
            pieces_list.append((piece_info[0], piece_info[1], piece_info[2]))
    return pieces_list
