import pytest
import numpy as np
from MatPlus.BoxPlot import BoxPlot
import matplotlib.pyplot as plt


def test_boxplot_creation():
    data = [1, 2, 3, 4, 5]
    boxplot = BoxPlot(data, sym="r")
    assert boxplot.data == data
    assert boxplot.sym == "r"
    assert boxplot.notch is False
    assert boxplot.vert is True
    assert boxplot.whis == 1.5


def test_boxplot_statistics():
    data = [1, 2, 3, 4, 5]
    boxplot = BoxPlot(data)

    # Test quartiles
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    median = np.median(data)

    assert np.median(boxplot.data) == median
    assert np.percentile(boxplot.data, 25) == q1
    assert np.percentile(boxplot.data, 75) == q3


def test_boxplot_parameters():
    data = [1, 2, 3, 4, 5]
    boxplot = BoxPlot(data, notch=True, sym="x", vert=False, whis=2.0)
    assert boxplot.notch is True
    assert boxplot.sym == "x"
    assert boxplot.vert is False
    assert boxplot.whis == 2.0


def test_boxplot_empty_data():
    with pytest.raises(ValueError):
        BoxPlot([])


def test_boxplot_plot():
    data = [1, 2, 3, 4, 5]
    boxplot = BoxPlot(data)
    # Just verify the plot method runs without error
    boxplot.plot()
    plt.close()  # Clean up plot


def test_median_calculation():
    data = [1, 2, 3, 4, 5, 6]
    boxplot = BoxPlot(data)
    assert boxplot.median() == 3.5

    # Test with even number of elements
    data = [1, 2, 3, 4]
    boxplot = BoxPlot(data)
    assert boxplot.median() == 2.5


def test_quartiles_calculation():
    data = [1, 2, 3, 4, 5, 6, 7, 8]
    boxplot = BoxPlot(data)
    q1, q3 = boxplot.quartiles()
    assert q1 == 2.75
    assert q3 == 6.25


def test_outliers_detection():
    # Create data with known outliers
    data = [1, 2, 2, 3, 3, 3, 4, 4, 100, -100]  # 100 and -100 are outliers
    boxplot = BoxPlot(data, whis=1.5)
    outliers = boxplot.outliers()
    assert len(outliers) == 2
    assert 100 in outliers
    assert -100 in outliers


def test_plot_horizontal_orientation():
    data = [1, 2, 3, 4, 5]
    boxplot = BoxPlot(data, vert=False)
    boxplot.plot()
    plt.close()


def test_invalid_data_type():
    with pytest.raises(TypeError):
        BoxPlot(["a", "b", "c"])


def test_negative_whis():
    with pytest.raises(ValueError):
        BoxPlot([1, 2, 3], whis=-1.5)


def test_single_value_data():
    data = [1]
    boxplot = BoxPlot(data)
    q1, q3 = boxplot.quartiles()
    assert q1 == 1
    assert q3 == 1
    assert boxplot.median() == 1
    assert len(boxplot.outliers()) == 0
