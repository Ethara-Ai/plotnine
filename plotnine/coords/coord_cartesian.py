from __future__ import annotations

import typing
from types import SimpleNamespace

from ..iapi import panel_view
from ..positions.position import transform_position
from .coord import coord, dist_euclidean

if typing.TYPE_CHECKING:
    from typing import Any

    import pandas as pd

    from plotnine.iapi import scale_view
    from plotnine.scales.scale import scale
    from plotnine.typing import (
        FloatArray,
        FloatSeries,
    )


class coord_cartesian(coord):
    """
    Cartesian coordinate system

    Parameters
    ----------
    xlim :
        Limits (in data type of the x-aesthetic) for x axis.
        If None, then they are automatically computed.
    ylim :
        Limits (in data type of the x-aesthetic) for y axis.
        If None, then they are automatically computed.
    expand :
        If `True`, expand the coordinate axes by some factor. If `False`,
        use the limits from the data.
    """

    is_linear = True

    def __init__(
        self,
        xlim: tuple[Any, Any] | None = None,
        ylim: tuple[Any, Any] | None = None,
        expand: bool = True,
    ):
        self.limits = SimpleNamespace(x=xlim, y=ylim)
        self.expand = expand

    def transform(
        self, data: pd.DataFrame, panel_params: panel_view, munch: bool = False
    ) -> pd.DataFrame:
        pass

    def setup_panel_params(self, scale_x: scale, scale_y: scale) -> panel_view:
        """
        Compute the range and break information for the panel
        """
        pass

    def distance(
        self,
        x: FloatSeries,
        y: FloatSeries,
        panel_params: panel_view,
    ) -> FloatArray:
        pass
