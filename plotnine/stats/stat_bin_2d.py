import itertools
import types

import numpy as np
import pandas as pd

from .._utils import is_scalar
from ..doctools import document
from ..mapping.evaluation import after_stat
from .binning import fuzzybreaks
from .stat import stat


@document
class stat_bin_2d(stat):
    """
    2 Dimensional bin counts

    {usage}

    Parameters
    ----------
    {common_parameters}
    bins : int, default=30
        Number of bins. Overridden by binwidth.
    breaks : array_like | tuple[array_like, array_like] , default=None
        Bin boundaries. This supersedes the `binwidth`, `bins`,
        `center` and `boundary`. It can be an array_like or
        a list of two array_likes to provide distinct breaks for
        the `x` and `y` axes.
    binwidth : float, default=None
        The width of the bins. The default is to use bins bins that
        cover the range of the data. You should always override this
        value, exploring multiple widths to find the best to illustrate
        the stories in your data.
    drop : bool, default=False
        If `True`{.py}, removes all cells with zero counts.

    See Also
    --------
    plotnine.geom_rect : The default `geom` for this `stat`.
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "xmin"    # x lower bound for the bin
    "xmax"    # x upper bound for the bin
    "ymin"    # y lower bound for the bin
    "ymax"    # y upper bound for the bin
    "count"   # number of points in bin
    "density" # density of points in bin, scaled to integrate to 1
    ```

    """
    REQUIRED_AES = {"x", "y"}
    DEFAULT_PARAMS = {
        "geom": "rect",
        "bins": 30,
        "breaks": None,
        "binwidth": None,
        "drop": True,
    }
    DEFAULT_AES = {"fill": after_stat("count"), "weight": None}
    CREATES = {"xmin", "xmax", "ymin", "ymax", "count", "density"}

    def setup_params(self, data):
        pass

    def compute_group(self, data, scales):
        pass


stat_bin2d = stat_bin_2d


def dual_param(value):
    """
    Return duplicate of parameter value

    Used to apply same value to x & y axes if only one
    value is given.
    """
    pass
