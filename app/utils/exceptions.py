"""Exceptions module
"""


class ImpossibleMoveException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class InvalidPlayerException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class NoPieceAtLocationException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class UnderXequeException(Exception):
    def __init__(self, *args):
        super().__init__(*args)
