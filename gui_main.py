import logging
import tkinter as tk
from gui.program_controller import ProgramController


def main():

    for handler in logging.root.handlers[:]:  # needed to reconfigure logging
        logging.root.removeHandler(handler)
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%H:%M:%S',  level=logging.DEBUG)

    root = tk.Tk()
    root.withdraw()
    app = ProgramController(r"C:\Users\Bogusz\inzynierka\player-simulator\saved_sessions\session1")
    root.mainloop()


if __name__ == '__main__':
    main()