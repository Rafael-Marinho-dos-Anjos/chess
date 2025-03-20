"""This class implements a standart piece behaviour.
"""
import numpy as np

from app.utils.exceptions import *


class Piece:
    def __init__(self, coordinates: tuple, player: int):
        """Standart piece class"""
        if player not in [0, 1]:
            raise InvalidPlayerException("The player num must be 0 or 1")
        
        self.__player = player
        self.__coordinates = np.array(coordinates, dtype=int)
        self.__isalive = True

    def isalive(self) -> bool:
        """Checks if this piece is still in the game."""
        return self.__isalive
    
    def get_coordinates(self, turned: bool = False) -> np.ndarray:
        """
            Returns the current piece coordinate.

            params:
                turned: If it's True gets the coordinate turning the table (for
                player 2 movements).
            
            return: A numpy ndarray with the current coordinate of the piece.
        """
        return self.__coordinates if not turned else np.array([7, 7], dtype=int) - self.__coordinates
    
    def got_captured(self):
        self.__isalive = False

    def _possible_moveset(self, chess_table: np.ndarray) -> np.ndarray:
        """
            Calculates all possible moves for this piece.

            params:
                chess_table: A (8, 8) shaped numpy ndarray containing all
                friend and enemy pieces location (0 for unoccupied, 1 for
                friend and 2 for enemy).

            return: A numpy array with all possible moves.
        """
        # Implement this in the subclasses
        pass
    
    def _move(self, dest: np.ndarray, chess_table: np.ndarray) -> None:
        if 2 not in np.sum(self._possible_moveset(chess_table) == dest, axis=1):
            raise ImpossibleMoveException(f"Cannot move this piece to pos {[dest[0], dest[1]]}.")

        if not isinstance(dest, np.ndarray):
            np.array(dest, dtype=int)

        self.__coordinates = dest

    def get_player(self) -> int:
        return self.__player
