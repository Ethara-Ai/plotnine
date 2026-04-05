from __future__ import annotations

import typing

import numpy as np
import pandas as pd

from .._utils import copy_missing_columns
from ..doctools import document
from ..exceptions import PlotnineError
from .geom import geom
from .geom_path import geom_path

if typing.TYPE_CHECKING:
    from typing import Any

    from matplotlib.axes import Axes

    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view


@document
class geom_step(geom_path):
    """
    Stepped connected points

    {usage}

    Parameters
    ----------
    {common_parameters}
    direction : Literal["hv", "vh", "mid"], default="hv"
        horizontal-vertical steps,
        vertical-horizontal steps or steps half-way between adjacent
        x values.

    See Also
    --------
    plotnine.geom_path : For documentation of extra parameters.
    """

    DEFAULT_PARAMS = {"direction": "hv"}

    draw_panel = geom.draw_panel

    @staticmethod
    def draw_group(
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
    ):
        pass
