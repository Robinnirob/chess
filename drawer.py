import svgwrite


def draw_chessboard_with_labels(pieces, filename='chessboard_with_labels.svg'):
    board_size = 8
    square_size = 50
    dwg = svgwrite.Drawing(filename, profile='tiny', size=(board_size * square_size, board_size * square_size))

    for row in range(board_size):
        for col in range(board_size):
            if (row + col) % 2 == 0:
                fill = 'white'
            else:
                fill = 'gray'
            dwg.add(dwg.rect(insert=(col * square_size, row * square_size), size=(square_size, square_size), fill=fill))

    piece_labels = {'R': 'R', 'N': 'N', 'B': 'B', 'Q': 'Q', 'K': 'K', 'P': 'P'}

    for piece, color, position in pieces:
        print(f"piece, color, position: {piece}, {color}, {position}")
        col = ord(position[0]) - ord('a')
        row = 8 - int(position[1])
        if color == 'B':
            piece_color = 'black'
            text_color = 'white'
        else:
            piece_color = 'white'
            text_color = 'black'
        center_x, center_y = (col + 0.5) * square_size, (row + 0.5) * square_size

        adjusted_y_position = center_y + (square_size * 0.1)

        dwg.add(dwg.circle(center=(center_x, center_y), r=square_size * 0.3, fill=piece_color))

        dwg.add(dwg.text(piece_labels[piece], insert=(center_x, adjusted_y_position), fill=text_color, font_size='20', font_family='Arial', text_anchor="middle"))

    dwg.save()


pieces = [
    ('R', 'B', 'a1'), ('N', 'B', 'b1'), ('B', 'B', 'c1'), ('Q', 'B', 'd1'),
    ('K', 'B', 'e1'), ('B', 'B', 'f1'), ('N', 'B', 'g1'), ('R', 'B', 'h1'),
    ('P', 'B', 'a2'), ('P', 'B', 'b2'), ('P', 'B', 'c2'), ('P', 'B', 'd2'),
    ('P', 'B', 'e2'), ('P', 'B', 'f2'), ('P', 'B', 'g2'), ('P', 'B', 'h2'),
    ('P', 'N', 'a7'), ('P', 'N', 'b7'), ('P', 'N', 'c7'), ('P', 'N', 'd7'),
    ('P', 'N', 'e7'), ('P', 'N', 'f7'), ('P', 'N', 'g7'), ('P', 'N', 'h7'),
    ('R', 'N', 'a8'), ('N', 'N', 'b8'), ('B', 'N', 'c8'), ('Q', 'N', 'd8'),
    ('K', 'N', 'e8'), ('B', 'N', 'f8'), ('N', 'N', 'g8'), ('R', 'N', 'h8')
]

draw_chessboard_with_labels(pieces)
