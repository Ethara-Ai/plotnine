from __future__ import annotations

from dataclasses import dataclass, field
from itertools import cycle
from typing import TYPE_CHECKING, Sequence

from ..composition._types import ComposeAddable

if TYPE_CHECKING:
    from ._compose import Compose


@dataclass(kw_only=True)
class plot_layout(ComposeAddable):
    """
    Customise the layout of plots in a composition
    """

    nrow: int | None = None
    """
    Number of rows
    """

    ncol: int | None = None
    """
    Number of columns
    """

    byrow: bool | None = None
    """
    How to place plots into the grid.
    If None or True, they are placed row by row, left to right.
    If False, they are placed column by column, top to bottom.
    """

    widths: Sequence[float] | None = None
    """
    Relative widths of each column
    """

    heights: Sequence[float] | None = None
    """
    Relative heights of each column
    """

    _cmp: Compose = field(init=False, repr=False)
    """
    Composition that this layout is attached to
    """

    def __radd__(self, cmp: Compose) -> Compose:
        """
        Add plot layout to composition
        """
        cmp.layout = self
        return cmp

    def _setup(self, cmp: Compose):
        """
        Setup default parameters as they are expected by the layout manager

        - Ensure nrow and ncol have values
        - Ensure the widths & heights are set and normalised to mean=1
        """
        pass

    def update(self, other: plot_layout):
        """
        Update this layout with the contents of other
        """
        pass


def repeat(seq: Sequence[float], n: int) -> list[float]:
    """
    Ensure returned sequence has n values, repeat as necessary
    """
    return [val for _, val in zip(range(n), cycle(seq))]


def normalise(seq: Sequence[float]) -> list[float]:
    """
    Normalise seq so that the mean is 1
    """
    pass
