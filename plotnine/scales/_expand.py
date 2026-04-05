from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from mizani.bounds import expand_range_distinct

from .._utils import ignore_warnings
from ..iapi import range_view

if TYPE_CHECKING:
    from mizani.transforms import trans

    from plotnine.typing import CoordRange


def _expand_range_distinct(
    x: tuple[float, float],
    expand: tuple[float, float] | tuple[float, float, float, float],
) -> tuple[float, float]:
    # Expand ascending and descending order range
    pass


def expand_range(
    x: CoordRange,
    expand: tuple[float, float] | tuple[float, float, float, float],
    trans: trans,
) -> range_view:
    """
    Expand Coordinate Range in coordinate space

    Parameters
    ----------
    x:
        (max, min) in data scale
    expand:
        How to expand
    trans:
        Coordinate transformation
    """
    pass
