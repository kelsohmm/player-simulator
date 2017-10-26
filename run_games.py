from config import *
from game_controller import GameController
from gameplay_job import GameplayJob
from gamestate_repo import GamestateRepo
from random_agent import RandomAgent
from random_saving_agent import RandomSavingAgent
from supervised_vm import SupervisedVmDecorator
from vm_host import VmHost


NO_GAMES = 200

for game_number in range(NO_GAMES):
    logging.info("Starting job %d", game_number)
    game_vm = SupervisedVmDecorator(VmHost(MARIO_VM_CONFIG, mode='gui'))
    controller = GameController(game_vm, MARIO_VM_SCORE_RECT, ['A', 'LEFT', 'RIGHT'])
    player = RandomAgent(3)

    job = GameplayJob(game_vm, controller, player, str(game_number))
    job.run()