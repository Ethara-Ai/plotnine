from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING, cast
from warnings import warn

import numpy as np
import pandas as pd

from ..doctools import document
from ..exceptions import PlotnineError, PlotnineWarning
from ..mapping.evaluation import after_stat
from .stat import stat

if TYPE_CHECKING:
    from plotnine.typing import FloatArray, FloatArrayLike


# NOTE: Parameter descriptions are in
# statsmodels/nonparametric/kde.py
@document
class stat_density(stat):
    """
    Compute density estimate

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
    gridsize : int, default=None
        If gridsize is `None`{.py}, `max(len(x), 50)`{.py} is used.
    bw : str | float, default="nrd0"
        The bandwidth to use, If a float is given, it is the bandwidth.
        The options are:

        ```python
        "nrd0"
        "normal_reference"
        "scott"
        "silverman"
        ```

        `nrd0` is a port of `stats::bw.nrd0` in R; it is eqiuvalent
        to `silverman` when there is more than 1 value in a group.
    cut : float, default=3
        Defines the length of the grid past the lowest and highest
        values of `x` so that the kernel goes to zero. The end points
        are `-/+ cut*bw*{min(x) or max(x)}`.
    clip : tuple[float, float], default=(-inf, inf)
        Values in `x` that are outside of the range given by clip are
        dropped. The number of values in `x` is then shortened.
    bounds: tuple[float, float], default=(-inf, inf)
        The domain boundaries of the data. When the domain is finite the
        estimated density will be corrected to remove asymptotic boundary
        effects that are usually biased away from the probability density
        function being estimated.

    See Also
    --------
    plotnine.geom_density : The default `geom` for this `stat`.
    statsmodels.nonparametric.kde.KDEUnivariate
    statsmodels.nonparametric.kde.KDEUnivariate.fit
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    'density'   # density estimate

    'count'     # density * number of points,
                # useful for stacked density plots

    'scaled'    # density estimate, scaled to maximum of 1
    'n'         # Number of observations at a position
    ```


    """
    REQUIRED_AES = {"x"}
    DEFAULT_PARAMS = {
        "geom": "density",
        "position": "stack",
        "kernel": "gaussian",
        "adjust": 1,
        "trim": False,
        "n": 1024,
        "gridsize": None,
        "bw": "nrd0",
        "cut": 3,
        "clip": (-np.inf, np.inf),
        "bounds": (-np.inf, np.inf),
    }
    DEFAULT_AES = {"y": after_stat("density")}
    CREATES = {"density", "count", "scaled", "n"}

    def setup_params(self, data):
        pass

    def compute_group(self, data, scales):
        pass


def compute_density(x, weight, range, params):
    """
    Compute density
    """
    pass


def nrd0(x: FloatArrayLike) -> float:
    """
    Port of R stats::bw.nrd0

    This is equivalent to statsmodels silverman when x has more than
    1 unique value. It can never give a zero bandwidth.

    Parameters
    ----------
    x : array_like
        Values whose density is to be estimated

    Returns
    -------
    out : float
        Bandwidth of x
    """
    pass


def fit_density_to_bounds(
    x: FloatArray,
    y: FloatArray,
    range: tuple[float, float],
    bounds: tuple[float, float],
) -> tuple[FloatArray, FloatArray]:
    """
    Fit calculated density to the given bounds

    Parameters
    ----------
    x :
        Points at which the density is estimated. `x` is expected to
        to include all values of the density grid.
    y :
        Estimated density.
    range :
    bounds :
        Valid boundary (domain) of the x values.

    Returns
    -------
    x_bound :
        Points that fall within the bounds at which the density is
        estimated.
    y_bound :
        Estimated densities at points within the bounds.
    """
    pass
