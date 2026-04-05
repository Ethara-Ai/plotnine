"""
Margin
"""

from __future__ import annotations

from contextlib import suppress
from copy import copy
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable, Literal

    from plotnine import theme


@dataclass
class margin:
    """
    Margin
    """

    t: float = 0
    """
    Top margin
    """

    r: float = 0
    """
    Right margin
    """

    b: float = 0
    """
    Bottom margin
    """

    l: float = 0
    """
    Left Margin
    """

    unit: Literal["pt", "in", "lines", "fig"] = "pt"
    """
    The units (coordinate space) of the values
    """

    # These are set by the themeable when it is applied
    fontsize: float = field(init=False, default=0)
    """
    Font size of text that this margin applies to
    """

    figure_size: tuple[float, float] = field(init=False, default=(0, 0))
    """
    Size of the figure in inches
    """

    def setup(self, theme: theme, themeable_name: str):
        """
        Setup the margin to be used in the layout

        For the margin's values to be useful, we need to be able to
        convert them to different units as is required. Here we get
        all the parameters that we shall need to do the conversions.
        """
        pass

    @property
    def pt(self) -> margin:
        """
        Return margin in points

        These are the units of the display coordinate system
        """
        pass

    @property
    def inch(self) -> margin:
        """
        Return margin in inches

        These are the units of the figure-inches coordinate system
        """
        pass

    @property
    def lines(self) -> margin:
        """
        Return margin in lines units
        """
        pass

    @property
    def fig(self) -> margin:
        """
        Return margin in figure units

        These are the units of the figure coordinate system
        """
        pass

    def to(self, unit: Literal["pt", "in", "lines", "fig"]) -> margin:
        """
        Return margin in request unit
        """
        pass

    def _convert(self, conversion: str, D: float, value: float) -> float:
        pass


def margin_auto(
    t: float = 0.0,
    r: float | None = None,
    b: float | None = None,
    l: float | None = None,
    unit: Literal["pt", "in", "lines", "fig"] = "pt",
) -> margin:
    """
    Create margin with minimal arguments
    """
    pass
