

def create_vm_game_job(game_config, agent, log_id='', mode='gui'):
    from game.supervised_vm import SupervisedVmDecorator
    from game.vm_host import VmHost
    from game.game_controller import GameController
    from game.gameplay_job import GameplayJob

    vm_config, controller_config = game_config
    vm = SupervisedVmDecorator(VmHost(vm_config, mode=mode))
    controller = GameController(vm, controller_config)
    return GameplayJob(vm, controller, agent, log_id)
