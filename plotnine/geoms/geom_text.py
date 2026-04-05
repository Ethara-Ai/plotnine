from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING, cast
from warnings import warn

import numpy as np

from .._utils import order_as_data_mapping, to_rgba
from ..doctools import document
from ..exceptions import PlotnineError, PlotnineWarning
from ..positions import position_nudge
from .geom import geom

if TYPE_CHECKING:
    from typing import Any, Sequence

    import pandas as pd
    from matplotlib.axes import Axes
    from matplotlib.offsetbox import DrawingArea
    from matplotlib.text import Text

    from plotnine import aes
    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view
    from plotnine.layer import layer
    from plotnine.typing import DataLike


# Note: hjust & vjust are parameters instead of aesthetics
# due to a limitation imposed by MPL
# see: https://github.com/matplotlib/matplotlib/pull/1181
@document
class geom_text(geom):
    """
    Textual annotations

    {usage}

    Parameters
    ----------
    {common_parameters}
    parse : bool, default=False
        If `True`{.py}, the labels will be rendered with
        [latex](http://matplotlib.org/users/usetex.html).
    nudge_x : float, default=0
        Horizontal adjustment to apply to the text
    nudge_y : float, default=0
        Vertical adjustment to apply to the text
    adjust_text: dict, default=None
        Parameters to [](`~adjustText.adjust_text`) will repel
        overlapping texts. This parameter takes priority of over
        `nudge_x` and `nudge_y`.
        `adjust_text` does not work well when it is used in the
        first layer of the plot, or if it is the only layer.
        For more see the documentation at
        https://github.com/Phlya/adjustText/wiki .
    format_string : str, default=None
        If not `None`{.py}, then the text is formatted with this
        string using [](`str.format`) e.g:

        ```python
        # 2.348 -> "2.35%"
        geom_text(format_string="{:.2f}%")
        ```
    path_effects : list, default=None
        If not `None`{.py}, then the text will use these effects.
        See
        [](https://matplotlib.org/tutorials/advanced/patheffects_guide.html)
        documentation for more details.

    See Also
    --------
    plotnine.geom_label
    matplotlib.text.Text
    matplotlib.patheffects

    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Aesthetics Descriptions**

    `size`

    :   Float or one of:

        ```python
        {
            "xx-small", "x-small", "small", "medium", "large",
            "x-large", "xx-large"
        }
        ```

    `ha`

    :   Horizontal alignment. One of `{"left", "center", "right"}`{.py}.

    `va`

    :   Vertical alignment. One of
        `{"top", "center", "bottom", "baseline", "center_baseline"}`{.py}.

    `family`

    :   Font family. Can be a font name
        e.g. "Arial", "Helvetica", "Times", ... or a family that is one of
        `{"serif", "sans-serif", "cursive", "fantasy", "monospace"}}`{.py}

    `fontweight`

    :   Font weight. A numeric value in range 0-1000 or a string that is
        one of:

        ```python
        {
            "ultralight", "light", "normal", "regular", "book", "medium",
            "roman", "semibold", "demibold", "demi", "bold", "heavy",
            "extra bold", "black"
        }
        ```

    `fontstyle`

    :   Font style. One of `{"normal", "italic", "oblique"}`{.py}.

    `fontvariant`

    :   Font variant. One of `{"normal", "small-caps"}`{.py}.
    """
    DEFAULT_AES = {
        "alpha": 1,
        "angle": 0,
        "color": "black",
        "size": 11,
        "lineheight": 1.2,
        "ha": "center",
        "va": "center",
        "family": None,
        "fontweight": "normal",
        "fontstyle": "normal",
        "fontvariant": None,
    }
    REQUIRED_AES = {"label", "x", "y"}
    DEFAULT_PARAMS = {
        "parse": False,
        "nudge_x": 0,
        "nudge_y": 0,
        "adjust_text": None,
        "format_string": None,
        "path_effects": None,
    }

    def __init__(
        self,
        mapping: aes | None = None,
        data: DataLike | None = None,
        **kwargs: Any,
    ):
        data, mapping = order_as_data_mapping(data, mapping)
        nudge_kwargs = {}
        adjust_text = kwargs.get("adjust_text")
        if adjust_text is None:
            with suppress(KeyError):
                nudge_kwargs["x"] = kwargs["nudge_x"]
            with suppress(KeyError):
                nudge_kwargs["y"] = kwargs["nudge_y"]
            if nudge_kwargs:
                kwargs["position"] = position_nudge(**nudge_kwargs)
        else:
            check_adjust_text()

        # Accommodate the old names
        if mapping and "hjust" in mapping:
            mapping["ha"] = mapping.pop("hjust")

        if mapping and "vjust" in mapping:
            mapping["va"] = mapping.pop("vjust")

        geom.__init__(self, mapping, data, **kwargs)

    def setup_data(self, data: pd.DataFrame) -> pd.DataFrame:
        pass

    def draw_panel(
        self,
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
    ):
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
    def draw_legend(
        data: pd.Series[Any], da: DrawingArea, lyr: layer
    ) -> DrawingArea:
        """
        Draw letter 'a' in the box

        Parameters
        ----------
        data : Series
            Data Row
        da : DrawingArea
            Canvas
        lyr : layer
            Layer

        Returns
        -------
        out : DrawingArea
        """
        pass

    @staticmethod
    def legend_key_size(
        data: pd.Series[Any], min_size: tuple[int, int], lyr: layer
    ) -> tuple[int, int]:
        pass


def check_adjust_text():
    pass


def do_adjust_text(
    texts: Sequence[Text],
    ax: Axes,
    params: dict[str, Any],
    color: Any,
    size: float,
    zorder: float,
):
    pass
