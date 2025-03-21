"""Pawn piece class module
"""
import numpy as np

from app.model.pieces.piece import Piece
from app.utils.special_plays import SpecialPlays


class Pawn(Piece):
    def __init__(self, coordinates: tuple, player: int) -> None:
        """Pawn piece class"""
        super().__init__(coordinates, player)

        self.__first_move = True
    
    def possible_moveset(self, chess_table, last_move: tuple = None):
        moves = list()

        def __add_move(loc: tuple, cond: any):
            if cond(loc):
                moves.append(loc)

        if self.__first_move: # First move
            condition = lambda x: chess_table[x[0], x[1]] == 0 and\
                        chess_table[x[0] + 1, x[1]] == 0
            move = self.get_coordinates() + (-2, 0)
            __add_move(move, condition)
        
        if self.get_coordinates()[0] == 3 and last_move is not None: # En passant
            condition = lambda x: x[1] >= 0 and x[1] <= 7 and\
                        chess_table[x[0], x[1]] == 0 and\
                        chess_table[x[0] + 1, x[1]] == 2 and\
                        (x[0] + 1) == last_move[0] and x[1] == last_move[1]                
            move = self.get_coordinates() + (-1, -1)
            __add_move(move, condition)
            move = self.get_coordinates() + (-1, 1)
            __add_move(move, condition)

        # Forward move
        condition = lambda x: chess_table[x[0], x[1]] == 0
        move = self.get_coordinates() + (-1, 0)
        __add_move(move, condition)
        
        # Capture move
        condition = lambda x: x[1] >= 0 and x[1] <= 7 and chess_table[x[0], x[1]] == 2
        move = self.get_coordinates() + (-1, -1)
        __add_move(move, condition)
        move = self.get_coordinates() + (-1, +1)
        __add_move(move, condition)

        return np.array(moves, dtype=int)
    
    def move(self, dest: tuple, chess_table: np.ndarray, last_move: tuple):
        """
            Verifies if the destination is a valid movement and
            moves this piece to it if possible.

            params:
                dest: A tuple with destination coordinates.

            return: None.
        """
        init = self.get_coordinates()

        super()._move(dest, chess_table, last_move=last_move)
        self.__first_move = False

        if abs(init[1] - dest[1]) == 1 and\
            chess_table[dest[0], dest[1]] == 0 and\
            chess_table[dest[0] + 1, dest[1]] == 2:
            return SpecialPlays.EN_PASSANT
            
        if dest[0] == 0:
            return SpecialPlays.END_OF_BOARD
