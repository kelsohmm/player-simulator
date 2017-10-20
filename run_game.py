from datetime import datetime
from time import sleep

from config import *
from game_controller import GameController
from random_agent import RandomAgent
from vm_host import VmHost

game_vm = VmHost(MARIO_VM_CONFIG)
controller = GameController(game_vm, MARIO_VM_SCORE_RECT, ['A', 'LEFT', 'RIGHT'])
player = RandomAgent(3)

try:
    while True:
        state, score, screen = controller.get_game_state()
        if(state == "FINISHED"):
            print(datetime.now().time(), " --- Game finished!")
            break
        else:
            print(datetime.now().time(), " --- State:", state, " Score: ", score, end=' --- REACTION: ')
            inputs = player.react_to_new_game_screen(screen)
            controller.set_active_keys(inputs)
            sleep(0.1)
finally:
    game_vm.stop()

