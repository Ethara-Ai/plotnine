from __future__ import annotations

from typing import TYPE_CHECKING, cast

import numpy as np

from .._utils import SIZE_FACTOR, make_line_segments, to_rgba
from ..coords import coord_flip
from ..doctools import document
from .geom import geom
from .geom_path import geom_path

if TYPE_CHECKING:
    from typing import Any

    import pandas as pd
    from matplotlib.axes import Axes

    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view
    from plotnine.typing import FloatArray


@document
class geom_rug(geom):
    """
    Marginal rug plot

    {usage}

    Parameters
    ----------
    {common_parameters}
    sides : str, default="bl"
        Sides onto which to draw the marks. Any combination
        chosen from the characters `"btlr"`, for *bottom*, *top*,
        *left* or *right* side marks.
    length: float, default=0.03
        length of marks in fractions of horizontal/vertical panel size.
    """

    DEFAULT_AES = {
        "alpha": 1,
        "color": "black",
        "size": 0.5,
        "linetype": "solid",
    }
    DEFAULT_PARAMS = {"sides": "bl", "length": 0.03}

    draw_legend = staticmethod(geom_path.draw_legend)

    @staticmethod
    def draw_group(
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
    ):
        pass
