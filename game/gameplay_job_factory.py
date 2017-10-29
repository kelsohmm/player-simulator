from agents.agent_factory import agent_factory
from game.supervised_vm import SupervisedVmDecorator
from game.vm_host import VmHost
from game.game_controller import GameController
from game.gameplay_job import GameplayJob


def create_vm_game_job(args):
    game_config, agent_name, save_path, mode = args
    vm_config, controller_config, possible_moves = game_config

    vm = SupervisedVmDecorator(vm_config, mode)
    controller = GameController(vm, controller_config)
    agent = agent_factory(agent_name, possible_moves, save_path)

    GameplayJob(vm, controller, agent).run()
