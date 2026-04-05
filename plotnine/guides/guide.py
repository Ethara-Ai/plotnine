from __future__ import annotations

from abc import ABC
from dataclasses import asdict, dataclass, field
from functools import cached_property
from types import SimpleNamespace as NS
from typing import TYPE_CHECKING, cast

from .._utils import ensure_xy_location, get_opposite_side
from .._utils.registry import Register
from ..themes.theme import theme as Theme

if TYPE_CHECKING:
    from typing import Literal, Optional, Sequence, TypeAlias

    import pandas as pd
    from matplotlib.offsetbox import PackerBase
    from typing_extensions import Self

    from plotnine import aes, guides
    from plotnine.iapi import guide_text
    from plotnine.layer import Layers, layer
    from plotnine.scales.scale import scale
    from plotnine.typing import (
        LegendPosition,
        Orientation,
        Side,
    )

    from .guides import GuidesElements

    AlignDict: TypeAlias = dict[
        Literal["ha", "va"], dict[tuple[Orientation, Side], str]
    ]


@dataclass
class guide(ABC, metaclass=Register):
    """
    Base class for all guides

    Notes
    -----
    At the moment not all parameters have been fully implemented.
    """

    title: Optional[str] = None
    """
    Title of the guide. Default is the name of the aesthetic or the
    name specified using [](`~plotnine.components.labels.lab`)
    """

    theme: Theme = field(default_factory=Theme)
    """A theme to style the guide. If `None`, the plots theme is used."""

    position: Optional[LegendPosition] = None
    """Where to place the guide relative to the panels."""

    direction: Optional[Orientation] = None
    """
    Direction of the guide. The default is depends on
    [](`~plotnine.themes.themeable.legend_position`).
    """

    reverse: bool = False
    """Whether to reverse the order of the legend keys."""

    order: int = 0
    """Order of this guide among multiple guides."""

    # Non-Parameter Attributes
    available_aes: set[str] = field(init=False, default_factory=set)

    def __post_init__(self):
        self.hash: str
        self.key: pd.DataFrame
        self.plot_layers: Layers
        self.plot_mapping: aes
        self._elements_cls = GuideElements
        self.elements = cast("GuideElements", None)
        self.guides_elements: GuidesElements

    def legend_aesthetics(self, layer: layer):
        """
        Return the aesthetics that contribute to the legend

        Parameters
        ----------
        layer : Layer
            Layer whose legend is to be drawn

        Returns
        -------
        matched : list
            List of the names of the aethetics that contribute
            to the legend.
        """
        pass

    def setup(self, guides: guides):
        """
        Setup guide for drawing process
        """
        pass

    @property
    def _resolved_position_justification(
        self,
    ) -> tuple[Side, float] | tuple[tuple[float, float], tuple[float, float]]:
        """
        Return the final position & justification to draw the guide
        """
        pass

    @property
    def num_breaks(self) -> int:
        """
        Number of breaks
        """
        pass

    def train(
        self, scale: scale, aesthetic: Optional[str] = None
    ) -> Self | None:
        """
        Create the key for the guide

        Returns guide if training is successful
        """

    def merge(self, other: Self) -> Self:
        """
        Merge with another guide
        """
        pass

    def draw(self) -> PackerBase:
        """
        Draw guide
        """
        raise NotImplementedError

    def create_geoms(self) -> Optional[Self]:
        """
        Create layers of geoms for the guide

        Returns
        -------
        :
            self if geom layers were create or None of no geom layers
            were created.
        """
        raise NotImplementedError


@dataclass
class GuideElements:
    """
    Access & calculate theming for the guide
    """

    theme: Theme
    guide: guide

    @cached_property
    def text(self) -> guide_text:
        raise NotImplementedError

    def __post_init__(self):
        self.guide_kind = type(self.guide).__name__.split("_")[-1]
        self._elements_cls = GuideElements

    @cached_property
    def margin(self):
        pass

    @cached_property
    def title(self):
        pass

    @cached_property
    def text_positions(self) -> Sequence[Side]:
        raise NotImplementedError

    @cached_property
    def _text_margin(self) -> Sequence[float]:
        pass

    @cached_property
    def title_position(self) -> Side:
        pass

    @cached_property
    def direction(self) -> Orientation:
        pass

    @cached_property
    def position(self) -> Side | tuple[float, float]:
        pass

    @cached_property
    def _position_inside(self) -> Side | tuple[float, float]:
        pass

    #  These do not track the themeables directly
    @cached_property
    def is_vertical(self) -> bool:
        """
        Whether the guide is vertical
        """
        pass

    @cached_property
    def is_horizontal(self) -> bool:
        """
        Whether the guide is horizontal
        """
        pass
