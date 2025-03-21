"""Chess Table class module
"""
from copy import deepcopy

import numpy as np

from app.model.pieces import *
from app.model.pieces.piece import Piece
from app.utils.exceptions import *
from app.utils.special_plays import SpecialPlays


class ChessTable:
    def __init__(self):
        """Chess Table class."""
        self.__pieces = list()
        self.__last_move = None
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
                player_num = (2 * player_num) % 3
            
            for piece in self.__pieces[i]:
                if not piece.isalive():
                    continue

                loc = piece.get_coordinates(player_num == 2)
                table[loc[0], loc[1]] = player_num

        return table
    
    def get_table(self):
        return deepcopy(self.__pieces)

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
            if i != player:
                continue

            for j, piece in enumerate(self.__pieces[i]):
                if not piece.isalive():
                    continue

                if np.sum(piece.get_coordinates(i != player) == _from) == 2:
                    chosen = piece
                    break
            
            if chosen is not None:
                break

        if chosen is None:
            raise NoPieceAtLocationException("Any piece at given location.")
        
        reroll = deepcopy(self.__pieces)
        table = self.get_friends_n_enemies(player=i)
        if isinstance(chosen, King):
            special_play = chosen.move(to, table, towers=self.get_towers(player))
        elif isinstance(chosen, Pawn):
            special_play = chosen.move(to, table, last_move=self.get_last_move())
        else:
            special_play = chosen.move(to, table)

        if special_play is None:
            pass

        elif special_play == SpecialPlays.EN_PASSANT:
            to = (to[0] + 1, to[1])

        elif special_play == SpecialPlays.END_OF_BOARD:
            self.__pieces[i][j] = Queen(coordinates=to, player=i)

        elif special_play == SpecialPlays.ROCK:
            for vector in np.array([(0, 1), (0, -1)], dtype=int):
                tower = self.get_piece_by_loc(chosen.get_coordinates() + vector, turned=player==1)
                if isinstance(tower, Tower):
                    break

            tower.move_rock(vector * (-2))   

        captured = None
        for i in range(2):
            if i == player:
                continue

            for piece in self.__pieces[i]:
                if not piece.isalive():
                    continue

                if np.sum(piece.get_coordinates(i != player) == to) == 2:
                    captured = piece
                    break
            
            if captured is not None:
                captured.got_captured()
                break
        
        if self.is_under_xeque(player):
            self.__pieces = reroll
            raise UnderXequeException("This movement puts you under xeque.")

        self.__last_move = to

        return captured

    def get_piece_by_loc(self, coordinates: tuple, turned: bool = False) -> Piece:
        """
            Gets the piece located at given coordinates.

            params:
                coordinates: Location to look.
                turned: If the table is turned (second player look).

            return: A Piece object.
        """
        turn_player = 0 if turned else 1
        for i in range(2):
            for piece in self.__pieces[i]:
                if not piece.isalive():
                    continue

                if np.sum(piece.get_coordinates(i == turn_player) == coordinates) == 2:
                    return piece

    def get_king_loc(self, player: int) -> tuple:
        for piece in self.__pieces[player]:
            if isinstance(piece, King):
                return piece.get_coordinates()
            
    def get_towers(self, player: int) -> tuple:
        towers = list()
        for piece in self.__pieces[player]:
            if isinstance(piece, Tower) and piece.isalive() and not piece.was_moved():
                towers.append(piece.get_coordinates())
        
        return towers
    
    def get_last_move(self) -> tuple:
        if self.__last_move:
            return np.array([7, 7], dtype=int) - self.__last_move
            
    def is_under_xeque(self, player: int) -> bool:
        king_loc = np.array((7, 7), dtype=int) - self.get_king_loc(player)
        for piece in self.__pieces[(player + 1) % 2]:
            if not piece.isalive():
                continue
            moves = piece.possible_moveset(self.get_friends_n_enemies((player + 1) % 2))
            if len(moves) == 0:
                continue
            if 2 in np.sum(moves == king_loc, axis=1):
                return True
            
        return False
