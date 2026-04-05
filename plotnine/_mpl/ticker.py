import locale

from matplotlib.ticker import FixedFormatter


class MyFixedFormatter(FixedFormatter):
    """
    Override MPL fixedformatter for better formatting
    """

    def format_data(self, value: float) -> str:
        """
        Return a formatted string representation of a number.
        """
        pass
