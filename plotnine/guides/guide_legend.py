from __future__ import annotations

import hashlib
from contextlib import suppress
from dataclasses import dataclass, field
from functools import cached_property
from itertools import islice
from typing import TYPE_CHECKING, cast
from warnings import warn

import numpy as np
import pandas as pd

from plotnine.iapi import guide_text

from .._utils import remove_missing
from ..exceptions import PlotnineError, PlotnineWarning
from ..mapping.aes import rename_aesthetics
from .guide import GuideElements, guide

if TYPE_CHECKING:
    from typing import Any, Optional, Sequence

    from matplotlib.artist import Artist
    from matplotlib.offsetbox import PackerBase

    from plotnine.geoms.geom import geom
    from plotnine.layer import layer
    from plotnine.typing import Side


# See guides.py for terminology


@dataclass
class LayerParameters:
    geom: geom
    data: pd.DataFrame
    layer: layer


@dataclass
class guide_legend(guide):
    """
    Legend guide
    """

    nrow: Optional[int] = None
    """Number of rows of legends."""

    ncol: Optional[int] = None
    """Number of columns of legends."""

    byrow: bool = False
    """Whether to fill the legend row-wise or column-wise."""

    override_aes: dict[str, Any] = field(default_factory=dict)
    """Aesthetic parameters of legend key."""

    # Non-Parameter Attributes
    available_aes: set[str] = field(
        init=False, default_factory=lambda: {"any"}
    )
    """Aesthetics for which this guide can be used"""

    _layer_parameters: list[LayerParameters] = field(
        init=False, default_factory=list
    )

    def __post_init__(self):
        self._elements_cls = GuideElementsLegend
        self.elements: GuideElementsLegend

    def train(self, scale, aesthetic=None):
        """
        Create the key for the guide

        The key is a dataframe with two columns:

        - scale name : values
        - label : labels for each value

        scale name is one of the aesthetics: `x`, `y`, `color`,
        `fill`, `size`, `shape`, `alpha`, `stroke`.

        Returns this guide if training is successful and None
        if it fails
        """
        pass

    def merge(self, other):
        """
        Merge overlapped guides

        For example:

        ```python
        from ggplot import *
        p = (
            ggplot(aes(x="cut", fill="cut", color="cut"), data=diamonds)
            + stat_bin()
        )
        ```

        Would create similar guides for fill and color where only
        a single guide would do
        """
        pass

    def create_geoms(self):
        """
        Make information needed to draw a legend for each of the layers.

        For each layer, that information is a dictionary with the geom
        to draw the guide together with the data and the parameters that
        will be used in the call to geom.
        """
        pass

    def _calculate_rows_and_cols(
        self, elements: GuideElementsLegend
    ) -> tuple[int, int]:
        pass

    def draw(self):
        """
        Draw guide

        Returns
        -------
        out : matplotlib.offsetbox.Offsetbox
            A drawing of this legend
        """
        pass


class GuideElementsLegend(GuideElements):
    """
    Access & calculate theming for the legend
    """

    @cached_property
    def text(self):
        pass

    @cached_property
    def text_positions(self) -> Sequence[Side]:
        pass

    @cached_property
    def key_spacing_x(self) -> float:
        pass

    @cached_property
    def key_spacing_y(self) -> float:
        pass

    @cached_property
    def _key_dimensions(self) -> list[tuple[float, float]]:
        """
        key width and key height for each legend entry

        Take a peak into data['size'] to make sure the legend key
        dimensions are big enough.
        """
        pass

    @cached_property
    def key_widths(self) -> list[float]:
        """
        Widths of the keys

        If legend is vertical, key widths must be equal, so we use the
        maximum. So a plot like

           (ggplot(diamonds, aes(x="cut", y="clarity"))
            + stat_sum(aes(group="cut"))
            + scale_size(range=(3, 25))
           )

        would have keys with variable heights, but fixed width.
        """
        pass

    @cached_property
    def key_heights(self) -> list[float]:
        """
        Heights of the keys

        If legend is horizontal, then key heights must be equal, so we
        use the maximum
        """
        pass

    @cached_property
    def empty_key_size(self) -> tuple[float, float]:
        """
        Size of an empty key
        """
        pass
