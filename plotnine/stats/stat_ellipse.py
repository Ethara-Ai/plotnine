from __future__ import annotations

from typing import TYPE_CHECKING
from warnings import warn

import numpy as np
import pandas as pd

from ..doctools import document
from ..exceptions import PlotnineWarning
from .stat import stat

if TYPE_CHECKING:
    from typing import Any, Optional

    from plotnine.typing import FloatArray, FloatArrayLike


@document
class stat_ellipse(stat):
    """
    Calculate normal confidence interval ellipse

    {usage}

    Parameters
    ----------
    {common_parameters}
    type : Literal["t", "norm", "euclid"], default="t"
        The type of ellipse.
        `t` assumes a multivariate t-distribution.
        `norm` assumes a multivariate normal distribution.
        `euclid` draws a circle with the radius equal to
        `level`, representing the euclidean distance from the center.

    level : float, default=0.95
        The confidence level at which to draw the ellipse.
    segments : int, default=51
        Number of segments to be used in drawing the ellipse.

    See Also
    --------
    plotnine.geom_path : The default `geom` for this `stat`.
    """

    REQUIRED_AES = {"x", "y"}
    DEFAULT_PARAMS = {
        "geom": "path",
        "type": "t",
        "level": 0.95,
        "segments": 51,
    }

    def compute_group(self, data, scales):
        pass


def cov_trob(
    x,
    wt: Optional[FloatArrayLike] = None,
    cor=False,
    center: FloatArrayLike | bool = True,
    nu=5,
    maxit=25,
    tol=0.01,
):
    """
    Covariance Estimation for Multivariate t Distribution

    Estimates a covariance or correlation matrix assuming the
    data came from a multivariate t distribution: this provides
    some degree of robustness to outlier without giving a high
    breakdown point.

    **credit**: This function a port of the R function
    `MASS::cov.trob`.

    Parameters
    ----------
    x : array
        data matrix. Missing values (NaNs) are not allowed.
    wt : array
        A vector of weights for each case: these are treated as
        if the case i actually occurred `wt[i]` times.
    cor : bool
        Flag to choose between returning the correlation
        (`cor=True`) or covariance (`cor=False`) matrix.
    center : array | bool
        A logical value or a numeric vector providing the location
        about which the covariance is to be taken.
        If `center=False`, no centering is done; if
        `center=True` the MLE of the location vector is used.
    nu : int
        'degrees of freedom' for the multivariate t distribution.
        Must exceed 2 (so that the covariance matrix is finite).
    maxit : int
        Maximum number of iterations in fitting.
    tol : float
        Convergence tolerance for fitting.

    Returns
    -------
    out : dict
        A dictionary with with the following key-value

        - `cov` : the fitted covarince matrix.
        - `center` : the estimated or specified location vector.
        - `wt` : the specified weights: only returned if the
           wt argument was given.
        - `n_obs` : the number of cases used in the fitting.
        - `cor` : the fitted correlation matrix: only returned
          if `cor=True`.
        - `call` : The matched call.
        - `iter` : The number of iterations used.

    References
    ----------
    - J. T. Kent, D. E. Tyler and Y. Vardi (1994) A curious likelihood
      identity for the multivariate t-distribution. *Communications in
      Statistics-Simulation and Computation* **23**, 441-453.

    - Venables, W. N. and Ripley, B. D. (1999) *Modern Applied
      Statistics with S-PLUS*. Third Edition. Springer.

    """
    pass
