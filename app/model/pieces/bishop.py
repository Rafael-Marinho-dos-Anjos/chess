"""Bishop piece class module
"""
import numpy as np

from app.model.pieces.piece import Piece


class Bishop(Piece):
    def __init__(self, coordinates: tuple, player: int) -> None:
        """Bishop piece class"""
        super().__init__(coordinates, player)
    
    def _possible_moveset(self, chess_table):
        moves = list()

        def __add_move(loc: tuple, cond: any):
            if cond(loc):
                moves.append(loc)
        
        # Forward right move
        condition = lambda x: chess_table[x[0], x[1]] in (0, 2)
        directions = [
            (-1, 1), # Forward right
            (-1, -1), # Forward left
            (1, 1), # Backward right
            (1, -1) # Backward left
        ]

        for direction in directions:
            move = self.get_coordinates() + direction
            while (move[0] >= 0 and move[0] <= 7 and move[1] >= 0 and move[1] <= 7):
                if chess_table[move[0], move[1]] == 1:
                    break

                __add_move(move, condition)

                if chess_table[move[0], move[1]] == 2:
                    break

                move = move + direction
    
    def move(self, dest: tuple, chess_table: np.ndarray):
        """
            Verifies if the destination is a valid movement and
            moves this piece to it if possible.

            params:
                dest: A tuple with destination coordinates.

            return: None.
        """
        super()._move(dest, chess_table)
        self.__first_move = False
