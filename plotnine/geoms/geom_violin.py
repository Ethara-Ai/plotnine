from __future__ import annotations

from typing import TYPE_CHECKING, cast

import numpy as np
import pandas as pd

from .._utils import groupby_apply, interleave, resolution
from ..doctools import document
from .geom import geom
from .geom_path import geom_path
from .geom_polygon import geom_polygon

if TYPE_CHECKING:
    from typing import Any

    from matplotlib.axes import Axes

    from plotnine import aes
    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view
    from plotnine.typing import DataLike, FloatArray


@document
class geom_violin(geom):
    """
    Violin Plot

    {usage}

    Parameters
    ----------
    {common_parameters}
    draw_quantiles : float | list[float], default=None
        draw horizontal lines at the given quantiles (0..1)
        of the density estimate.
    style : str, default="full"
        The type of violin plot to draw. The options are:

        ```python
        'full'        # Regular (2 sided violins)
        'left'        # Left-sided half violins
        'right'       # Right-sided half violins
        'left-right'  # Alternate (left first) half violins by the group
        'right-left'  # Alternate (right first) half violins by the group
        ```

    See Also
    --------
    plotnine.stat_ydensity : The default `stat` for this `geom`.
    """

    DEFAULT_AES = {
        "alpha": 1,
        "color": "#333333",
        "fill": "white",
        "linetype": "solid",
        "size": 0.5,
        "weight": 1,
    }
    REQUIRED_AES = {"x", "y"}
    DEFAULT_PARAMS = {
        "stat": "ydensity",
        "position": "dodge",
        "draw_quantiles": None,
        "style": "full",
        "scale": "area",
        "trim": True,
        "width": None,
    }
    draw_legend = staticmethod(geom_polygon.draw_legend)

    def __init__(
        self,
        mapping: aes | None = None,
        data: DataLike | None = None,
        **kwargs: Any,
    ):
        if "draw_quantiles" in kwargs:
            kwargs["draw_quantiles"] = np.repeat(kwargs["draw_quantiles"], 1)
            if not all(0 < q < 1 for q in kwargs["draw_quantiles"]):
                raise ValueError(
                    "draw_quantiles must be a float or "
                    "an iterable of floats (>0.0; < 1.0)"
                )

        if "style" in kwargs:
            allowed = ("full", "left", "right", "left-right", "right-left")
            if kwargs["style"] not in allowed:
                raise ValueError(f"style must be either {allowed}")

        super().__init__(mapping, data, **kwargs)

    def setup_data(self, data: pd.DataFrame) -> pd.DataFrame:
        pass

    def draw_panel(
        self,
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
    ):
        pass


def make_quantile_df(
    data: pd.DataFrame, draw_quantiles: FloatArray
) -> pd.DataFrame:
    """
    Return a dataframe with info needed to draw quantile segments
    """
    pass
