"""Game sprites module
"""
import os

import cv2
from numpy import ndarray

from app.model.pieces import *
from app.model.pieces.piece import Piece


pieces_names = {
    Pawn: "pawn.png",
    Queen: "queen.png",
    Tower: "rook.png",
    Horse: "knight.png",
    Bishop: "bishop.png",
    King: "king.png"
}

SPRITE_DIM = (16, 16)
SPRITES_PATH = "app/view/sprites/color/"

def load_sprite(piece_type: Piece, player: int) -> ndarray:
    """
        Loads a piece sprite.

        parameters:
            piece_type: A Piece class to identify the piece type.
            player: The player num (0 or 1).

        returns: A numpy ndarray with the piece sprite image.
    """
    color = ["white", "black"][player]
    piece_name = pieces_names[piece_type]
    path = os.path.join(SPRITES_PATH, color, piece_name)

    sprite = cv2.imread(path)
    sprite = cv2.cvtColor(sprite, cv2.COLOR_BGR2RGB)

    return sprite
