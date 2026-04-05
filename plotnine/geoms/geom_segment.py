from __future__ import annotations

import typing

import numpy as np
import pandas as pd

from .._utils import SIZE_FACTOR, interleave, make_line_segments, to_rgba
from ..doctools import document
from .geom import geom
from .geom_path import geom_path

if typing.TYPE_CHECKING:
    from typing import Any

    from matplotlib.axes import Axes

    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view


@document
class geom_segment(geom):
    """
    Line segments

    {usage}

    Parameters
    ----------
    {common_parameters}
    lineend : Literal["butt", "round", "projecting"], default="butt"
        Line end style. This option is applied for solid linetypes.
    arrow : ~plotnine.geoms.geom_path.arrow, default=None
        Arrow specification. Default is no arrow.

    See Also
    --------
    plotnine.arrow : for adding arrowhead(s) to segments.
    """

    DEFAULT_AES = {
        "alpha": 1,
        "color": "black",
        "linetype": "solid",
        "size": 0.5,
    }
    REQUIRED_AES = {"x", "y", "xend", "yend"}
    NON_MISSING_AES = {"linetype", "size", "shape"}
    DEFAULT_PARAMS = {"lineend": "butt", "arrow": None}

    draw_legend = staticmethod(geom_path.draw_legend)
    legend_key_size = staticmethod(geom_path.legend_key_size)

    @staticmethod
    def draw_group(
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
    ):
        pass
