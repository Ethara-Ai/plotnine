import numpy as np
import pandas as pd

from .._utils import resolution
from ..doctools import document
from .stat import stat


@document
class stat_boxplot(stat):
    """
    Compute boxplot statistics

    {usage}

    Parameters
    ----------
    {common_parameters}
    coef : float, default=1.5
        Length of the whiskers as a multiple of the Interquartile
        Range.

    See Also
    --------
    plotnine.geom_boxplot: The default `geom` for this `stat`.
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "width"  # width of boxplot
    "lower"  # lower hinge, 25% quantile
    "middle" # median, 50% quantile
    "upper"  # upper hinge, 75% quantile

    # lower edge of notch, computed as;
    # median - 1.58 * IQR / sqrt(n)
    "notchlower"

    # upper edge of notch, computed as;
    # median + 1.58 * IQR / sqrt(n)
    "notchupper"

    # lower whisker, computed as; smallest observation
    # greater than or equal to lower hinge - 1.5 * IQR
    "ymin"

    # upper whisker, computed as; largest observation
    # less than or equal to upper hinge + 1.5 * IQR
    "ymax"
    ```

        'n'     # Number of observations at a position

    Calculated aesthetics are accessed using the `after_stat` function.
    e.g. `after_stat('width')`{.py}.
    """

    REQUIRED_AES = {"x", "y"}
    NON_MISSING_AES = {"weight"}
    DEFAULT_PARAMS = {
        "geom": "boxplot",
        "position": "dodge",
        "coef": 1.5,
        "width": None,
    }
    CREATES = {
        "lower",
        "upper",
        "middle",
        "ymin",
        "ymax",
        "outliers",
        "notchupper",
        "notchlower",
        "width",
        "relvarwidth",
        "n",
    }

    def setup_data(self, data):
        pass

    def setup_params(self, data):
        pass

    def compute_group(self, data, scales):
        pass


def weighted_percentile(a, q, weights=None):
    """
    Compute the weighted q-th percentile of data

    Parameters
    ----------
    a : array_like
        Input that can be converted into an array.
    q : array_like[float]
        Percentile or sequence of percentiles to compute. Must be int
        the range [0, 100]
    weights : array_like
        Weights associated with the input values.
    """
    pass


def weighted_boxplot_stats(x, weights=None, whis=1.5):
    """
    Calculate weighted boxplot plot statistics

    Parameters
    ----------
    x : array_like
        Data
    weights : array_like
        Weights associated with the data.
    whis : float
        Position of the whiskers beyond the interquartile range.
        The data beyond the whisker are considered outliers.

        If a float, the lower whisker is at the lowest datum above
        `Q1 - whis*(Q3-Q1)`, and the upper whisker at the highest
        datum below `Q3 + whis*(Q3-Q1)`, where Q1 and Q3 are the
        first and third quartiles.  The default value of
        `whis = 1.5` corresponds to Tukey's original definition of
        boxplots.

    Notes
    -----
    This method adapted from Matplotlibs boxplot_stats. The key difference
    is the use of a weighted percentile calculation and then using linear
    interpolation to map weight percentiles back to data.
    """
    pass
