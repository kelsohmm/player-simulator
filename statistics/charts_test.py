from time import sleep
from statistics.statistics_view import StatisticsView
from statistics.plot_builder import PlotBuilder

data_view = StatisticsView()

chart = PlotBuilder(data_view)

while True:
    chart.show_final_scores_plot()
    chart.show_move_usage_distribution_per_distance()
    sleep(1)
