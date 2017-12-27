import tkinter as tk
from session import Session, verify_session_path

_SELECT_WINDOW_TEXT = '''
Welcome to Player-Simulator!
Select a path with existing session to reopen,
or empty directory to initialize new session!
'''

def show_error(message):
    from tkinter import messagebox
    messagebox.showerror('Error', message)

def _select_dir_popup():
    from tkinter import filedialog
    return filedialog.askdirectory()


class SessionSelectWindow(tk.Frame):

    def __init__(self, callback):
        super().__init__(padx=3)
        self.path_var = tk.StringVar()
        self.callback = callback
        self.initUI()


    def initUI(self):

        self.master.title("Player Simulator - select session")

        window_text = tk.Label(self, text=_SELECT_WINDOW_TEXT)
        window_text.pack()

        dir_open_subframe = tk.Frame(self, relief=tk.RAISED)

        dir_entry = tk.Entry(dir_open_subframe, textvariable=self.path_var)
        dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        select_button = tk.Button(dir_open_subframe, text="Select", command=self.select_path)
        select_button.pack(side=tk.LEFT, fill=tk.NONE)

        dir_open_subframe.pack(fill=tk.BOTH, expand=True)

        self.pack(fill=tk.BOTH, expand=True)

        ok_button = tk.Button(self, text="Open session", command=self._create_session)
        ok_button.pack(side=tk.RIGHT, fill=tk.X)

    def select_path(self):
        self.path_var.set(_select_dir_popup())

    def _create_session(self):
        path = self.path_var.get()
        if verify_session_path(path):
            self.callback(path)
        else:
            show_error("Select empty directory to create a new session, or reopen existing session directory.")

    def quit(self):
        self._root().destroy()