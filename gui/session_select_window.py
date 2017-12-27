import tkinter as tk

_SELECT_WINDOW_TEXT = '''
Welcome to Player-Simulator!
Select a path with existing session to reopen,
or empty directory to initialize new session!
'''


def _select_dir_popup():
    from tkinter import filedialog
    return filedialog.askdirectory()


class SessionSelectWindow(tk.Frame):

    def __init__(self):
        super().__init__(padx=3)

        self.path_var = tk.StringVar()

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

        okButton = tk.Button(self, text="Open session")
        okButton.pack(side=tk.RIGHT, fill=tk.X)

    def select_path(self):
        self.path_var.set(_select_dir_popup())
