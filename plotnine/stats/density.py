"""
Kernel Density Functions

These functions make it easy to integrate stats that compute
kernel densities with the wider scientific python ecosystem.

Credit: Jake VanderPlas for the original kde_* functions
https://jakevdp.github.io/blog/2013/12/01/kernel-density-estimation/
"""

from __future__ import annotations

import typing

import numpy as np

from .._utils import array_kind

if typing.TYPE_CHECKING:
    from typing import Any, Literal

    import pandas as pd

    from plotnine.typing import FloatArray


def kde_scipy(data: FloatArray, grid: FloatArray, **kwargs: Any) -> FloatArray:
    """
    Kernel Density Estimation with Scipy

    Parameters
    ----------
    data :
        Data points used to compute a density estimator. It
        has `n x p` dimensions, representing n points and p
        variables.
    grid :
        Data points at which the desity will be estimated. It
        has `m x p` dimensions, representing m points and p
        variables.

    Returns
    -------
    out : numpy.array
        Density estimate. Has `m x 1` dimensions
    """
    pass


def kde_statsmodels_u(
    data: FloatArray, grid: FloatArray, **kwargs: Any
) -> FloatArray:
    """
    Univariate Kernel Density Estimation with Statsmodels

    Parameters
    ----------
    data :
        Data points used to compute a density estimator. It
        has `n x 1` dimensions, representing n points and p
        variables.
    grid :
        Data points at which the desity will be estimated. It
        has `m x 1` dimensions, representing m points and p
        variables.

    Returns
    -------
    out : numpy.array
        Density estimate. Has `m x 1` dimensions
    """
    pass


def kde_statsmodels_m(
    data: FloatArray, grid: FloatArray, **kwargs: Any
) -> FloatArray:
    """
    Multivariate Kernel Density Estimation with Statsmodels

    Parameters
    ----------
    data :
        Data points used to compute a density estimator. It
        has `n x p` dimensions, representing n points and p
        variables.
    grid :
        Data points at which the desity will be estimated. It
        has `m x p` dimensions, representing m points and p
        variables.

    Returns
    -------
    out :
        Density estimate. Has `m x 1` dimensions
    """
    pass


def kde_sklearn(
    data: FloatArray, grid: FloatArray, **kwargs: Any
) -> FloatArray:
    """
    Kernel Density Estimation with Scikit-learn

    Parameters
    ----------
    data :
        Data points used to compute a density estimator. It
        has `n x p` dimensions, representing n points and p
        variables.
    grid :
        Data points at which the desity will be estimated. It
        has `m x p` dimensions, representing m points and p
        variables.

    Returns
    -------
    out :
        Density estimate. Has `m x 1` dimensions
    """
    pass


def kde_count(data: FloatArray, grid: FloatArray, **kwargs: Any) -> FloatArray:
    """
    Kernel Density Estimation via count within radius

    Parameters
    ----------
    data :
        Data points used to compute a density estimator. It
        has `n x p` dimensions, representing n points and p
        variables.
    grid :
        Data points at which the desity will be estimated. It
        has `m x p` dimensions, representing m points and p
        variables.

    Returns
    -------
    out :
        Density estimate. Has `m x 1` dimensions
    """
    pass


KDE_FUNCS = {
    "statsmodels-u": kde_statsmodels_u,
    "statsmodels-m": kde_statsmodels_m,
    "scipy": kde_scipy,
    "scikit-learn": kde_sklearn,
    "sklearn": kde_sklearn,
    "count": kde_count,
}


def kde(
    data: FloatArray, grid: FloatArray, package: str, **kwargs: Any
) -> FloatArray:
    """
    Kernel Density Estimation

    Parameters
    ----------
    package :
        Package whose kernel density estimation to use.
        Should be one of
        `['statsmodels-u', 'statsmodels-m', 'scipy', 'sklearn']`.
    data :
        Data points used to compute a density estimator. It
        has `n x p` dimensions, representing n points and p
        variables.
    grid :
        Data points at which the desity will be estimated. It
        has `m x p` dimensions, representing m points and p
        variables.

    Returns
    -------
    out : numpy.array
        Density estimate. Has `m x 1` dimensions
    """
    pass


def get_var_type(col: pd.Series) -> Literal["c", "o", "u"]:
    """
    Return var_type (for KDEMultivariate) of the column

    Parameters
    ----------
    col :
        A dataframe column.

    Returns
    -------
    out :
        Character that denotes the type of column.
        `c` for continuous, `o` for ordered categorical and
        `u` for unordered categorical or if not sure.

    See Also
    --------
    statsmodels.nonparametric.kernel_density.KDEMultivariate : For the origin
        of the character codes.
    """
    pass
