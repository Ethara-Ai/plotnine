from __future__ import annotations

import typing

import pandas as pd

from ..iapi import labels_view, panel_ranges, panel_view
from .coord_cartesian import coord_cartesian

if typing.TYPE_CHECKING:
    from typing import Sequence, TypeVar

    from plotnine.scales.scale import scale

    THasLabels = TypeVar(
        "THasLabels", bound=pd.DataFrame | labels_view | panel_view
    )


class coord_flip(coord_cartesian):
    """
    Flipped cartesian coordinates

    The horizontal becomes vertical, and vertical becomes horizontal.
    This is primarily useful for converting geoms and statistics which
    display y conditional on x, to x conditional on y.

    Parameters
    ----------
    xlim : tuple[float, float], default=None
        Limits for x axis. If None, then they are automatically computed.
    ylim : tuple[float, float], default=None
        Limits for y axis. If None, then they are automatically computed.
    expand : bool, default=True
        If `True`, expand the coordinate axes by some factor. If `False`,
        use the limits from the data.
    """

    def labels(self, cur_labels: labels_view) -> labels_view:
        pass

    def transform(
        self, data: pd.DataFrame, panel_params: panel_view, munch: bool = False
    ) -> pd.DataFrame:
        pass

    def setup_panel_params(self, scale_x: scale, scale_y: scale) -> panel_view:
        pass

    def setup_layout(self, layout: pd.DataFrame) -> pd.DataFrame:
        # switch the scales
        pass

    def range(self, panel_params: panel_view) -> panel_ranges:
        """
        Return the range along the dimensions of the coordinate system
        """
        pass


def flip_labels(obj: THasLabels) -> THasLabels:
    """
    Rename fields x to y and y to x

    Parameters
    ----------
    obj : dict_like | dataclass
        Object with labels to rename
    """
    pass
