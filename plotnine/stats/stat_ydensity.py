from contextlib import suppress

import numpy as np
import pandas as pd

from ..doctools import document
from ..exceptions import PlotnineError
from .stat import stat
from .stat_density import compute_density, stat_density


@document
class stat_ydensity(stat):
    """
    Density estimate

    {usage}

    Parameters
    ----------
    {common_parameters}
    kernel : str, default="gaussian"
        Kernel used for density estimation. One of:

        ```python
        "biweight"
        "cosine"
        "cosine2"
        "epanechnikov"
        "gaussian"
        "triangular"
        "triweight"
        "uniform"
        ```
    adjust : float, default=1
        An adjustment factor for the `bw`. Bandwidth becomes
        `bw * adjust`{.py}.
        Adjustment of the bandwidth.
    trim : bool, default=False
        This parameter only matters if you are displaying multiple
        densities in one plot. If `False`{.py}, the default, each
        density is computed on the full range of the data. If
        `True`{.py}, each density is computed over the range of that
        group; this typically means the estimated x values will not
        line-up, and hence you won't be able to stack density values.
    n : int, default=1024
        Number of equally spaced points at which the density is to
        be estimated. For efficient computation, it should be a power
        of two.
    bw : str | float, default="nrd0"
        The bandwidth to use, If a float is given, it is the bandwidth.
        The `str` choices are:

        ```python
        "nrd0"
        "normal_reference"
        "scott"
        "silverman"
        ```

        `nrd0` is a port of `stats::bw.nrd0` in R; it is eqiuvalent
        to `silverman` when there is more than 1 value in a group.
    scale : Literal["area", "count", "width"], default="area"
        How to scale the violins. The options are:
        If `area` all violins have the same area, before trimming the tails.
        If `count` the areas are scaled proportionally to the number of
        observations.
        If `width` all violins have the same maximum width.

    See Also
    --------
    plotnine.geom_violin : The default `geom` for this `stat`.
    statsmodels.nonparametric.kde.KDEUnivariate
    statsmodels.nonparametric.kde.KDEUnivariate.fit
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "width"        # Maximum width of density, [0, 1] range.
    "violinwidth"  # Shape of the violin
    ```

    Calculated aesthetics are accessed using the `after_stat` function.
    e.g. `after_stat('width')`{.py}.
    """
    REQUIRED_AES = {"x", "y"}
    NON_MISSING_AES = {"weight"}
    DEFAULT_PARAMS = {
        "geom": "violin",
        "position": "dodge",
        "adjust": 1,
        "kernel": "gaussian",
        "n": 1024,
        "trim": True,
        "bw": "nrd0",
        "scale": "area",
    }
    DEFAULT_AES = {"weight": None}
    CREATES = {"width", "violinwidth"}

    def setup_data(self, data):
        pass

    def setup_params(self, data):
        pass

    def compute_panel(self, data, scales):
        pass

    def compute_group(self, data, scales):
        pass
