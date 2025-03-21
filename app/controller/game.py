"""Game controller module.
"""
import cv2
from numpy import ndarray

from app.controller import MOVE_DELAY
from app.model.chess_table import ChessTable
from app.model.pieces.piece import Piece
from app.view.board_view import draw_board, draw_moves, draw_warning, get_square


class Game:
    def __init__(self):
        self.new_game()
    
    def new_game(self) -> None:
        """Start a new game."""
        self.__table = ChessTable()
        self.__turn = 0
        self.__selected = None
        self.__under_xeque = False
    
    def show(self, wait: int = 0) -> None:
        """
            Shows a window filled with the game frame.
        """
        self.__window = cv2.namedWindow("Chess", cv2.WINDOW_KEEPRATIO)
        cv2.setMouseCallback("Chess", self.__callback)
        cv2.imshow("Chess", self.__draw_frame())
        cv2.waitKey(wait)
        
    def __callback(self, *args) -> None:
        action = args[0]
        loc = list(reversed(args[1: 3]))
        loc = get_square(loc)

        if action == 1:
            if isinstance(self.__selected, Piece):
                self.__move(loc)
                self.__selected = None
            else:
                selected = self.__table.get_piece_by_loc(loc, self.__turn % 2 == 1)
                if selected and selected.get_player() == self.__turn % 2:
                    self.__selected = selected
                else:
                    self.__selected = loc

        elif action == 2:
            self.__selected = None

        else:
            return
        
        self.show()

    def __draw_frame(self) -> ndarray:
        player = self.__turn % 2

        board = draw_board(self.__table, player == 1)
        if self.__selected:
            board = draw_moves(self.__table, board, self.__selected, player == 1)
        if self.__under_xeque:
            board = draw_warning(self.__table, board, self.__turn % 2)

        return board

    def __move(self, loc) -> None:
        try:
            self.__table.move(self.__selected.get_coordinates(), loc, self.__turn % 2)
            self.show(MOVE_DELAY)
            self.__turn += 1

            self.__under_xeque = self.__table.is_under_xeque(self.__turn % 2)

        except Exception as e:
            print(e)