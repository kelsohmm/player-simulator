import tkinter as tk

from gui.chart_widget import ChartWidget


class ChartsWindow(tk.Toplevel):
    def __init__(self, window_name, charts, columns=3):
        super(ChartsWindow, self).__init__()
        self.title(window_name)

        chart_widgets = [ChartWidget(self, chart_name, charts[chart_name])
                         for chart_name in charts.keys()]

        curr_col = 0
        curr_row = 0
        for chart in chart_widgets:
            chart.grid(row=curr_row, column=curr_col)

            curr_col += 1
            if curr_col >= columns:
                curr_row += 1
                curr_col = 0
