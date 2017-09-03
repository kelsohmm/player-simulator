from collections import namedtuple


def _isNonEmptyBooleanIterable(iterable):
    return len(iterable) > 0 and \
            all( isinstance(elem, bool) for elem in iterable)


class Inputs(object):
    def __init__(self, activeInputs):
        """

        :type activeInputs: list[bool]
        """
        _isNonEmptyBooleanIterable(activeInputs)
        self.activeInputs = activeInputs

class Gamestate(object):
    def __init__(self, gamestate):
        """

        :type gamestate: list[bool]
        """
        _isNonEmptyBooleanIterable(gamestate)
        self.gamestate = gamestate