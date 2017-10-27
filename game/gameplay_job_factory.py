from agents.agent_factory import agent_factory
from game.supervised_vm import SupervisedVmDecorator
from game.vm_host import VmHost
from game.game_controller import GameController
from game.gameplay_job import GameplayJob


def create_vm_game_job(game_config, agent_config, log_id='', mode='gui'):

    vm_config, controller_config = game_config
    vm = SupervisedVmDecorator(VmHost(vm_config, mode=mode))
    controller = GameController(vm, controller_config)
    agent = agent_factory(agent_config)

    GameplayJob(vm, controller, agent, log_id).run()
