from typing import TYPE_CHECKING, cast

import numpy as np
import pandas as pd

from ..doctools import document
from ..mapping.evaluation import after_stat
from .density import get_var_type, kde
from .stat import stat

if TYPE_CHECKING:
    from plotnine.typing import FloatArray


@document
class stat_pointdensity(stat):
    """
    Compute density estimation for each point

    {usage}

    Parameters
    ----------
    {common_parameters}
    package : Literal["statsmodels", "scipy", "sklearn"], default="statsmodels"
        Package whose kernel density estimation to use.
    kde_params : dict, default=None
        Keyword arguments to pass on to the kde class.

    See Also
    --------
    plotnine.geom_density_2d : The default `geom` for this `stat`.
    statsmodels.nonparametric.kde.KDEMultivariate
    scipy.stats.gaussian_kde
    sklearn.neighbors.KernelDensity
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "density"   # Computed density at a point
    ```

    """
    REQUIRED_AES = {"x", "y"}
    DEFAULT_AES = {"color": after_stat("density")}
    DEFAULT_PARAMS = {
        "geom": "density_2d",
        "package": "statsmodels",
        "kde_params": None,
    }
    CREATES = {"density"}

    def setup_params(self, data):
        pass

    def compute_group(self, data, scales):
        pass
