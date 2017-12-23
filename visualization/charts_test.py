from time import sleep
from visualization.dataframe_view import DataFrameView
from visualization.plot_builder import PlotBuilder

data_view = DataFrameView()

chart = PlotBuilder(data_view)

while True:
    chart.show_average_final_score_plot()
    sleep(1)
