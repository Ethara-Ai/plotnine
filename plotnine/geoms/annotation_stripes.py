from __future__ import annotations

import typing
from itertools import cycle, islice

import numpy as np
import pandas as pd

from ..coords import coord_flip
from ..scales.scale_discrete import scale_discrete
from .annotate import annotate
from .geom import geom
from .geom_polygon import geom_polygon
from .geom_rect import geom_rect

if typing.TYPE_CHECKING:
    from typing import Any, Literal, Sequence

    from matplotlib.axes import Axes

    from plotnine.coords.coord import coord
    from plotnine.facets.layout import Layout
    from plotnine.iapi import panel_view


class annotation_stripes(annotate):
    """
    Alternating stripes, centered around each label.

    Useful as a background for geom_jitter.

    Parameters
    ----------
    fill :
        List of colors for the strips.
    fill_range :
        How to fill stripes beyond the range of scale:

        ```python
        "cycle"      # keep cycling the colors of the
                     # stripes after the range ends
        "nocycle"    # stop cycling the colors of the
                     # stripes after the range ends
        "auto"       # "cycle" for continuous scales and
                     # "nocycle" for discrete scales.
        "no"         # Do not add stripes passed the range
                     # passed the range of the scales
        ```
    direction :
        Orientation of the stripes
    extend :
        Range of the stripes. The default is (0, 1), top to bottom.
        The values should be in the range [0, 1].
    **kwargs :
        Other aesthetic parameters for the rectangular stripes.
        They include; `alpha`, `color`, `linetype`, and `size`.
    """

    def __init__(
        self,
        fill: Sequence[str] = ("#AAAAAA", "#CCCCCC"),
        fill_range: Literal["auto", "cycle", "no", "nocycle"] = "auto",
        direction: Literal["horizontal", "vertical"] = "vertical",
        extend: tuple[float, float] = (0, 1),
        **kwargs: Any,
    ):
        allowed = ("vertical", "horizontal")
        if direction not in allowed:
            raise ValueError(f"direction must be one of {allowed}")
        self._annotation_geom = _geom_stripes(
            fill=fill,
            fill_range=fill_range,
            extend=extend,
            direction=direction,
            inherit_aes=False,
            show_legend=False,
            **kwargs,
        )


class _geom_stripes(geom):
    DEFAULT_AES = {}
    REQUIRED_AES = set()
    DEFAULT_PARAMS = {
        "color": None,
        "fill": ("#AAAAAA", "#CCCCCC"),
        "linetype": "solid",
        "size": 1,
        "alpha": 0.5,
        "direction": "vertical",
        "extend": (0, 1),
        "fill_range": "auto",
    }
    draw_legend = staticmethod(geom_polygon.draw_legend)

    def draw_layer(self, data: pd.DataFrame, layout: Layout, coord: coord):
        """
        Draw stripes on every panel
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
