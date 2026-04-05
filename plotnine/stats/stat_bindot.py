from __future__ import annotations

import typing
from warnings import warn

import numpy as np
import pandas as pd

from .._utils import groupby_apply
from ..doctools import document
from ..exceptions import PlotnineError, PlotnineWarning
from ..mapping.evaluation import after_stat
from .binning import (
    assign_bins,
    breaks_from_bins,
    breaks_from_binwidth,
    freedman_diaconis_bins,
)
from .stat import stat

if typing.TYPE_CHECKING:
    from typing import Optional

    from plotnine.typing import FloatArrayLike


@document
class stat_bindot(stat):
    """
    Binning for a dot plot

    {usage}

    Parameters
    ----------
    {common_parameters}
    bins : int, default=None
        Number of bins. Overridden by binwidth. If `None`{.py},
        a number is computed using the freedman-diaconis method.
    binwidth : float, default=None
        When `method="dotdensity"`{.py}, this specifies the maximum
        binwidth. When `method="histodot"`{.py}, this specifies the
        binwidth. This supersedes the `bins`.
    origin : float, default=None
        When `method="histodot"`{.py}, origin of the first bin.
    width : float, default=0.9
        When `binaxis="y"`{.py}, the spacing of the dotstacks for
        dodging.
    binaxis : Literal["x", "y"], default="x"
        Axis to bin along.
    method : Literal["dotdensity", "histodot"], default="dotdensity"
        Whether to do dot-density binning or fixed widths binning.
    binpositions : Literal["all", "bygroup"], default="bygroup"
        Position of the bins when `method="dotdensity"`{.py}. The value
        - `bygroup` -  positions of the bins for each group are
        determined separately.
        - `all` - positions of the bins are determined with all
        data taken together. This aligns the dots
        stacks across multiple groups.
    drop : bool, default=False
        If `True`{.py}, remove all bins with zero counts.
    right : bool, default=True
        When `method="histodot"`{.py}, `True`{.py} means include right
        edge of the bins and if `False`{.py} the left edge is included.
    breaks : FloatArray, default=None
        Bin boundaries for `method="histodot"`{.py}. This supersedes the
        `binwidth` and `bins`.

    See Also
    --------
    plotnine.geom_dotplot : The default `geom` for this `stat`.
    plotnine.stat_bin
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "count"    # number of points in bin
    "density"  # density of points in bin, scaled to integrate to 1
    "ncount"   # count, scaled to maximum of 1
    "ndensity" # density, scaled to maximum of 1
    ```

    """

    REQUIRED_AES = {"x"}
    NON_MISSING_AES = {"weight"}
    DEFAULT_PARAMS = {
        "geom": "dotplot",
        "bins": None,
        "binwidth": None,
        "origin": None,
        "width": 0.9,
        "binaxis": "x",
        "method": "dotdensity",
        "binpositions": "bygroup",
        "drop": False,
        "right": True,
        "breaks": None,
    }
    DEFAULT_AES = {"y": after_stat("count")}
    CREATES = {"width", "count", "density", "ncount", "ndensity"}

    def setup_params(self, data):
        pass

    def compute_panel(self, data, scales):
        pass

    def compute_group(self, data, scales):
        pass


def densitybin(
    x,
    weight: FloatArrayLike | None,
    binwidth: float | None,
    bins: int = 30,
    rangee: Optional[tuple[float, float]] = None,
):
    """
    Do density binning

    It does not collapse each bin with a count.

    Parameters
    ----------
    x : array_like
        Numbers to bin
    weight : array_like
        Weights
    binwidth : numeric
        Size of the bins
    bins : int
        Number of bins
    rangee : tuple
        Range of x

    Returns
    -------
    data : DataFrame
    """
    pass
