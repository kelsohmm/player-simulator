import tkinter as tk
from gui.controller import Controller


def main():

    root = tk.Tk()
    app = Controller()
    root.mainloop()


if __name__ == '__main__':
    main()