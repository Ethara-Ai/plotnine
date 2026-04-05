from __future__ import annotations

from collections import Counter
from contextlib import suppress
from typing import TYPE_CHECKING
from warnings import warn

import numpy as np

from .._utils import SIZE_FACTOR, make_line_segments, match, to_rgba
from ..doctools import document
from ..exceptions import PlotnineWarning
from .geom import geom

if TYPE_CHECKING:
    from typing import Any, Literal, Sequence

    import numpy.typing as npt
    import pandas as pd
    from matplotlib.axes import Axes
    from matplotlib.offsetbox import DrawingArea
    from matplotlib.path import Path

    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view
    from plotnine.layer import layer
    from plotnine.typing import BoolArray


@document
class geom_path(geom):
    """
    Connected points

    {usage}

    Parameters
    ----------
    {common_parameters}
    lineend : Literal["butt", "round", "projecting"], default="butt"
        Line end style. This option is applied for solid linetypes.
    linejoin : Literal["round", "miter", "bevel"], default="round"
        Line join style. This option is applied for solid linetypes.
    arrow : ~plotnine.geoms.geom_path.arrow, default=None
        Arrow specification. Default is no arrow.

    See Also
    --------
    plotnine.arrow : for adding arrowhead(s) to paths.
    """

    DEFAULT_AES = {
        "alpha": 1,
        "color": "black",
        "linetype": "solid",
        "size": 0.5,
    }

    REQUIRED_AES = {"x", "y"}
    DEFAULT_PARAMS = {
        "lineend": "butt",
        "linejoin": "round",
        "arrow": None,
    }

    def handle_na(self, data: pd.DataFrame) -> pd.DataFrame:
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
        Draw a horizontal line in the box

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


class arrow:
    """
    Define arrow (actually an arrowhead)

    This is used to define arrow heads for
    [](`~plotnine.geoms.geom_path`).

    Parameters
    ----------
    angle :
        angle in degrees between the tail a
        single edge.
    length :
        of the edge in "inches"
    ends :
        At which end of the line to draw the
        arrowhead
    type :
        When it is closed, it is also filled
    """

    def __init__(
        self,
        angle: float = 30,
        length: float = 0.2,
        ends: Literal["first", "last", "both"] = "last",
        type: Literal["open", "closed"] = "open",
    ):
        self.angle = angle
        self.length = length
        self.ends = ends
        self.type = type

    def draw(
        self,
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
        constant: bool = True,
    ):
        """
        Draw arrows at the end(s) of the lines

        Parameters
        ----------
        data : dataframe
            Data to be plotted by this geom. This is the
            dataframe created in the plot_build pipeline.
        panel_params : panel_view
            The scale information as may be required by the
            axes. At this point, that information is about
            ranges, ticks and labels. Attributes are of interest
            to the geom are:

            ```python
            "panel_params.x.range"  # tuple
            "panel_params.y.range"  # tuple
            ```
        coord : coord
            Coordinate (e.g. coord_cartesian) system of the
            geom.
        ax : axes
            Axes on which to plot.
        constant: bool
            If the path attributes vary along the way. If false,
            the arrows are per segment of the path
        params : dict
            Combined parameters for the geom and stat. Also
            includes the `zorder`.
        """
        pass

    def get_paths(
        self,
        x1: npt.ArrayLike,
        y1: npt.ArrayLike,
        x2: npt.ArrayLike,
        y2: npt.ArrayLike,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
    ) -> list[Path]:
        """
        Compute paths that create the arrow heads

        Parameters
        ----------
        x1, y1, x2, y2 : array_like
            List of points that define the tails of the arrows.
            The arrow heads will be at x1, y1. If you need them
            at x2, y2 reverse the input.
        panel_params : panel_view
            The scale information as may be required by the
            axes. At this point, that information is about
            ranges, ticks and labels. Attributes are of interest
            to the geom are:

            ```python
            "panel_params.x.range"  # tuple
            "panel_params.y.range"  # tuple
            ```
        coord : coord
            Coordinate (e.g. coord_cartesian) system of the geom.
        ax : axes
            Axes on which to plot.

        Returns
        -------
        out : list of Path
            Paths that create arrow heads
        """
        pass


def _draw_segments(data: pd.DataFrame, ax: Axes, params: dict[str, Any]):
    """
    Draw independent line segments between all the
    points
    """
    pass


def _draw_lines(data: pd.DataFrame, ax: Axes, params: dict[str, Any]):
    """
    Draw a path with the same characteristics from the
    first point to the last point
    """
    pass


def _get_joinstyle(
    data: pd.DataFrame, params: dict[str, Any]
) -> dict[str, Any]:
    pass


def _axes_get_size_inches(ax: Axes) -> tuple[float, float]:
    """
    Size of axes in inches

    Parameters
    ----------
    ax : axes
        Axes

    Returns
    -------
    out : tuple[float, float]
        (width, height) of ax in inches
    """
    pass
