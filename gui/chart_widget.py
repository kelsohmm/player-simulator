import tkinter as tk
from PIL import Image, ImageTk


class ChartWidget(tk.Frame):
    def __init__(self, master, name, chart_array):
        super(ChartWidget, self).__init__(master)

        self.image = ImageTk.PhotoImage(Image.fromarray(chart_array))
        image_label = tk.Label(self, image=self.image)
        image_label.pack()

        name_label = tk.Label(self, text=name)
        name_label.pack()

