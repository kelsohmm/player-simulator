import tkinter as tk
from gui.controller import Controller


def main():

    root = tk.Tk()
    app = Controller(r"C:\Users\Bogusz\inzynierka\player-simulator\saved_sessions\session1")
    root.mainloop()


if __name__ == '__main__':
    main()