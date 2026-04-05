from typing import TYPE_CHECKING, cast

import numpy as np
import pandas as pd

from ..doctools import document
from ..exceptions import PlotnineError
from .stat import stat
from .stat_qq import theoretical_qq

if TYPE_CHECKING:
    from plotnine.typing import FloatArray


@document
class stat_qq_line(stat):
    """
    Calculate line through quantile-quantile plot

    {usage}

    Parameters
    ----------
    {common_parameters}
    distribution : str, default="norm"
        Distribution or distribution function name. The default is
        *norm* for a normal probability plot. Objects that look enough
        like a stats.distributions instance (i.e. they have a ppf
        method) are also accepted. See [scipy stats ](`scipy.stats`)
        for available distributions.
    dparams : dict, default=None
        Distribution-specific shape parameters (shape parameters plus
        location and scale).
    quantiles : array_like, default=None
        Probability points at which to calculate the theoretical
        quantile values. If provided, must be the same number as
        as the sample data points. The default is to use calculated
        theoretical points, use to `alpha_beta` control how
        these points are generated.
    alpha_beta : tuple, default=(3/8, 3/8)
        Parameter values to use when calculating the quantiles.
    line_p : tuple, default=(0.25, 0.75)
        Quantiles to use when fitting a Q-Q line. Must be 2 values.
    fullrange : bool, default=False
        If `True`{.py} the fit will span the full range of the plot.

    See Also
    --------
    plotnine.geom_qq_line : The default `geom` for this `stat`.
    scipy.stats.mstats.plotting_positions : Uses `alpha_beta`
        to calculate the quantiles.
    """

    REQUIRED_AES = {"sample"}
    DEFAULT_PARAMS = {
        "geom": "qq_line",
        "distribution": "norm",
        "dparams": {},
        "quantiles": None,
        "alpha_beta": (3 / 8, 3 / 8),
        "line_p": (0.25, 0.75),
        "fullrange": False,
    }
    CREATES = {"x", "y"}

    def setup_params(self, data):
        pass

    def compute_group(self, data, scales):
        pass
