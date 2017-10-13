from time import sleep

from config import *
from game_controller import GameController
from random_agent import RandomAgent
from vm_host import VmHost

game_vm = VmHost(MARIO_VM_CONFIG)
controller = GameController(game_vm, ['A', 'LEFT', 'RIGHT'])
player = RandomAgent(3)

while True:
    state, screen = controller.get_game_state()
    if(state == "FINISHED"):
        break
    else:
        inputs = player.react_to_new_game_screen(screen)
        controller.set_active_keys(inputs)
        sleep(0.1)

