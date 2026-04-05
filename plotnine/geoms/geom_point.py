from __future__ import annotations

import typing

import numpy as np

from .._utils import SIZE_FACTOR, to_rgba
from ..doctools import document
from ..scales.scale_shape import FILLED_SHAPES
from .geom import geom

if typing.TYPE_CHECKING:
    from typing import Any

    import pandas as pd
    from matplotlib.axes import Axes
    from matplotlib.offsetbox import DrawingArea

    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view
    from plotnine.layer import layer


@document
class geom_point(geom):
    """
    Plot points (Scatter plot)

    {usage}

    Parameters
    ----------
    {common_parameters}
    """

    DEFAULT_AES = {
        "alpha": 1,
        "color": "black",
        "fill": None,
        "shape": "o",
        "size": 1.5,
        "stroke": 0.5,
    }
    REQUIRED_AES = {"x", "y"}
    NON_MISSING_AES = {"color", "shape", "size"}

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

    @staticmethod
    def draw_unit(
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
    ):
        # Our size is in 'points' while scatter wants
        # 'points^2'. The stroke is outside. And pi
        # gives a large enough scaling factor
        # All other sizes for which the MPL units should
        # be in points must scaled using sqrt(pi)
        pass

    @staticmethod
    def draw_legend(
        data: pd.Series[Any], da: DrawingArea, lyr: layer
    ) -> DrawingArea:
        """
        Draw a point in the box

        Parameters
        ----------
        data : Series
            Data Row
        da : DrawingArea
            Canvas
        lyr : layer
            Layer

        Returns
        -------
        out : DrawingArea
        """
        pass

    @staticmethod
    def legend_key_size(
        data: pd.Series[Any], min_size: tuple[int, int], lyr: layer
    ) -> tuple[int, int]:
        pass
