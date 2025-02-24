import matplotlib.pyplot as plt
import numpy as np


class BoxPlot:
    def __init__(self, data, notch=False, sym="b", vert=True, whis=1.5):
        """Initializes Boxplot object with the following parameters:
        data: data to be plotted
        notch: notch shape of the box
        sym: symbol for outliers
        vert: vertical orientation (deprecated, use orientation instead)
        whis: whisker length in number of IQR
        """
        # Validate data type
        if not isinstance(data, (list, np.ndarray)):
            raise TypeError("Data must be a list or numpy array")

        # Validate numeric data
        try:
            numeric_data = [float(x) for x in data]
        except (ValueError, TypeError):
            raise TypeError("All elements must be numeric")

        # Validate data length
        if not data or len(data) == 0:
            raise ValueError("Data array cannot be empty")

        # Validate whis parameter
        if whis <= 0:
            raise ValueError("Whisker length must be positive")

        self.data = numeric_data
        self.notch = notch
        self.sym = sym
        self.vert = vert
        self.whis = whis

    # Rest of the class implementation remains the same
    def median(self):
        """Calculate median of the data"""
        return float(np.median(self.data))

    def quartiles(self):
        """Calculate first and third quartiles"""
        q1 = float(np.percentile(self.data, 25))
        q3 = float(np.percentile(self.data, 75))
        return (q1, q3)

    def outliers(self):
        """Identify outliers using whis*IQR rule"""
        q1, q3 = self.quartiles()
        iqr = q3 - q1
        lower_bound = q1 - (self.whis * iqr)
        upper_bound = q3 + (self.whis * iqr)
        return [x for x in self.data if x < lower_bound or x > upper_bound]

    def plot(self):
        """Generate box plot"""
        plt.style.use("_mpl-gallery")
        fig, ax = plt.subplots()

        # Set labels and ticks
        if self.vert:
            ax.set_xlabel("Data")
            ax.set_ylabel("Value")
            ax.set_xticks([1])
        else:
            ax.set_xlabel("Value")
            ax.set_ylabel("Data")
            ax.set_yticks([1])

        # Add grid for better readability
        ax.grid(True, linestyle="--", alpha=0.7)

        # Adjust layout to prevent label clipping
        plt.tight_layout()

        plt.show()
