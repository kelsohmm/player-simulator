import matplotlib.pyplot as plt


class ChartsWindow:
    def __init__(self, window_name, chart_builders, nrows=2, ncols=2):
        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, num=window_name)

        col = 0
        row = 0
        for chart_name in chart_builders.keys():
            axes[row, col].set_title(chart_name)
            chart_builders[chart_name](ax=axes[row, col])

            col += 1
            if col >= ncols:
                col = 0
                row += 1

        plt.show()
