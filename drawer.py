from typing import List

import svgwrite

from data import Chessboard, Color, Position

SQUARE_COLORS = {
    Color.BLACK: 'darkgray',
    Color.WHITE: '#7A511D',
}

SUGGESTED_SQUARE_COLOR = 'pink'

PIECE_COLORS = {
    Color.BLACK: 'black',
    Color.WHITE: 'white'
}

TEXT_COLORS = {
    Color.BLACK: 'white',
    Color.WHITE: 'black'
}

board_size = 8
square_size = 50


def draw_chessboard_with_labels(chessboard: Chessboard, suggested_moves: List[Position] = [],
                                filename='chessboard_with_labels.svg'):
    dwg = svgwrite.Drawing(filename, profile='tiny', size=(board_size * square_size, board_size * square_size))

    for row in range(board_size):
        for col in range(board_size):
            position = Position(col, row)
            is_white = (position.row + position.col) % 2 == 0
            if is_white:
                fill = SQUARE_COLORS[Color.WHITE]
            else:
                fill = SQUARE_COLORS[Color.BLACK]
            draw_square(
                dwg=dwg,
                fill=fill,
                position=position,
                class_=f'chess-square pos-{position.to_string()}'
            )

    for move in suggested_moves:
        print("---" + str(move))
        draw_square(
            dwg=dwg,
            fill=SUGGESTED_SQUARE_COLOR,
            position=move,
            class_=f'chess-suggestion pos-{move.to_string()}'
        )

    for piece in chessboard.pieces_list.values():
        col = piece.position.col
        row = 7 - piece.position.row

        piece_color = PIECE_COLORS[piece.color]
        text_color = TEXT_COLORS[piece.color]

        center_x, center_y = (col + 0.5) * square_size, (row + 0.5) * square_size

        adjusted_y_position = center_y + (square_size * 0.1)

        pos_str = piece.position.to_string()
        dwg.add(dwg.circle(
            center=(center_x, center_y),
            r=square_size * 0.3,
            fill=piece_color,
            class_=f'chess-piece pos-{pos_str}')
        )

        dwg.add(dwg.text(
            piece.type.value,
            insert=(center_x, adjusted_y_position),
            fill=text_color,
            font_size='20',
            font_family='Arial',
            text_anchor="middle",
            class_=f'chess-piece-text pos-{pos_str}'
        ))

    dwg.save()


def draw_square(dwg, fill, position, class_: str | None = None):
    if class_ is None:
        dwg.add(dwg.rect(
            insert=(position.col * square_size, (7 - position.row) * square_size),
            size=(square_size, square_size),
            fill=fill)
        )
    else:
        dwg.add(dwg.rect(
            class_=class_,
            insert=(position.col * square_size, (7 - position.row) * square_size),
            size=(square_size, square_size),
            fill=fill)
        )
