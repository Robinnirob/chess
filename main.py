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


@app.get("/", response_class=HTMLResponse)
async def get_chessboard():
    pieces = [('R', 'B', 'a1'), ('N', 'B', 'b1')]
    draw_chessboard_with_labels(pieces)


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
