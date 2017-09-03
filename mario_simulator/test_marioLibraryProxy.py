from unittest import TestCase
from game_interface import *
from mario_library_proxy import MarioLibraryProxy
import config

class TestMarioLibraryProxy(TestCase):
    def setUp(self):
        config.MOCK_GAME_LIBRARY = True
        self.sut = MarioLibraryProxy()

    def test_initializeGamestateReturnsGamestate(self):
        initialState = self.sut.initializeGamestate()
        self.assertIsInstance(
            initialState,
            Gamestate
        )

    def test_simulateTourWithAnyParametersReturnsGamestate(self):
        inputs = Inputs([True, False, True, True])

        self.assertIsInstance(
            self.sut.simulateTour(inputs),
            Gamestate
        )

    def test_gamestateShapeIsConstant(self):
        inputs1 = Inputs([True, False, True, True])
        inputs2 = Inputs([False, True, True, False])

        initialState = self.sut.initializeGamestate() # type: Gamestate
        gamestate1 = self.sut.simulateTour(inputs1) # type: Gamestate
        gamestate2 = self.sut.simulateTour(inputs2) # type: Gamestate

        self.assertTrue(
            initialState.gamestate ==
            gamestate1.gamestate ==
            gamestate2.gamestate
        )
