"""Exceptions module
"""

class ImpossibleMoveException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class InvalidPlayerException(Exception):
    def __init__(self, *args):
        super().__init__(*args)
