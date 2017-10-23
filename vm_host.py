import itertools
from time import sleep
from virtualbox import VirtualBox, Session
from virtualbox.library import LockType, SessionType, BitmapFormat
import scipy.misc
import numpy as np

from config import MARIO_VM_CONFIG

_SCANCODES = {
    'ESC': [[0x01], [0x81]],
    '1': [[0x02], [0x82]],
    '2': [[0x03], [0x83]],
    '3': [[0x04], [0x84]],
    '4': [[0x05], [0x85]],
    '5': [[0x06], [0x86]],
    '6': [[0x07], [0x87]],
    '7': [[0x08], [0x88]],
    '8': [[0x09], [0x89]],
    '9': [[0x0A], [0x8A]],
    '0': [[0x0B], [0x8B]],
    '-': [[0x0C], [0x8C]],
    '=': [[0x0D], [0x8D]],
    'BKSP': [[0x0E], [0x8E]],
    '\b': [[0x0E], [0x8E]],
    'TAB': [[0x0F], [0x8F]],
    '\t': [[0x0F], [0x8F]],
    'Q': [[0x10], [0x90]],
    'W': [[0x11], [0x91]],
    'E': [[0x12], [0x92]],
    'R': [[0x13], [0x93]],
    'T': [[0x14], [0x94]],
    'Y': [[0x15], [0x95]],
    'U': [[0x16], [0x96]],
    'I': [[0x17], [0x97]],
    'O': [[0x18], [0x98]],
    'P': [[0x19], [0x99]],
    '[': [[0x1A], [0x9A]],
    ']': [[0x1B], [0x9B]],
    'ENTER': [[0x1C], [0x9C]],
    '\r': [[0x1C], [0x9C]],
    '\n': [[0x1C], [0x9C]],
    'CTRL': [[0x1D], [0x9D]],
    'A': [[0x1E], [0x9E]],
    'S': [[0x1F], [0x9F]],
    'D': [[0x20], [0xA0]],
    'F': [[0x21], [0xA1]],
    'G': [[0x22], [0xA2]],
    'H': [[0x23], [0xA3]],
    'J': [[0x24], [0xA4]],
    'K': [[0x25], [0xA5]],
    'L': [[0x26], [0xA6]],
    ';': [[0x27], [0xA7]],
    '\'': [[0x28], [0xA8]],
    '`': [[0x29], [0xA9]],
    'LSHIFT': [[0x2A], [0xAA]],
    '\\': [[0x2B], [0xAB]],
    'Z': [[0x2C], [0xAC]],
    'X': [[0x2D], [0xAD]],
    'C': [[0x2E], [0xAE]],
    'V': [[0x2F], [0xAF]],
    'B': [[0x30], [0xB0]],
    'N': [[0x31], [0xB1]],
    'M': [[0x32], [0xB2]],
    ',': [[0x33], [0xB3]],
    '.': [[0x34], [0xB4]],
    '/': [[0x35], [0xB5]],
    'RSHIFT': [[0x36], [0xB6]],
    'PRTSC': [[0x37], [0xB7]],
    'ALT': [[0x38], [0xB8]],
    'SPACE': [[0x39], [0xB9]],
    ' ': [[0x39], [0xB9]],
    'CAPS': [[0x3A], [0xBA]],
    'F1': [[0x3B], [0xBB]],
    'F2': [[0x3C], [0xBC]],
    'F3': [[0x3D], [0xBD]],
    'F4': [[0x3E], [0xBE]],
    'F5': [[0x3F], [0xBF]],
    'F6': [[0x40], [0xC0]],
    'F7': [[0x41], [0xC1]],
    'F8': [[0x42], [0xC2]],
    'F9': [[0x43], [0xC3]],
    'F10': [[0x44], [0xC4]],
    'F11': [[0x57], [0xD7]],
    'F12': [[0x58], [0xD8]],
    'NUM': [[0x45], [0xC5]],
    'SCRL': [[0x46], [0xC6]],
    'HOME': [[0x47], [0xC7]],
    'UP': [[0x48], [0xC8]],
    'PGUP': [[0x49], [0xC9]],
    'MINUS': [[0x4A], [0xCA]],
    'LEFT': [[0x4B], [0xCB]],
    'CENTER': [[0x4C], [0xCC]],
    'RIGHT': [[0xE0, 0x4D], [0xE0, 0xCD]],
    'PLUS': [[0x4E], [0xCE]],
    'END': [[0x4F], [0xCF]],
    'DOWN': [[0x50], [0xD0]],
    'PGDN': [[0x51], [0xD1]],
    'INS': [[0x52], [0xD2]],
    'DEL': [[0x53], [0xD3]],
}


def take_key_down_scancode(key):
    return _SCANCODES[key][0]


def take_key_up_scancode(key):
    return _SCANCODES[key][1]


class VmHost:
    _BITMAP_FORMAT = BitmapFormat.rgba
    _ONLY_SCREEN_ID = 0
    _SNAP_RESTORE_TIMEOUT = 30 * 1000
    _VM_STARTUP_TIMEOUT = 60 * 1000
    _GUEST_SESSION_NAME = '__GUEST_SESSION__'

    def __init__(self, vm_config, mode='gui'):
        vm_name, snap_name, window_rect = vm_config
        vbox = VirtualBox()
        self.session = Session()
        self.machine = vbox.find_machine(vm_name)
        self.window_rect = window_rect
        self.snap_name = snap_name
        self.mode = mode


    def start(self):
        self._set_snapshot()
        self._launch_vm()

    def _set_snapshot(self):
        self.machine.lock_machine(self.session, LockType.write)
        assert (self.session.type_p == SessionType.write_lock)
        progress = self.session.machine.restore_snapshot(self.machine.find_snapshot(self.snap_name))

        progress.wait_for_completion(self._SNAP_RESTORE_TIMEOUT)
        if not progress.completed:
            raise TimeoutError

        self.session.unlock_machine()

    def _launch_vm(self):
        progress = self.machine.launch_vm_process(self.session, type_p=self.mode)
        progress.wait_for_completion(self._VM_STARTUP_TIMEOUT)
        if not progress.completed:
            raise TimeoutError

    def stop(self):
        progress = self.session.console.power_down()
        progress.wait_for_completion(-1)

    def take_screen_shot(self):
        display = self.session.console.display
        window_width, window_height, window_x, window_y = self.window_rect
        screen_height, screen_width, _, _, _, _ = display.get_screen_resolution(self._ONLY_SCREEN_ID)

        screen_array = display.take_screen_shot_to_array(self._ONLY_SCREEN_ID, screen_height, screen_width,
                                                         self._BITMAP_FORMAT)
        array_np = np.frombuffer(screen_array, dtype=np.uint8)
        array_np = np.reshape(array_np, (screen_width, screen_height, 4))
        return array_np[
               window_y:window_y + window_height,
               window_x:window_x + window_width,
               :3]  # discard alpha chanel

    def keys_down(self, keys):
        scancodes_lists = map(lambda key: take_key_down_scancode(key), keys)
        scancodes_unique = set(itertools.chain.from_iterable(scancodes_lists))
        self.session.console.keyboard.put_scancodes(list(scancodes_unique))

    def keys_up(self, keys):
        scancodes_lists = map(lambda key: take_key_up_scancode(key), keys)
        scancodes_unique = set(itertools.chain.from_iterable(scancodes_lists))
        self.session.console.keyboard.put_scancodes(list(scancodes_unique))


