"""This module implements a enumerator to identify special plays.
"""
from enum import Enum

class SpecialPlays(Enum):
    EN_PASSANT = 0
    END_OF_BOARD = 1
    ROCK = 2
