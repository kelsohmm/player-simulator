import os
from unittest import TestCase
from mario_simulator import MarioSimulator

_mockInterfacePath = "interface.h"

class TestMarioSimulator(TestCase):
    def setUp(self):
        self.assertTrue(os.path.isfile(_mockInterfacePath))
        self.simulator = MarioSimulator(_mockInterfacePath)

    def test_startGame(self):
        self.assertTrue(self.simulator.startGame())

    def test_simulateTour(self):
        self.assertTrue(self.simulator.simulateTour(1))
