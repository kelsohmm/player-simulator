from time import sleep
from statistics.dataframe_view import DataFrameView
from statistics.plot_builder import PlotBuilder

data_view = DataFrameView()

chart = PlotBuilder(data_view)

while True:
    chart.show_final_scores_plot()
    chart.show_move_usage_distribution_per_distance()
    sleep(1)
