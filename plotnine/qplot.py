from __future__ import annotations

import typing
from contextlib import suppress
from warnings import warn

import numpy as np
import pandas as pd

from ._utils import array_kind
from ._utils.registry import Registry
from .exceptions import PlotnineError, PlotnineWarning
from .facets import facet_grid, facet_null, facet_wrap
from .facets.facet_grid import parse_grid_facets_old
from .facets.facet_wrap import parse_wrap_facets_old
from .ggplot import ggplot
from .labels import labs
from .mapping.aes import ALL_AESTHETICS, SCALED_AESTHETICS, aes
from .scales import lims, scale_x_log10, scale_y_log10
from .themes import theme

if typing.TYPE_CHECKING:
    from typing import Any, Iterable, Literal, Optional, Sequence

    from plotnine.typing import DataLike

__all__ = ("qplot",)


def qplot(
    x: Optional[str | Iterable[Any] | range] = None,
    y: Optional[str | Iterable[Any] | range] = None,
    data: Optional[DataLike] = None,
    facets: str = "",
    margins: bool | Sequence[str] = False,
    geom: str | Sequence[str] = "auto",
    xlim: Optional[tuple[float, float]] = None,
    ylim: Optional[tuple[float, float]] = None,
    log: Optional[Literal["x", "y", "xy"]] = None,
    main: Optional[str] = None,
    xlab: Optional[str] = None,
    ylab: Optional[str] = None,
    asp: Optional[float] = None,
    **kwargs: Any,
) -> ggplot:
    """
    Quick plot

    Parameters
    ----------
    x :
        x aesthetic
    y :
        y aesthetic
    data :
        Data frame to use (optional). If not specified,
        will create one, extracting arrays from the
        current environment.
    geom :
        *geom(s)* to do the drawing. If `auto`, defaults
        to 'point' if `x` and `y` are specified or
        'histogram' if only `x` is specified.
    facets :
        Facets
    margins :
        variable names to compute margins for. True will compute
        all possible margins. Depends on the facetting.
    xlim :
        x-axis limits
    ylim :
        y-axis limits
    log :
        Which (if any) variables to log transform.
    main :
        Plot title
    xlab :
        x-axis label
    ylab :
        y-axis label
    asp :
        The y/x aspect ratio.
    **kwargs :
        Arguments passed on to the geom.

    Returns
    -------
    :
        ggplot object
    """
    pass
