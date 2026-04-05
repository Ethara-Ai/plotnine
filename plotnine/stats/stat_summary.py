from typing import cast

import numpy as np
import pandas as pd

from .._utils import get_valid_kwargs, uniquecols
from ..doctools import document
from ..exceptions import PlotnineError
from .stat import stat


def bootstrap_statistics(
    series,
    statistic,
    n_samples=1000,
    confidence_interval=0.95,
    random_state=None,
):
    """
    Default parameters taken from
    R's Hmisc smean.cl.boot
    """
    pass


def mean_cl_boot(
    series, n_samples=1000, confidence_interval=0.95, random_state=None
):
    """
    Bootstrapped mean with confidence interval

    Parameters
    ----------
    series : pandas.Series
        Values
    n_samples : int, default=1000
        Number of sample to draw.
    confidence_interval : float
        Confidence interval in the range (0, 1).
    random_state : int | ~numpy.random.RandomState, default=None
        Seed or Random number generator to use. If `None`, then
        numpy global generator [](`numpy.random`) is used.
    """
    pass


def mean_cl_normal(series, confidence_interval=0.95):
    """
    Mean with confidence interval assuming normal distribution

    Credit: from http://stackoverflow.com/a/15034143

    Parameters
    ----------
    series : pandas.Series
        Values
    confidence_interval : float
        Confidence interval in the range (0, 1).
    """
    pass


def mean_sdl(series, mult=2):
    """
    Mean +/- a constant times the standard deviation

    Parameters
    ----------
    series : pandas.Series
        Values
    mult : float
        Multiplication factor.
    """
    pass


def median_hilow(series, confidence_interval=0.95):
    """
    Median and a selected pair of outer quantiles having equal tail areas

    Parameters
    ----------
    series : pandas.Series
        Values
    confidence_interval : float
        Confidence interval in the range (0, 1).
    """
    pass


def mean_se(series, mult=1):
    """
    Calculate mean and standard errors on either side

    Parameters
    ----------
    series : pandas.Series
        Values
    mult : float
        Multiplication factor.
    """
    pass


function_dict = {
    "mean_cl_boot": mean_cl_boot,
    "mean_cl_normal": mean_cl_normal,
    "mean_sdl": mean_sdl,
    "median_hilow": median_hilow,
    "mean_se": mean_se,
}


def make_summary_fun(fun_data, fun_y, fun_ymin, fun_ymax, fun_args):
    """
    Make summary function
    """
    pass


@document
class stat_summary(stat):
    """
    Calculate summary statistics depending on x

    {usage}

    Parameters
    ----------
    {common_parameters}
    fun_data : str | callable, default="mean_cl_boot"
        If string, it should be one of:

        ```python
        # Bootstrapped mean, confidence interval
        # Arguments:
        #     n_samples - No. of samples to draw
        #     confidence_interval
        #     random_state
        "mean_cl_boot"

        # Mean, C.I. assuming normal distribution
        # Arguments:
        #     confidence_interval
        "mean_cl_normal"

        # Mean, standard deviation * constant
        # Arguments:
        #     mult - multiplication factor
        "mean_sdl"

        # Median, outlier quantiles with equal tail areas
        # Arguments:
        #     confidence_interval
        "median_hilow"

        # Mean, Standard Errors * constant
        # Arguments:
        #     mult - multiplication factor
        "mean_se"
        ```

        or any function that takes a array and returns a dataframe
        with three columns named `y`, `ymin` and `ymax`.
    fun_y : callable, default=None
        Any function that takes a array_like and returns a value
    fun_ymin : callable, default=None
        Any function that takes an array_like and returns a value
    fun_ymax : callable, default=None
        Any function that takes an array_like and returns a value
    fun_args : dict, default=None
        Arguments to any of the functions. Provided the names of the
        arguments of the different functions are in not conflict, the
        arguments will be assigned to the right functions. If there is
        a conflict, create a wrapper function that resolves the
        ambiguity in the argument names.
    random_state : int | ~numpy.random.RandomState, default=None
        Seed or Random number generator to use. If `None`, then
        numpy global generator [](`numpy.random`) is used.

    Notes
    -----
    If any of `fun_y`, `fun_ymin` or `fun_ymax` are provided, the
    value of `fun_data` will be ignored.

    See Also
    --------
    plotnine.geom_pointrange : The default `geom` for this `stat`.
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "ymin"  # ymin computed by the summary function
    "ymax"  # ymax computed by the summary function
    "n"     # Number of observations at a position
    ```

    Calculated aesthetics are accessed using the `after_stat` function.
    e.g. `after_stat('ymin')`{.py}.
    """

    REQUIRED_AES = {"x", "y"}
    DEFAULT_PARAMS = {
        "geom": "pointrange",
        "fun_data": "mean_cl_boot",
        "fun_y": None,
        "fun_ymin": None,
        "fun_ymax": None,
        "fun_args": None,
        "random_state": None,
    }
    CREATES = {"ymin", "ymax", "n"}

    def setup_params(self, data):
        pass

    def compute_panel(self, data, scales):
        pass
