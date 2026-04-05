from __future__ import annotations

import typing

from .._utils import SIZE_FACTOR, to_rgba
from ..coords import coord_flip
from ..doctools import document
from ..exceptions import PlotnineError
from .geom import geom
from .geom_path import geom_path
from .geom_polygon import geom_polygon

if typing.TYPE_CHECKING:
    from typing import Any

    import pandas as pd
    from matplotlib.axes import Axes

    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view
    from plotnine.typing import ColorsLike


@document
class geom_ribbon(geom):
    """
    Ribbon plot

    {usage}

    Parameters
    ----------
    {common_parameters}
    outline_type : Literal["upper", "lower", "both", "full"], default="both"
        How to stroke to outline of the region / area.
        If `upper`, draw only upper bounding line.
        If `lower`, draw only lower bounding line.
        If `both`, draw both upper & lower bounding lines.
        If `full`, draw closed polygon around the area.
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Aesthetics Descriptions**

    `where`

    :   Define where to exclude horizontal regions from being filled.
        Regions between any two `False` values are skipped.
        For sensible demarcation the value used in the *where* predicate
        expression should match the `ymin` value or expression. i.e.

        ```python
         aes(ymin=0, ymax="col1", where="col1 > 0")  # good
         aes(ymin=0, ymax="col1", where="col1 > 10")  # bad

         aes(ymin=col2, ymax="col1", where="col1 > col2")  # good
         aes(ymin=col2, ymax="col1", where="col1 > col3")  # bad
        ```
    """
    DEFAULT_AES = {
        "alpha": 1,
        "color": "none",
        "fill": "#333333",
        "linetype": "solid",
        "size": 0.5,
        "where": True,
    }
    REQUIRED_AES = {"x", "ymax", "ymin"}
    DEFAULT_PARAMS = {"outline_type": "both"}
    draw_legend = staticmethod(geom_polygon.draw_legend)

    def handle_na(self, data: pd.DataFrame) -> pd.DataFrame:
        pass

    def setup_data(self, data: pd.DataFrame) -> pd.DataFrame:
        # The outlines need x and y coordinates
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
    def draw_unit(
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
    ):
        pass

    @staticmethod
    def _draw_outline(
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
    ):
        pass
