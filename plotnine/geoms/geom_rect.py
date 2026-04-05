from __future__ import annotations

import typing

import numpy as np
import pandas as pd

from .._utils import SIZE_FACTOR, to_rgba
from ..doctools import document
from .geom import geom
from .geom_polygon import geom_polygon

if typing.TYPE_CHECKING:
    from typing import Any

    from matplotlib.axes import Axes

    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view


@document
class geom_rect(geom):
    """
    Rectangles

    {usage}

    Parameters
    ----------
    {common_parameters}
    """

    DEFAULT_AES = {
        "color": None,
        "fill": "#595959",
        "linetype": "solid",
        "size": 0.5,
        "alpha": 1,
    }
    REQUIRED_AES = {"xmax", "xmin", "ymax", "ymin"}

    draw_legend = staticmethod(geom_polygon.draw_legend)

    def draw_panel(
        self,
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
    ):
        """
        Plot all groups
        """
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


def _rectangles_to_polygons(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert rect data to polygons

    Parameters
    ----------
    df : dataframe
        Dataframe with *xmin*, *xmax*, *ymin* and *ymax* columns,
        plus others for aesthetics ...

    Returns
    -------
    data : dataframe
        Dataframe with *x* and *y* columns, plus others for
        aesthetics ...
    """
    pass
