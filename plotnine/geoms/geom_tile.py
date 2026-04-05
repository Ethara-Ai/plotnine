from __future__ import annotations

import typing

from .._utils import resolution
from ..doctools import document
from .geom_rect import geom_rect

if typing.TYPE_CHECKING:
    import pandas as pd


@document
class geom_tile(geom_rect):
    """
    Rectangles specified using a center points

    {usage}

    Parameters
    ----------
    {common_parameters}

    See Also
    --------
    plotnine.geom_rect
    """

    DEFAULT_AES = {
        "alpha": 1,
        "color": None,
        "fill": "#333333",
        "linetype": "solid",
        "size": 0.1,
        "width": None,
        "height": None,
    }
    REQUIRED_AES = {"x", "y"}

    def setup_data(self, data: pd.DataFrame) -> pd.DataFrame:
        pass
