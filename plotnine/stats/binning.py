from __future__ import annotations

import typing

import numpy as np
import pandas as pd

from ..exceptions import PlotnineError
from ..scales.scale_discrete import scale_discrete

if typing.TYPE_CHECKING:
    from typing import Literal, Optional

    from plotnine.typing import FloatArray, FloatArrayLike


__all__ = (
    "freedman_diaconis_bins",
    "breaks_from_bins",
    "breaks_from_binwidth",
    "assign_bins",
    "fuzzybreaks",
)


def freedman_diaconis_bins(a):
    """
    Calculate number of hist bins using Freedman-Diaconis rule.
    """
    pass


def breaks_from_binwidth(
    x_range: tuple[float, float],
    binwidth: float,
    center: Optional[float] = None,
    boundary: Optional[float] = None,
) -> FloatArray:
    """
    Calculate breaks given binwidth

    Parameters
    ----------
    x_range :
        Range over with to calculate the breaks. Must be
        of size 2.
    binwidth :
        Separation between the breaks
    center :
        The center of one of the bins
    boundary :
        A boundary between two bins

    Returns
    -------
    out : array_like
        Sequence of break points.
    """
    pass


def breaks_from_bins(
    x_range: tuple[float, float],
    bins: int = 30,
    center: Optional[float] = None,
    boundary: Optional[float] = None,
) -> FloatArray:
    """
    Calculate breaks given binwidth

    Parameters
    ----------
    x_range :
        Range over with to calculate the breaks. Must be
        of size 2.
    bins :
        Number of bins
    center :
        The center of one of the bins
    boundary :
        A boundary between two bins

    Returns
    -------
    out : array_like
        Sequence of break points.
    """
    pass


def assign_bins(
    x,
    breaks: FloatArrayLike,
    weight: Optional[FloatArrayLike] = None,
    pad: bool = False,
    closed: Literal["right", "left"] = "right",
):
    """
    Assign value in x to bins demacated by the break points

    Parameters
    ----------
    x :
        Values to be binned.
    breaks :
        Sequence of break points.
    weight :
        Weight of each value in `x`. Used in creating the frequency
        table. If `None`, then each value in `x` has a weight of 1.
    pad :
        If `True`, add empty bins at either end of `x`.
    closed :
        Whether the right or left edges of the bins are part of the
        bin.

    Returns
    -------
    out : dataframe
        Bin count and density information.
    """
    pass


def result_dataframe(count, x, width, xmin=None, xmax=None):
    """
    Create a dataframe to hold bin information
    """
    pass


def fuzzybreaks(
    scale, breaks=None, boundary=None, binwidth=None, bins=30, right=True
) -> FloatArray:
    """
    Compute fuzzy breaks

    For a continuous scale, fuzzybreaks "preserve" the range of
    the scale. The fuzzing is close to numerical roundoff and
    is visually imperceptible.

    Parameters
    ----------
    scale : scale
        Scale
    breaks : array_like
        Sequence of break points. If provided and the scale is not
        discrete, they are returned.
    boundary : float
        First break. If `None` a suitable on is computed using
        the range of the scale and the binwidth.
    binwidth : float
        Separation between the breaks
    bins : int
        Number of bins
    right : bool
        If `True` the right edges of the bins are part of the
        bin. If `False` then the left edges of the bins are part
        of the bin.

    Returns
    -------
    out : array_like
    """
    pass


def _adjust_breaks(breaks: FloatArray, right: bool) -> FloatArray:
    """
    Adjust breaks to include/exclude every right break

    If right=True, the breaks create intervals closed on right
    i.e. [_] (_] (_] (_]
    If right=False, the breaks create intervals closed on the left
    i.e. [_) [_) [_) [_]
    """
    pass
