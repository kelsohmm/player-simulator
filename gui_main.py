import tkinter as tk
from gui.program_controller import ProgramController


def main():

    root = tk.Tk()
    root.withdraw()
    app = ProgramController(r"C:\Users\Bogusz\inzynierka\player-simulator\saved_sessions\session1")
    root.mainloop()


if __name__ == '__main__':
    main()