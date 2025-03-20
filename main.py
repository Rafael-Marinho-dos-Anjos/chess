from app.view.board_view import *
from app.model.chess_table import ChessTable


table = ChessTable()
board = draw_board(table)
board = cv2.resize(board, (300, 300))
cv2.imshow("board", board)
cv2.waitKey(0)
