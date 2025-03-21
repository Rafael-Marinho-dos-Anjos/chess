"""King piece class module
"""
import numpy as np

from app.model.pieces.piece import Piece
from app.utils.special_plays import SpecialPlays


class King(Piece):
    def __init__(self, coordinates: tuple, player: int) -> None:
        """King piece class"""
        super().__init__(coordinates, player)

        self.__first_move = True
    
    def possible_moveset(self, chess_table, towers: tuple = None):
        moves = list()

        def __add_move(loc: tuple, cond: any):
            if cond(loc):
                moves.append(loc)
        
        condition = lambda x: chess_table[x[0], x[1]] in (0, 2)
        directions = [
            (-1, 0), # Forward
            (1, 0), # Backward
            (0, 1), # Right
            (0, -1), # Left
            (-1, 1), # Forward right
            (-1, -1), # Forward left
            (1, 1), # Backward right
            (1, -1) # Backward left
        ]

        for direction in directions:
            move = self.get_coordinates() + direction

            if (move[0] >= 0 and move[0] <= 7 and move[1] >= 0 and move[1] <= 7):
                __add_move(move, condition)
        
        if self.__first_move and towers and len(towers) > 0: # Rock
            condition = lambda x: chess_table[x[0], x[1]] != 0

            for tower in towers:
                move = self.get_coordinates()
                vector = tower - move
                vector = (vector / abs(np.sum(vector))).astype(int)
                move = move + vector
                
                can_rock = True
                while (move != tower).any():
                    if condition(move):
                        can_rock = False
                        break

                    move = move + vector
                
                if can_rock:
                    moves.append(move - vector)

        return np.array(moves, dtype=int)
    
    def move(self, dest: tuple, chess_table: np.ndarray, towers: tuple):
        """
            Verifies if the destination is a valid movement and
            moves this piece to it if possible.

            params:
                dest: A tuple with destination coordinates.

            return: None.
        """
        _from = self.get_coordinates().copy()
        super()._move(dest, chess_table, towers=towers)

        self.__first_move = False

        if np.sum(np.abs(_from - self.get_coordinates())) > 1:
            return SpecialPlays.ROCK
