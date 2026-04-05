from __future__ import annotations

import warnings
from contextlib import suppress
from typing import TYPE_CHECKING, Callable, cast

import numpy as np
import pandas as pd

from .._utils import get_valid_kwargs
from ..exceptions import PlotnineError, PlotnineWarning

if TYPE_CHECKING:
    import statsmodels.api as sm

    from plotnine.typing import FloatArray


def predictdf(data, xseq, params) -> pd.DataFrame:
    """
    Make prediction on the data

    This is a general function responsible for dispatching
    to functions that do predictions for the specific models.
    """
    pass


def lm(data, xseq, params) -> pd.DataFrame:
    """
    Fit OLS / WLS if data has weight
    """
    pass


def lm_formula(data, xseq, params) -> pd.DataFrame:
    """
    Fit OLS / WLS using a formula
    """
    pass


def rlm(data, xseq, params) -> pd.DataFrame:
    """
    Fit RLM
    """
    pass


def rlm_formula(data, xseq, params) -> pd.DataFrame:
    """
    Fit RLM using a formula
    """
    pass


def gls(data, xseq, params) -> pd.DataFrame:
    """
    Fit GLS
    """
    pass


def gls_formula(data, xseq, params):
    """
    Fit GLL using a formula
    """
    pass


def glm(data, xseq, params) -> pd.DataFrame:
    """
    Fit GLM
    """
    pass


def glm_formula(data, xseq, params):
    """
    Fit with GLM formula
    """
    pass


def lowess(data, xseq, params) -> pd.DataFrame:
    """
    Lowess fitting
    """
    pass


def loess(data, xseq, params) -> pd.DataFrame:
    """
    Loess smoothing
    """
    pass


def mavg(data, xseq, params) -> pd.DataFrame:
    """
    Fit moving average
    """
    pass


def gpr(data, xseq, params):
    """
    Fit gaussian process
    """
    pass


def tdist_ci(x, dof, stderr, level):
    """
    Confidence Intervals using the t-distribution
    """
    pass


# Override wls_prediction_std from statsmodels to calculate the confidence
# interval instead of only the prediction interval
def wls_prediction_std(
    res, exog=None, weights=None, alpha=0.05, interval="confidence"
):
    """
    Calculate standard deviation and confidence interval

    Applies to WLS and OLS, not to general GLS,
    that is independently but not identically distributed observations

    Parameters
    ----------
    res : regression-result
        results of WLS or OLS regression required attributes see notes
    exog : array_like
        exogenous variables for points to predict
    weights : scalar | array_like
        weights as defined for WLS (inverse of variance of observation)
    alpha : float
        confidence level for two-sided hypothesis
    interval : str
        Type of interval to compute. One of "confidence" or "prediction"

    Returns
    -------
    predstd : array_like
        Standard error of prediction. It must be the same length as rows
        of exog.
    interval_l, interval_u : array_like
        Lower und upper confidence bounds

    Notes
    -----
    The result instance needs to have at least the following
    res.model.predict() : predicted values or
    res.fittedvalues : values used in estimation
    res.cov_params() : covariance matrix of parameter estimates

    If exog is 1d, then it is interpreted as one observation,
    i.e. a row vector.

    testing status: not compared with other packages

    References
    ----------
    Greene p.111 for OLS, extended to WLS by analogy
    """
    pass


def separate_method_kwargs(method_args, init_method, fit_method):
    """
    Categorise kwargs passed to the stat

    Some args are of the init method others for the fit method
    The separation is done by introspecting the init & fit methods
    """
    pass


def _glm_family(family: str) -> sm.families.Family:
    """
    Get glm-family instance

    Ref: https://www.statsmodels.org/stable/glm.html#families
    """
    pass
