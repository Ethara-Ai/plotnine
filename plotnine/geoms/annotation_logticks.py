from __future__ import annotations

import typing
import warnings

import numpy as np
import pandas as pd

from .._utils import log
from ..coords import coord_flip
from ..exceptions import PlotnineWarning
from ..scales.scale_continuous import scale_continuous as ScaleContinuous
from .annotate import annotate
from .geom_path import geom_path
from .geom_rug import geom_rug

if typing.TYPE_CHECKING:
    from typing import Any, Literal, Optional, Sequence

    from matplotlib.axes import Axes

    from plotnine.coords.coord import coord
    from plotnine.facets.layout import Layout
    from plotnine.geoms.geom import geom
    from plotnine.iapi import panel_view
    from plotnine.typing import AnyArray


class _geom_logticks(geom_rug):
    """
    Internal geom implementing drawing of annotation_logticks
    """

    DEFAULT_AES = {}
    DEFAULT_PARAMS = {
        "sides": "bl",
        "alpha": 1,
        "color": "black",
        "size": 0.5,
        "linetype": "solid",
        "lengths": (0.036, 0.0225, 0.012),
        "base": 10,
    }
    draw_legend = staticmethod(geom_path.draw_legend)

    def draw_layer(self, data: pd.DataFrame, layout: Layout, coord: coord):
        """
        Draw ticks on every panel
        """
        pass

    @staticmethod
    def _check_log_scale(
        base: Optional[float],
        sides: str,
        panel_params: panel_view,
        coord: coord,
    ) -> tuple[float, float]:
        """
        Check the log transforms

        Parameters
        ----------
        base : float | None
            Base of the logarithm in which the ticks will be
            calculated. If `None`, the base of the log transform
            the scale will be used.
        sides : str, default="bl"
            Sides onto which to draw the marks. Any combination
            chosen from the characters `btlr`, for *bottom*, *top*,
            *left* or *right* side marks. If `coord_flip()` is used,
            these are the sides *before* the flip.
        panel_params : panel_view
            `x` and `y` view scale values.
        coord : coord
            Coordinate (e.g. coord_cartesian) system of the geom.

        Returns
        -------
        out : tuple
            The bases (base_x, base_y) to use when generating the ticks.
        """
        pass

    @staticmethod
    def _calc_ticks(
        value_range: tuple[float, float], base: float
    ) -> tuple[AnyArray, AnyArray, AnyArray]:
        """
        Calculate tick marks within a range

        Parameters
        ----------
        value_range: tuple
            Range for which to calculate ticks.

        base : number
            Base of logarithm

        Returns
        -------
        out: tuple
            (major, middle, minor) tick locations
        """
        pass

    def draw_panel(
        self,
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
    ):
        pass


class annotation_logticks(annotate):
    """
    Marginal log ticks.

    If added to a plot that does not have a log10 axis
    on the respective side, a warning will be issued.

    Parameters
    ----------
    sides :
        Sides onto which to draw the marks. Any combination
        chosen from the characters `btlr`, for *bottom*, *top*,
        *left* or *right* side marks. If `coord_flip()` is used,
        these are the sides *after* the flip.
    alpha :
        Transparency of the ticks
    color :
        Colour of the ticks
    size :
        Thickness of the ticks
    linetype :
        Type of line
    lengths:
        length of the ticks drawn for full / half / tenth
        ticks relative to panel size
    base :
        Base of the logarithm in which the ticks will be
        calculated. If `None`, the base used to log transform
        the scale will be used.
    """

    def __init__(
        self,
        sides: str = "bl",
        alpha: float = 1,
        color: str
        | tuple[float, float, float]
        | tuple[float, float, float, float] = "black",
        size: float = 0.5,
        linetype: Literal["solid", "dashed", "dashdot", "dotted"]
        | Sequence[float] = "solid",
        lengths: tuple[float, float, float] = (0.036, 0.0225, 0.012),
        base: float | None = None,
    ):
        if len(lengths) != 3:
            raise ValueError(
                "length for annotation_logticks must be a tuple of 3 floats"
            )

        self._annotation_geom = _geom_logticks(
            sides=sides,
            alpha=alpha,
            color=color,
            size=size,
            linetype=linetype,
            lengths=lengths,
            base=base,
            inherit_aes=False,
            show_legend=False,
        )
