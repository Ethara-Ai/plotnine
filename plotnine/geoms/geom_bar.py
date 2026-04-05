from __future__ import annotations

import typing

from .._utils import resolution
from ..doctools import document
from .geom_rect import geom_rect

if typing.TYPE_CHECKING:
    import pandas as pd


@document
class geom_bar(geom_rect):
    """
    Bar plot

    {usage}

    Parameters
    ----------
    {common_parameters}
    just : float, default=0.5
        How to align the column with respect to the axis breaks. The default
        `0.5` aligns the center of the column with the break. `0` aligns the
        left of the of the column with the break and `1` aligns the right of
        the column with the break.
    width : float, default=None
        Bar width. If `None`{.py}, the width is set to
        `90%` of the resolution of the data.

    See Also
    --------
    plotnine.geom_histogram
    plotnine.stat_count : The default `stat` for this `geom`.
    """

    REQUIRED_AES = {"x", "y"}
    NON_MISSING_AES = {"xmin", "xmax", "ymin", "ymax"}
    DEFAULT_PARAMS = {
        "stat": "count",
        "position": "stack",
        "just": 0.5,
        "width": None,
    }

    def setup_data(self, data: pd.DataFrame) -> pd.DataFrame:
        pass
