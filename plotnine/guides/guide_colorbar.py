from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from functools import cached_property
from types import SimpleNamespace as NS
from typing import TYPE_CHECKING, cast
from warnings import warn

import numpy as np
import pandas as pd
from mizani.bounds import rescale

from plotnine.iapi import guide_text

from .._utils import get_opposite_side
from ..exceptions import PlotnineError, PlotnineWarning
from ..mapping.aes import rename_aesthetics
from ..scales.scale_continuous import scale_continuous
from .guide import GuideElements, guide

if TYPE_CHECKING:
    from typing import Literal, Optional, Sequence

    from matplotlib.artist import Artist
    from matplotlib.collections import LineCollection
    from matplotlib.offsetbox import AuxTransformBox, PackerBase
    from matplotlib.text import Text

    from plotnine import theme
    from plotnine.guides import guides
    from plotnine.scales.scale import scale
    from plotnine.typing import Side


@dataclass
class guide_colorbar(guide):
    """
    Guide colorbar

    Notes
    -----
    To correctly place a rasterized colorbar when saving the plot as an `svg`
    or `pdf`, you should set the `dpi` to 72 i.e. `theme(dpi=72)`{.py}.
    """

    nbin: Optional[int] = None
    """
    Number of bins for drawing a colorbar. A larger value yields
    a smoother colorbar
    """

    display: Literal["gradient", "rectangles", "raster"] = "gradient"
    """
    How to render the colorbar

    SVG figures will always use "rectangles" to create gradients. This has
    better support across applications that render svg images.
    """

    alpha: Optional[float] = None
    """
    Opacity (in the range `[0, 1]`) of the colorbar. The default
    `None`, is to use the opacity of the plot.
    """

    draw_ulim: bool = True
    """Whether to show the upper limit tick marks."""

    draw_llim: bool = True
    """Whether to show the lower limit tick marks. """

    # Non-Parameter Attributes
    available_aes: set[str] = field(
        init=False, default_factory=lambda: {"colour", "color", "fill"}
    )

    def __post_init__(self):
        self._elements_cls = GuideElementsColorbar
        self.elements: GuideElementsColorbar

        if self.nbin is None:
            self.nbin = 300  # if self.display == "gradient" else 300

    def setup(self, guides: guides):
        pass

    def train(self, scale: scale, aesthetic=None):
        pass

    def create_geoms(self):
        """
        Return self if colorbar will be drawn and None if not

        This guide is not geom based
        """
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


guide_colourbar = guide_colorbar


def add_gradient_colorbar(
    auxbox: AuxTransformBox,
    colors: Sequence[str],
    alpha: float | None,
    elements: GuideElementsColorbar,
    raster: bool = False,
):
    """
    Add an interpolated gradient colorbar to DrawingArea
    """
    pass


def add_segmented_colorbar(
    auxbox: AuxTransformBox,
    colors: Sequence[str],
    alpha: float | None,
    elements: GuideElementsColorbar,
):
    """
    Add 'non-rastered' colorbar to AuxTransformBox
    """
    pass


def add_ticks(auxbox, locations, elements) -> LineCollection:
    """
    Add ticks to colorbar
    """
    pass


def add_labels(
    auxbox: AuxTransformBox,
    labels: Sequence[str],
    ys: Sequence[float],
    elements: GuideElementsColorbar,
) -> list[Text]:
    """
    Return Texts added to the auxbox
    """
    pass


def add_frame(auxbox, elements):
    """
    Add frame to colorbar
    """
    pass


class GuideElementsColorbar(GuideElements):
    """
    Access & calculate theming for the colobar
    """

    @cached_property
    def text(self):
        pass

    @cached_property
    def text_positions(self) -> Sequence[Side]:
        pass

    @cached_property
    def key_width(self):
        # We scale up the width only if it inherited its value
        pass

    @cached_property
    def key_height(self):
        # We scale up the height only if it inherited its value
        pass

    @cached_property
    def frame(self):
        pass

    @cached_property
    def ticks_length(self):
        pass

    @cached_property
    def ticks(self):
        pass
