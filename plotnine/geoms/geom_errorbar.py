from __future__ import annotations

import typing

import numpy as np
import pandas as pd

from .._utils import copy_missing_columns, resolution
from ..doctools import document
from .geom import geom
from .geom_path import geom_path
from .geom_segment import geom_segment

if typing.TYPE_CHECKING:
    from typing import Any

    from matplotlib.axes import Axes

    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view


@document
class geom_errorbar(geom):
    """
    Vertical interval represented as an errorbar

    {usage}

    Parameters
    ----------
    {common_parameters}
    width : float, default=0.5
        Bar width as a fraction of the resolution of the data.
    """

    DEFAULT_AES = {
        "alpha": 1,
        "color": "black",
        "linetype": "solid",
        "size": 0.5,
    }
    REQUIRED_AES = {"x", "ymin", "ymax"}
    DEFAULT_PARAMS = {"width": 0.5}

    draw_legend = staticmethod(geom_path.draw_legend)

    def setup_data(self, data: pd.DataFrame) -> pd.DataFrame:
        pass

    @staticmethod
    def draw_group(
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
    ):
        pass
