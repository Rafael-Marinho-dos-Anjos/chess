"""This module generates the board view image
"""
import cv2
import numpy as np

from app.view.sprites import SPRITE_DIM, load_sprite
from app.model.pieces.piece import Piece
from app.model.chess_table import ChessTable


SQUARE_PADDING = 1
SQUARE_DIVISOR = 0

TABLE_SIZE = [(SPRITE_DIM[i] + 2 * SQUARE_PADDING) * 8 + SQUARE_DIVISOR * 7 for i in range(2)]

EVEN_SQUARE_COLOR = (62, 137, 72)
ODD_SQUARE_COLOR = (99, 199, 77)
SQUARE_DIVISOR_COLOR = (51, 115, 60)

TABLE_BASE = np.ones(TABLE_SIZE + [3], dtype=np.uint8)
TABLE_BASE[:, :] = SQUARE_DIVISOR_COLOR

for i in range(8):
    for j in range(8):
        if (i + j) % 2 == 0:
            color = EVEN_SQUARE_COLOR
        else:
            color = ODD_SQUARE_COLOR

        init = [(SPRITE_DIM[d] + 2 * SQUARE_PADDING + SQUARE_DIVISOR) * k for d, k in enumerate((i, j))]
        end = [(SPRITE_DIM[d] + 2 * SQUARE_PADDING) * (k + 1) + SQUARE_DIVISOR * k for d, k in enumerate((i, j))]

        TABLE_BASE[init[0]: end[0], init[1]: end[1]] = color


def draw_piece(piece: Piece, board:np.ndarray, turned: bool = False) -> np.ndarray:
    sprite = load_sprite(type(piece), piece.get_player())
    turned = turned if piece.get_player() == 0 else not turned

    base_point = [(SPRITE_DIM[d] + 2 * SQUARE_PADDING + SQUARE_DIVISOR) * k + SQUARE_DIVISOR for d, k in enumerate(piece.get_coordinates(turned))]

    board[base_point[0]: base_point[0] + sprite.shape[0], base_point[1]: base_point[1] + sprite.shape[1]][sprite[:, :] != (0, 0, 0)] = sprite[sprite[:, :] != (0, 0, 0)]

    return board


def draw_board(table: ChessTable, turned: bool = False) -> np.ndarray:
    pieces = table.get_table()
    board = None

    for i in range(2):
        for piece in pieces[i]:
            if board is None:
                board = draw_piece(piece, TABLE_BASE, turned)
            else:
                board = draw_piece(piece, board, turned)

    return board