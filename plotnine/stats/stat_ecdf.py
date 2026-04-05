import numpy as np
import pandas as pd

from ..doctools import document
from ..mapping.evaluation import after_stat
from .stat import stat


@document
class stat_ecdf(stat):
    """
    Empirical Cumulative Density Function

    {usage}

    Parameters
    ----------
    {common_parameters}
    n  : int, default=None
        This is the number of points to interpolate with.
        If `None`{.py}, do not interpolate.
    pad : bool, default=True
        If True, pad the domain with `-inf` and `+inf` so that
        ECDF does not have discontinuities at the extremes.

    See Also
    --------
    plotnine.geom_step : The default `geom` for this `stat`.
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "x"     # x in the data
    "ecdf"  # cumulative density corresponding to x
    ```
    """

    REQUIRED_AES = {"x"}
    DEFAULT_PARAMS = {"geom": "step", "n": None, "pad": True}
    DEFAULT_AES = {"y": after_stat("ecdf")}
    CREATES = {"ecdf"}

    def compute_group(self, data, scales):
        pass
