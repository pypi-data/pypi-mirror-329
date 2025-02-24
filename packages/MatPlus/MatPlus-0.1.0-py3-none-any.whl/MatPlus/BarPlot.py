import matplotlib.pyplot as plt
import numpy as np


class BarPlot:
    """
    A class to create bar plots with optional axis limits and styling.

    Attributes:
    ----------
    x : array-like
        The x coordinates of the bars.
    y : array-like
        The heights of the bars.
    lowerlimx : float, optional
        The lower limit for the x-axis. If None, it is set to 90% of the minimum x value.
    lowerlimy : float, optional
        The lower limit for the y-axis. If None, it is set to 90% of the minimum y value.
    upperlimx : float, optional
        The upper limit for the x-axis. If None, it is set to 110% of the maximum x value.
    upperlimy : float, optional
            The upper limit for the y-axis. If None, it is set to 110% of the maximum y value.
    wd : float
        The width of the bars.
    lw : float
        The linewidth of the bars.
    """

    def __init__(
        self,
        x,
        y,
        lowerlimx=None,
        lowerlimy=None,
        upperlimx=None,
        upperlimy=None,
        wd=None,
        lw=None,
    ):
        """
        Constructs all the necessary attributes for the BarPlot object.
        Plots the bar plot with the given parameters.
        """

        self.x = x
        self.y = y
        self.lowerlimx = lowerlimx
        self.lowerlimy = lowerlimy
        self.upperlimx = upperlimx
        self.upperlimy = upperlimy

        # Set default axis limits if not provided
        # Lower limit for x-axis/y-axis
        if self.lowerlimx is None:
            self.lowerlimx = np.min(x) * 0.9
        if self.lowerlimy is None:
            self.lowerlimy = np.min(y) * 0.9
        # Upper limit for x-axis/y-axis
        if self.upperlimx is None:
            self.upperlimx = np.max(x) * 1.1
        if self.upperlimy is None:
            self.upperlimy = np.max(y) * 1.1

        self.width = wd
        self.linewidth = lw

        # Set default width and linewidth if not provided
        if self.linewidth is None:
            self.linewidth = 1
        if self.width is None:
            self.width = 1

    def plot(self):
        plt.style.use("_mpl-gallery")
        fig, ax = plt.subplots()
        ax.bar(self.x, self.y, width=self.width, edgecolor="black", linewidth=1)
        ax.set(
            xlim=(self.lowerlimx, self.upperlimx),
            xticks=np.arange(self.lowerlimx + 1, self.upperlimx),
            ylim=(self.lowerlimy, self.upperlimy),
            yticks=np.arange(self.lowerlimy + 1, self.upperlimy),
        )
        plt.show()
