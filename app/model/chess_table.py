"""Chess Table class module
"""
import numpy as np

from app.model.pieces.pawn import Pawn
from app.model.pieces.bishop import Bishop
from app.model.pieces.tower import Tower
from app.model.pieces.horse import Horse
from app.model.pieces.king import King
from app.model.pieces.queen import Queen
from app.utils.exceptions import *


class ChessTable:
    def __init__(self):
        """Chess Table class."""
        self.__pieces = list()
        self.reset_table()

    def reset_table(self):
        """Reset all pieces location for a new game."""
        self.__pieces = [list() for i in range(2)]

        locs = {
            Pawn: [(6, i) for i in range(8)],
            Tower: [(7, 0), (7, 7)],
            Horse: [(7, 1), (7, 6)],
            Bishop: [(7, 2), (7, 5)]
        }

        for i in range(2):
            locs[King] = [(7, 4 - i)]
            locs[Queen] = [(7, 3 + i)]
            
            for piece_type in locs.keys():
                for loc in locs[piece_type]:
                    self.__pieces[i].append(
                        piece_type(coordinates=loc, player=i)
                    )
    
    def get_friends_n_enemies(self, player: int) -> np.ndarray:
        """
            Returns a (8, 8) shaped numpy ndarray with all friends (filled with 1)
            and enemies (filled with 2) locations.

            params:
                player: An int number indicating the player (0 or 1).

            returns: A numpy ndarray with all friendly and enemy pieces locations.
        """
        if player not in [0, 1]:
            raise InvalidPlayerException("The player num must be 0 or 1")
        
        inverted = player == 1
        table = np.zeros((8, 8), dtype=int)

        for i in range(2):
            player_num = 1 if i == 0 else 2

            if inverted:
                player_num = (2 * player) % 3
            
            for piece in self.__pieces[i]:
                if not piece.isalive():
                    continue

                loc = piece.get_coordinates(inverted)
                table[loc[0], loc[1]] = player_num

        return table
    
    def get_table(self):
        # TODO -> Returns a matrix with all pieces information
        pass

    def move(self, _from: tuple, to: tuple, player: int) -> None:
        """
            Move an piece located at specifc coordinate to another.

            params:
                _from: Current coordinate.
                to: Desired coordinate.
                player: An int number indicating the player (0 or 1).

            return: An Piece object if it's captured else None.
        """
        chosen = None
        for i in range(2):
            if i == player:
                continue

            for piece in self.__pieces:
                if not piece.isalive():
                    continue

                if np.sum(piece.get_coordinates(i == 1)) == 2:
                    chosen = piece
                    break
            
            if chosen is not None:
                break

        if chosen is None:
            raise NoPieceAtLocationException("Any piece at given location.")
        
        table = self.get_friends_n_enemies(player=i)
        chosen.move(to, table)

        captured = None
        for i in range(2):
            if i != player:
                continue

            for piece in self.__pieces:
                if not piece.isalive():
                    continue

                if np.sum(piece.get_coordinates(i == 1)) == 2:
                    captured = piece
                    break
            
            if captured is not None:
                captured.got_captured()
                break

        return captured
