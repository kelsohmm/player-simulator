from ctypes import *

import config
from game_interface import Inputs, Gamestate

class _Inputs_CType(Structure):
    _fields_ = [
        ("activeInputs", POINTER(c_bool)),
        ("length", c_int)
    ]

    @staticmethod
    def fromPythonType(inputs):
        # type: (Inputs) -> _Inputs_CType
        inputsLength = len(inputs.activeInputs)
        InputsArrayType = c_bool * inputsLength
        cBoolArray = InputsArrayType(*(inputs.activeInputs))

        return _Inputs_CType(
            cBoolArray,
            inputsLength
        )

class _Gamestate_CType(Structure):
    _fields_ = [
        ("gamestate", POINTER(c_bool)),
        ("length", c_int)
    ]

    def toPythonType(self):
        # type: (_Gamestate_CType) -> Gamestate
        gamestateLength = self.length # type: int
        return Gamestate(
            [ self.gamestate[i] for i in range(gamestateLength)]
        )


class MarioLibraryProxy(object):
    def __init__(self):
        libPath = self._getLibraryPathBasedOnConfig()
        marioLib = cdll.LoadLibrary(libPath)

        self._initializeGamestateFunc, self._simulateTourFunc = self._extractTypedMethods(marioLib)

    def initializeGamestate(self):
        gamestateCType = self._initializeGamestateFunc()
        return gamestateCType.toPythonType()

    def simulateTour(self, inputs):
        inputsCType = _Inputs_CType.fromPythonType(inputs)
        gamestateCType = self._simulateTourFunc(inputsCType)
        return gamestateCType.toPythonType()

    def _extractTypedMethods(self, marioLib):
        simulateTourFunc = marioLib.simulateTour
        initializeGamestateFunc = marioLib.initializeGamestate

        simulateTourFunc.restype = _Gamestate_CType
        simulateTourFunc.args = [_Inputs_CType]

        initializeGamestateFunc.restype = _Gamestate_CType
        initializeGamestateFunc.args = [None]
        return initializeGamestateFunc, simulateTourFunc

    def _getLibraryPathBasedOnConfig(self):
        if not config.MOCK_GAME_LIBRARY:
            return config.REAL_LIBRARY_PATH
        else:
            return config.MOCK_LIBRARY_PATH
