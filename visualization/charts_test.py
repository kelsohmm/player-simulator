from time import sleep
from visualization.dataframe_view import DataFrameView
from visualization.score_chart import ScoreChart

data_view = DataFrameView()

chart = ScoreChart(data_view)

while True:
    chart.plot()
    sleep(1)
