from __future__ import annotations

from typing import TYPE_CHECKING, cast

import numpy as np
import pandas as pd

from ..doctools import document
from .density import get_var_type, kde
from .stat import stat

if TYPE_CHECKING:
    from plotnine.typing import FloatArrayLike


@document
class stat_density_2d(stat):
    """
    Compute 2D kernel density estimation

    {usage}

    Parameters
    ----------
    {common_parameters}
    contour : bool, default=True
        Whether to create contours of the 2d density estimate.
    n : int, default=64
        Number of equally spaced points at which the density is to
        be estimated. For efficient computation, it should be a power
        of two.
    levels : int | array_like, default=5
        Contour levels. If an integer, it specifies the maximum number
        of levels, if array_like it is the levels themselves.
    package : Literal["statsmodels", "scipy", "sklearn"], default="statsmodels"
        Package whose kernel density estimation to use.
    kde_params : dict
        Keyword arguments to pass on to the kde class.

    See Also
    --------
    plotnine.geom_density_2d : The default `geom` for this `stat`.
    statsmodels.nonparametric.kernel_density.KDEMultivariate
    scipy.stats.gaussian_kde
    sklearn.neighbors.KernelDensity
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "level"     # density level of a contour
    "density"   # Computed density at a point
    "piece"     # Numeric id of a contour in a given group
    ```

    `level` is only relevant when contours are computed. `density`
    is available only when no contours are computed. `piece` is
    largely irrelevant.
    """
    REQUIRED_AES = {"x"}
    DEFAULT_PARAMS = {
        "geom": "density_2d",
        "contour": True,
        "package": "statsmodels",
        "kde_params": None,
        "n": 64,
        "levels": 5,
    }
    CREATES = {"y"}

    def setup_params(self, data):
        pass

    def compute_group(self, data, scales):
        pass


def contour_lines(X, Y, Z, levels: int | FloatArrayLike):
    """
    Calculate contour lines
    """
    pass
