from agents.agent_factory import agent_factory
from game.supervised_vm import SupervisedVmDecorator
from game.vm_host import VmHost
from game.game_controller import GameController
from game.gameplay_job import GameplayJob


def create_vm_game_job(game_config, agent_config, mode='gui'):
    vm_config, controller_config = game_config

    vm = SupervisedVmDecorator(vm_config, mode)
    controller = GameController(vm, controller_config)
    agent = agent_factory(agent_config)

    GameplayJob(vm, controller, agent).run()
