from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, fields
from functools import cached_property
from typing import TYPE_CHECKING, Literal, cast
from warnings import warn

import numpy as np
import pandas as pd

from .._utils import ensure_xy_location
from .._utils.registry import Registry
from ..exceptions import PlotnineError, PlotnineWarning
from ..iapi import (
    inside_legend,
    legend_artists,
    legend_justifications_view,
    outside_legend,
)
from ..mapping.aes import rename_aesthetics
from .guide import guide

if TYPE_CHECKING:
    from typing import Literal, Optional, Sequence, TypeAlias

    from matplotlib.offsetbox import OffsetBox, PackerBase

    from plotnine import ggplot, guide_colorbar, guide_legend, theme
    from plotnine.iapi import labels_view
    from plotnine.scales.scale import scale
    from plotnine.scales.scales import Scales
    from plotnine.typing import (
        Justification,
        LegendPosition,
        NoGuide,
        Orientation,
        ScaledAestheticsName,
        Side,
    )

    LegendOrColorbar: TypeAlias = (
        guide_legend | guide_colorbar | Literal["legend", "colorbar"]
    )
    LegendOnly: TypeAlias = guide_legend | Literal["legend"]


# Terminology
# -----------
# - A guide is either a legend or colorbar.
#
# - A guide definition (gdef) is an instantiated guide as it
#   is used in the process of creating the legend
#
# - The guides class holds all guides that will appear in the
#   plot
#
# - A guide box is a fully drawn out guide.
#   It is of subclass matplotlib.offsetbox.Offsetbox


@dataclass
class guides:
    """
    Guides for each scale

    Used to assign or remove a particular guide to the scale
    of an aesthetic.
    """

    alpha: Optional[LegendOrColorbar | NoGuide] = None
    """Guide for alpha scale."""

    color: Optional[LegendOrColorbar | NoGuide] = None
    """Guide for color scale."""

    fill: Optional[LegendOrColorbar | NoGuide] = None
    """Guide for fill scale."""

    linetype: Optional[LegendOnly | NoGuide] = None
    """Guide for linetype scale."""

    shape: Optional[LegendOnly | NoGuide] = None
    """Guide for shape scale."""

    size: Optional[LegendOnly | NoGuide] = None
    """Guide for size scale."""

    stroke: Optional[LegendOnly | NoGuide] = None
    """Guide for stroke scale."""

    colour: Optional[LegendOnly | NoGuide] = None
    """Guide for colour scale."""

    def __post_init__(self):
        self.plot: ggplot
        self.plot_scales: Scales
        self.plot_labels: labels_view
        self.elements: GuidesElements
        self._lookup: dict[
            tuple[str, ScaledAestheticsName], tuple[scale, guide]
        ] = {}
        if self.colour is not None and self.color is not None:
            raise ValueError("Got a guide for color and colour, choose one.")
        rename_aesthetics(self)

    def __radd__(self, other: ggplot):
        """
        Add guides to the plot

        Parameters
        ----------
        plot :
            ggplot object being created

        Returns
        -------
        :
            ggplot object with guides.
        """
        for f in fields(self):
            if (g := getattr(self, f.name)) is not None:
                setattr(other.guides, f.name, g)

        return other

    def _build(self) -> Sequence[guide]:
        """
        Build the guides

        Returns
        -------
        :
            The individual guides for which the geoms that draw them have
            have been created.
        """
        pass

    def _setup(self, plot: ggplot):
        """
        Setup all guides that will be active
        """
        pass

    def _train(self) -> Sequence[guide]:
        """
        Compute all the required guides

        Returns
        -------
        gdefs : list
            Guides for the plots
        """
        pass

    def _merge(self, gdefs: Sequence[guide]) -> Sequence[guide]:
        """
        Merge overlapped guides

        For example:

        ```python
         from plotnine import *
         p = (
            ggplot(mtcars, aes(y="wt", x="mpg", colour="factor(cyl)"))
            + stat_smooth(aes(fill="factor(cyl)"), method="lm")
            + geom_point()
         )
        ```

        would create two guides with the same hash
        """
        pass

    def _create_geoms(
        self,
        gdefs: Sequence[guide],
    ) -> Sequence[guide]:
        """
        Add geoms to the guide definitions
        """
        pass

    def _apply_guide_themes(self, gdefs: list[guide]):
        """
        Apply the theme for each guide
        """
        pass

    def _assemble_guides(
        self,
        gdefs: list[guide],
        boxes: list[PackerBase],
    ) -> legend_artists:
        """
        Assemble guides into Anchored Offset boxes depending on location
        """
        pass

    def draw(self) -> Optional[OffsetBox]:
        """
        Draw guides onto the figure

        Returns
        -------
        :matplotlib.offsetbox.Offsetbox | None
            A box that contains all the guides for the plot.
            If there are no guides, **None** is returned.
        """
        pass


VALID_JUSTIFICATION_WORDS = {"left", "right", "top", "bottom", "center"}


@dataclass
class GuidesElements:
    """
    Theme elements used when assembling the guides object

    This class is meant to provide convenient access to all the required
    elements having worked out good defaults for the unspecified values.
    """

    theme: theme

    @cached_property
    def box(self) -> Orientation:
        """
        The direction to layout the guides
        """
        pass

    @cached_property
    def position(self) -> LegendPosition | Literal["none"]:
        pass

    @cached_property
    def _position_inside(self) -> LegendPosition:
        # We return the position inside the panels when it is explicitly
        # set. Otherwise we return the justification inside the panels.
        # We convert the string (left, right, ...) justifications into
        # locations which justify the legend along the edges of the panel
        # area.
        # Overall when only the inside position is set, the same value is
        # applied to the justification and vice-versa. Always defaulting
        # to a center justification can have the legends close to the
        # edge go out of bounds.
        pass

    @cached_property
    def box_just(self) -> Justification | Literal["baseline"]:
        pass

    @cached_property
    def box_margin(self) -> int:
        pass

    @cached_property
    def spacing(self) -> float:
        pass

    @cached_property
    def justification(self) -> legend_justifications_view:
        # Don't bother, the legend has been turned off
        pass
