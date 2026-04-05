from __future__ import annotations

from types import SimpleNamespace as NS
from typing import TYPE_CHECKING, cast
from warnings import warn

from ..exceptions import PlotnineWarning
from ..iapi import panel_ranges, panel_view
from ..positions.position import transform_position
from .coord import coord, dist_euclidean

if TYPE_CHECKING:
    from typing import Optional

    import pandas as pd
    from mizani.transforms import trans

    from plotnine.iapi import scale_view
    from plotnine.scales.scale import scale
    from plotnine.typing import (
        FloatArray,
        FloatSeries,
        TFloatArrayLike,
    )


class coord_trans(coord):
    """
    Transformed cartesian coordinate system

    Parameters
    ----------
    x : str | trans
        Name of transform or `trans` class to transform the x axis
    y : str | trans
        Name of transform or `trans` class to transform the y axis
    xlim : tuple[float, float]
        Limits for x axis. If None, then they are automatically computed.
    ylim : tuple[float, float]
        Limits for y axis. If None, then they are automatically computed.
    expand : bool
        If `True`, expand the coordinate axes by some factor. If `False`,
        use the limits from the data.
    """

    trans_x: trans
    trans_y: trans

    def __init__(
        self,
        x: str | trans = "identity",
        y: str | trans = "identity",
        xlim: Optional[tuple[float, float]] = None,
        ylim: Optional[tuple[float, float]] = None,
        expand: bool = True,
    ):
        from mizani.transforms import gettrans

        self.trans_x = gettrans(x)
        self.trans_y = gettrans(y)
        self.limits = NS(x=xlim, y=ylim)
        self.expand = expand

    def transform(
        self, data: pd.DataFrame, panel_params: panel_view, munch: bool = False
    ) -> pd.DataFrame:
        pass

    def backtransform_range(self, panel_params: panel_view) -> panel_ranges:
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


def transform_value(trans: trans, value: TFloatArrayLike) -> TFloatArrayLike:
    """
    Transform value
    """
    pass
