import matplotlib.pyplot as plt
import numpy as np


class ScatterPlot:
    def __init__(
        self,
        x,
        y,
        lowerlimx=None,
        lowerlimy=None,
        upperlimx=None,
        upperlimy=None,
        sizes=[],
        colors=[],
        vmin=0,
        vmax=0,
        width=1,
    ):
        """
        A class to create scatter plots with optional axis limits and styling.

        Attributes:
        ----------
        type : str
            The type of the plot.
        x : array-like
            The x coordinates of the data points.
        y : array-like
            The y coordinates of the data points.
        lowerlimx : float, optional
            The lower limit for the x-axis. If None, it is set to 90% of the minimum x value.
        lowerlimy : float, optional
            The lower limit for the y-axis. If None, it is set to 90% of the minimum y value.
        upperlimx : float, optional
            The upper limit for the x-axis. If None, it is set to 110% of the maximum x value.
        upperlimy : float, optional
                The upper limit for the y-axis. If None, it is set to 110% of the maximum y value.
        sizes : array-like
            The sizes of the data points.
        colors : array-like
            The colors of the data points.
        vmin : float
            The minimum value of the color map.
        vmax : float
            The maximum value of the color map.
        width : float
            The width of the plot.
        """

        self.type = type
        self.x = x
        self.y = y
        self.lowerlimx = lowerlimx
        self.lowerlimy = lowerlimy
        self.upperlimx = upperlimx
        self.upperlimy = upperlimy
        self.sizes = sizes
        self.colors = colors
        self.vmin = vmin
        self.vmax = vmax
        self.width = width

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

    def plot(self):
        """
        Constructs all the necessary attributes for the ScatterPlot object.
        Plots the scatter plot with the given parameters.
        """
        # Plots the scatter plot with the given parameters
        fig, ax = plt.subplots()

        # Plot scatter plot with sizes and colors if both are provided
        if len(self.sizes) != 0 and len(self.colors) != 0:
            ax.scatter(
                self.x,
                self.y,
                s=self.sizes,
                c=self.colors,
                vmin=self.vmin,
                vmax=self.vmax,
            )

        # Plot scatter plot with sizes if only sizes are provided
        elif len(self.sizes) != 0:
            ax.scatter(self.x, self.y, s=self.sizes, vmin=self.vmin, vmax=self.vmax)
        # Plot scatter plot with default size if neither sizes nor colors are provided
        else:
            ax.scatter(self.x, self.y, s=20, vmin=self.vmin, vmax=self.vmax)
        # Set labels for the x-axis and y-axis"""
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        # Set limits and ticks for the x-axis and y-axis"""
        ax.set(
            xlim=(self.lowerlimx, self.upperlimx),
            xticks=np.arange(self.lowerlimx + 1, self.upperlimx),
            ylim=(self.lowerlimy, self.upperlimy),
            yticks=np.arange(self.lowerlimy + 1, self.upperlimy),
        )
        # Display the plot
        plt.show()
