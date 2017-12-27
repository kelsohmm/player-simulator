import tkinter as tk
from gui.session_select_window import SessionSelectWindow


def main():

    root = tk.Tk()
    root.geometry("300x200+300+300")
    app = SessionSelectWindow(lambda session: None)
    root.mainloop()


if __name__ == '__main__':
    main()