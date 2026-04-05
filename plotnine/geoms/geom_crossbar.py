from __future__ import annotations

import typing
from warnings import warn

import numpy as np
import pandas as pd

from .._utils import SIZE_FACTOR, copy_missing_columns, resolution, to_rgba
from ..doctools import document
from ..exceptions import PlotnineWarning
from .geom import geom
from .geom_polygon import geom_polygon
from .geom_segment import geom_segment

if typing.TYPE_CHECKING:
    from typing import Any

    import numpy.typing as npt
    from matplotlib.axes import Axes
    from matplotlib.offsetbox import DrawingArea

    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view
    from plotnine.layer import layer


@document
class geom_crossbar(geom):
    """
    Vertical interval represented by a crossbar

    {usage}

    Parameters
    ----------
    {common_parameters}
    width : float, default=0.5
        Box width as a fraction of the resolution of the data.
    fatten : float, default=2
        A multiplicative factor used to increase the size of the
        middle bar across the box.
    """

    DEFAULT_AES = {
        "alpha": 1,
        "color": "black",
        "fill": None,
        "linetype": "solid",
        "size": 0.5,
    }
    REQUIRED_AES = {"x", "y", "ymin", "ymax"}
    DEFAULT_PARAMS = {"width": 0.5, "fatten": 2}

    legend_key_size = staticmethod(geom_segment.legend_key_size)

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

    @staticmethod
    def draw_legend(
        data: pd.Series[Any], da: DrawingArea, lyr: layer
    ) -> DrawingArea:
        """
        Draw a rectangle with a horizontal strike in the box

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
