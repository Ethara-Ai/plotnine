from __future__ import annotations

import re
import typing
from warnings import warn

import numpy as np
import pandas as pd

from .._utils import join_keys, match
from ..exceptions import PlotnineError, PlotnineWarning
from .facet import (
    add_missing_facets,
    combine_vars,
    eval_facet_vars,
    facet,
    layout_null,
)
from .strips import Strips, strip

if typing.TYPE_CHECKING:
    from typing import Literal, Optional, Sequence

    from matplotlib.axes import Axes

    from plotnine.iapi import layout_details


class facet_wrap(facet):
    """
    Wrap 1D Panels onto 2D surface

    Parameters
    ----------
    facets :
        Variables to groupby and plot on different panels.
        If a string formula is used it should be right sided,
        e.g `"~ a + b"`, `("a", "b")`
    nrow : int, default=None
        Number of rows
    ncol : int, default=None
        Number of columns
    scales :
        Whether `x` or `y` scales should be allowed (free)
        to vary according to the data on each of the panel.
    shrink :
        Whether to shrink the scales to the output of the
        statistics instead of the raw data.
    labeller :
        How to label the facets. A string value if it should be
        one of `["label_value", "label_both", "label_context"]`{.py}.
    as_table :
        If `True`, the facets are laid out like a table with
        the highest values at the bottom-right. If `False`
        the facets are laid out like a plot with the highest
        value a the top-right
    drop :
        If `True`, all factor levels not used in the data
        will automatically be dropped. If `False`, all
        factor levels will be shown, regardless of whether
        or not they appear in the data.
    dir :
        Direction in which to layout the panels. `h` for
        horizontal and `v` for vertical.
    """

    def __init__(
        self,
        facets: Optional[str | Sequence[str]] = None,
        *,
        nrow: Optional[int] = None,
        ncol: Optional[int] = None,
        scales: Literal["fixed", "free", "free_x", "free_y"] = "fixed",
        shrink: bool = True,
        labeller: Literal[
            "label_value", "label_both", "label_context"
        ] = "label_value",
        as_table: bool = True,
        drop: bool = True,
        dir: Literal["h", "v"] = "h",
    ):
        super().__init__(
            scales=scales,
            shrink=shrink,
            labeller=labeller,
            as_table=as_table,
            drop=drop,
            dir=dir,
        )
        self.vars = parse_wrap_facets(facets)
        self._nrow, self._ncol = check_dimensions(nrow, ncol)

    def compute_layout(
        self,
        data: list[pd.DataFrame],
    ) -> pd.DataFrame:
        pass

    def map(self, data: pd.DataFrame, layout: pd.DataFrame) -> pd.DataFrame:
        pass

    def make_strips(self, layout_info: layout_details, ax: Axes) -> Strips:
        pass


def check_dimensions(
    nrow: Optional[int], ncol: Optional[int]
) -> tuple[int | None, int | None]:
    """
    Verify dimensions of the facet
    """
    pass


def parse_wrap_facets(facets: Optional[str | Sequence[str]]) -> Sequence[str]:
    """
    Return list of facetting variables
    """
    pass


def parse_wrap_facets_old(facets: str | Sequence[str]) -> Sequence[str]:
    """
    Return list of facetting variables

    This handles the old & silently deprecated r-style formulas
    """
    pass


def wrap_dims(
    n: int, nrow: Optional[int] = None, ncol: Optional[int] = None
) -> tuple[int, int]:
    """
    Wrap dimensions
    """
    pass


def n_to_nrow_ncol(n: int) -> tuple[int, int]:
    """
    Compute the rows and columns given the number of plots.
    """
    pass
