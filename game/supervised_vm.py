import logging
import sys
import os
import psutil
import subprocess

from game.vm_host import VmHost

VM_SUPERVISOR_SCRIPT_FILEPATH = os.path.join('game','vm_process_supervisor.py')


class SupervisedVmDecorator:
    def __init__(self, vm_config, mode):
        assert(os.path.exists(VM_SUPERVISOR_SCRIPT_FILEPATH))
        self.vm = VmHost(vm_config, mode)
        self.supervisor_process = None

    def start(self):
        self.vm.start()
        self_pid = os.getpid()
        vm_pid = self.vm.machine.session_pid
        supervisor_pid = self._start_detached_process(self_pid, vm_pid)
        logging.info("Started supervisor for VM, self_pid: %d, vm_pid: %d, supervisor_pid: %d", self_pid , vm_pid , supervisor_pid)
        self.supervisor_process = psutil.Process(supervisor_pid)

    def _start_detached_process(self, self_pid, vm_pid):
        DETACHED_PROCESS = 0x00000008
        CREATE_NEW_PROCESS_GROUP = 0x00000200

        command = sys.executable or 'python'
        return subprocess.Popen([command, VM_SUPERVISOR_SCRIPT_FILEPATH, str(self_pid), str(vm_pid)],
                                close_fds = True,
                                creationflags= DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP).pid

    def stop(self):
        self.supervisor_process.kill()
        self.supervisor_process = None
        return self.vm.stop()

    def keys_up(self, keys):
        return self.vm.keys_up(keys)

    def keys_down(self, keys):
        return self.vm.keys_down(keys)

    def take_screen_shot(self):
        return self.vm.take_screen_shot()