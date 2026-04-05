from __future__ import annotations

import typing

import numpy as np
import pandas as pd

from .._utils import add_margins, cross_join, join_keys, match, ninteraction
from ..exceptions import PlotnineError
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
    from plotnine.typing import FacetSpaceRatios


class facet_grid(facet):
    """
    Wrap 1D Panels onto 2D surface

    Parameters
    ----------
    rows :
        Variable expressions along the rows of the facets/panels.
        Each expression is evaluated within the context of the dataframe.
    cols :
        Variable expressions along the columns of the facets/panels.
        Each expression is evaluated within the context of the dataframe.
    margins :
        variable names to compute margins for.
        True will compute all possible margins.
    space :
        Control the size of the  `x` or `y` sides of the panels.
        The size also depends to the `scales` parameter.

        If a string, it should be one of
        `['fixed', 'free', 'free_x', 'free_y']`{.py}.

        If a `dict`, it indicates the relative facet size ratios such as:

        ```python
        {"x": [1, 2], "y": [3, 1, 1]}
        ```

        This means that in the horizontal direction, the second panel
        will be twice the length of the first. In the vertical direction
        the top facet will be the 3 times longer then the second and
        third facets.

        Note that the number of dimensions in the list must equal the
        number of facets that will be produced.
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
    """

    def __init__(
        self,
        rows: Optional[str | Sequence[str]] = None,
        cols: Optional[str | Sequence[str]] = None,
        *,
        margins: bool | Sequence[str] = False,
        scales: Literal["fixed", "free", "free_x", "free_y"] = "fixed",
        space: (
            Literal["fixed", "free", "free_x", "free_y"] | FacetSpaceRatios
        ) = "fixed",
        shrink: bool = True,
        labeller: Literal[
            "label_value", "label_both", "label_context"
        ] = "label_value",
        as_table: bool = True,
        drop: bool = True,
    ):
        facet.__init__(
            self,
            scales=scales,
            shrink=shrink,
            labeller=labeller,
            as_table=as_table,
            drop=drop,
        )
        self.rows, self.cols = parse_grid_rows_cols(rows, cols)
        self.space = space
        self.margins = margins

    def _make_gridspec(self):
        """
        Create gridspec for the panels
        """
        pass

    def compute_layout(self, data: list[pd.DataFrame]) -> pd.DataFrame:
        pass

    def map(self, data: pd.DataFrame, layout: pd.DataFrame) -> pd.DataFrame:
        pass

    def make_strips(self, layout_info: layout_details, ax: Axes) -> Strips:
        pass


def parse_grid_rows_cols(
    rows: Optional[str | Sequence[str]] = None,
    cols: Optional[str | Sequence[str]] = None,
) -> tuple[list[str], list[str]]:
    """
    Return the rows & cols that make up the grid
    """
    pass


def parse_grid_facets_old(
    facets: str | tuple[str | Sequence[str], str | Sequence[str]],
) -> tuple[list[str], list[str]]:
    """
    Return two lists of facetting variables, for the rows & columns

    This parse the old & silently deprecated style.
    """
    pass


def ensure_list_spec(term: Sequence[str] | str) -> Sequence[str]:
    """
    Convert a str specification to a list spec

    e.g.
    'a' -> ['a']
    'a + b' -> ['a', 'b']
    '.' -> []
    '' -> []
    """
    pass
