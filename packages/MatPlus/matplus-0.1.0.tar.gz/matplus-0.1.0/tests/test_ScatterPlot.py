import numpy as np
from MatPlus.ScatterPlot import ScatterPlot


def test_scatterplot_initialization():
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([5, 4, 3, 2, 1])
    scatter = ScatterPlot(x, y)

    assert scatter.x is x
    assert scatter.y is y
    assert scatter.lowerlimx == np.min(x) * 0.9
    assert scatter.lowerlimy == np.min(y) * 0.9
    assert scatter.upperlimx == np.max(x) * 1.1
    assert scatter.upperlimy == np.max(y) * 1.1


def test_scatterplot_custom_limits():
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([5, 4, 3, 2, 1])
    scatter = ScatterPlot(x, y, lowerlimx=0, lowerlimy=0, upperlimx=6, upperlimy=6)

    assert scatter.lowerlimx == 0
    assert scatter.lowerlimy == 0
    assert scatter.upperlimx == 6
    assert scatter.upperlimy == 6


def test_scatterplot_sizes_colors():
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([5, 4, 3, 2, 1])
    sizes = [10, 20, 30, 40, 50]
    colors = ["r", "g", "b", "y", "m"]
    scatter = ScatterPlot(x, y, sizes=sizes, colors=colors)

    assert scatter.sizes == sizes
    assert scatter.colors == colors


def test_scatterplot_plot():
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([5, 4, 3, 2, 1])
    scatter = ScatterPlot(x, y)

    scatter.plot()  # This will display the plot, but we can't assert visual output in tests
