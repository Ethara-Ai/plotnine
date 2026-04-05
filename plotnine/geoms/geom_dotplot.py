from __future__ import annotations

import typing
from warnings import warn

import numpy as np

from .._utils import groupby_apply, resolution, to_rgba
from ..doctools import document
from ..exceptions import PlotnineWarning
from .geom import geom
from .geom_path import geom_path

if typing.TYPE_CHECKING:
    from typing import Any

    import pandas as pd
    from matplotlib.axes import Axes
    from matplotlib.offsetbox import DrawingArea

    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view
    from plotnine.layer import layer
    from plotnine.typing import FloatSeries


@document
class geom_dotplot(geom):
    """
    Dot plot

    {usage}

    Parameters
    ----------
    {common_parameters}
    stackdir : Literal["up", "down", "center", "centerwhole"], default="up"
        Direction in which to stack the dots. Options are
    stackratio : float, default=1
        How close to stack the dots. If value is less than 1,
        the dots overlap, if greater than 1 they are spaced.
    dotsize : float, default=1
        Diameter of dots relative to `binwidth`.
    stackgroups : bool, default=False
        If `True`{.py}, the dots are stacked across groups.

    See Also
    --------
    plotnine.stat_bindot : The default `stat` for this `geom`.
    """

    DEFAULT_AES = {"alpha": 1, "color": "black", "fill": "black"}
    REQUIRED_AES = {"x", "y"}
    NON_MISSING_AES = {"size", "shape"}
    DEFAULT_PARAMS = {
        "stat": "bindot",
        "stackdir": "up",
        "stackratio": 1,
        "dotsize": 1,
        "stackgroups": False,
    }

    legend_key_size = staticmethod(geom_path.legend_key_size)

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
