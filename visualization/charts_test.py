from time import sleep
import numpy as np

from visualization.score_chart import ScoreChart

data1 = np.asarray(list(range(1, 10000)))
data2 = np.asarray(list(range(500, 500000)))

chart = ScoreChart(data1)

chart.plot()
sleep(2)

chart.append(data2)
chart.plot()
sleep(5)
