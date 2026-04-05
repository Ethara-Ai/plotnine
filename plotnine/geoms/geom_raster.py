from __future__ import annotations

import typing
from warnings import warn

import numpy as np

from .._utils import resolution
from ..coords import coord_cartesian
from ..doctools import document
from ..exceptions import PlotnineError, PlotnineWarning
from .geom import geom
from .geom_polygon import geom_polygon

if typing.TYPE_CHECKING:
    from typing import Any

    import pandas as pd
    from matplotlib.axes import Axes

    from plotnine import aes
    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view
    from plotnine.typing import DataLike


@document
class geom_raster(geom):
    """
    Rasterized Rectangles specified using center points

    {usage}

    Parameters
    ----------
    {common_parameters}

    hjust : float, default=0.5
        Horizontal justification for the rectangle at point `x`.
        Default is 0.5, which centers the rectangle horizontally.
        Must be in the range `[0, 1]`.
    vjust : float, default=0.5
        Vertical justification for the rectangle at point `y`
        Default is 0.5, which centers the rectangle vertically.
        Must be in the range `[0, 1]`.
    interpolation : str, default=None
        How to calculate values between the center points of
        adjacent rectangles. The default is `None`{.py} not to
        interpolate. Allowed values are:
        ```python
        "antialiased"
        "nearest"
        "bilinear"
        "bicubic"
        "spline16"
        "spline36"
        "hanning"
        "hamming"
        "hermite"
        "kaiser"
        "quadric"
        "catrom"
        "gaussian"
        "bessel"
        "mitchell"
        "sinc"
        "lanczos"
        "blackman"
        ```
    filterrad : float, default=4.0
        The filter radius for filters that have a radius parameter, i.e.
        when interpolation is one of: `sinc`, `lanczos`, `blackman`.
        Must be a number greater than zero.

    See Also
    --------
    plotnine.geom_rect
    plotnine.geom_tile
    """

    DEFAULT_AES = {"alpha": 1, "fill": "#333333"}
    REQUIRED_AES = {"x", "y"}
    NON_MISSING_AES = {"fill", "xmin", "xmax", "ymin", "ymax"}
    DEFAULT_PARAMS = {
        "vjust": 0.5,
        "hjust": 0.5,
        "interpolation": None,
        "filterrad": 4.0,
        "raster": True,
    }
    draw_legend = staticmethod(geom_polygon.draw_legend)

    def __init__(
        self,
        mapping: aes | None = None,
        data: DataLike | None = None,
        **kwargs: Any,
    ):
        # Silently accept:
        #    1. interpolate
        #    2. bool values for interpolation
        if "interpolate" in kwargs:
            kwargs["interpolation"] = kwargs.pop("interpolate")
        if isinstance(kwargs.get("interpolation"), bool):
            if kwargs["interpolation"] is True:
                kwargs["interpolation"] = "bilinear"
            else:
                kwargs["interpolation"] = None

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
        """
        Plot all groups
        """
        pass
