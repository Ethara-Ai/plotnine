from __future__ import annotations

import typing

import numpy as np
import pandas as pd

from .._utils import SIZE_FACTOR, to_rgba
from ..doctools import document
from ..exceptions import PlotnineError
from .geom import geom
from .geom_point import geom_point
from .geom_polygon import geom_polygon

if typing.TYPE_CHECKING:
    from typing import Any

    import numpy.typing as npt
    from matplotlib.axes import Axes
    from matplotlib.offsetbox import DrawingArea
    from matplotlib.patches import PathPatch
    from shapely.geometry.polygon import LinearRing, Polygon

    from plotnine import aes
    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view
    from plotnine.layer import layer
    from plotnine.typing import DataLike


@document
class geom_map(geom):
    """
    Draw map feature

    {usage}

    The map feature are drawn without any special projections.

    Parameters
    ----------
    {common_parameters}

    Notes
    -----
    This geom is best suited for plotting a shapefile read into
    geopandas dataframe. The dataframe should have a `geometry`
    column.
    """

    DEFAULT_AES = {
        "alpha": 1,
        "color": "#111111",
        "fill": "#333333",
        "linetype": "solid",
        "shape": "o",
        "size": 0.5,
        "stroke": 0.5,
    }
    REQUIRED_AES = {"geometry"}

    def __init__(
        self,
        mapping: aes | None = None,
        data: DataLike | None = None,
        **kwargs: Any,
    ):
        geom.__init__(self, mapping, data, **kwargs)
        # Almost all geodataframes loaded from shapefiles
        # have a geometry column.
        if "geometry" not in self.mapping:
            self.mapping["geometry"] = "geometry"

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

    @staticmethod
    def draw_legend(
        data: pd.Series[Any], da: DrawingArea, lyr: layer
    ) -> DrawingArea:
        """
        Draw a rectangle in the box

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


def PolygonPatch(
    obj: Polygon,
) -> PathPatch:
    """
    Return a Matplotlib patch from a Polygon/MultiPolygon Geometry

    Parameters
    ----------
    obj : shapley.geometry.Polygon | shapley.geometry.MultiPolygon
        A Polygon or MultiPolygon to create a patch for description

    Returns
    -------
    result : matplotlib.patches.PathPatch
        A patch representing the shapely geometry

    Notes
    -----
    This functionality was originally provided by the descartes package
    by Sean Gillies (BSD license, https://pypi.org/project/descartes)
    which is nolonger being maintained.
    """
    pass


def check_geopandas():
    pass
