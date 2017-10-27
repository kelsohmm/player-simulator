import datetime
import os

from agents.agent_factory import agent_factory
from game.game_controller import GameController
from game.vm_host import VmHost

from config import *
from game.gameplay_job import GameplayJob
from game.supervised_vm import SupervisedVmDecorator

NO_GAMES = 200
MARIO_POSSIBLE_MOVES = [[0, 0, 0], [0, 0, 1], [0, 1, 0], [1, 0, 0], [0, 0, 1], [1, 1, 0]]
DUMP_DIR = os.path.join('gamestate_dumps', datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
if not os.path.exists(DUMP_DIR):
    os.makedirs(DUMP_DIR)

for game_number in range(NO_GAMES):
    logging.info("Starting job %d", game_number)
    game_vm = SupervisedVmDecorator(VmHost(MARIO_VM_CONFIG, mode='gui'))
    controller = GameController(game_vm, MARIO_VM_SCORE_RECT, ['A', 'LEFT', 'RIGHT'])
    player = agent_factory('AGENT_NN', MARIO_POSSIBLE_MOVES)

    job = GameplayJob(game_vm, controller, player, str(game_number))
    job.run()
