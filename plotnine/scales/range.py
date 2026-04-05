from __future__ import annotations

import typing

from mizani.scale import scale_continuous, scale_discrete

if typing.TYPE_CHECKING:
    from typing import Any, Sequence

    from plotnine.typing import AnyArrayLike, FloatArrayLike


class Range:
    """
    Base class for all ranges
    """

    # Holds the range information after training
    range: Any

    def reset(self):
        """
        Reset range
        """
        pass

    def train(self, x: Sequence[Any]):
        """
        Train range
        """
        raise NotImplementedError("Not Implemented.")

    def is_empty(self) -> bool:
        """
        Whether there is range information
        """
        pass


class RangeContinuous(Range):
    """
    Continuous Range
    """

    range: tuple[float, float]

    def train(self, x: FloatArrayLike):
        """
        Train continuous range
        """
        pass


class RangeDiscrete(Range):
    """
    Discrete Range
    """

    range: Sequence[Any]

    def train(self, x: AnyArrayLike, drop: bool = False, na_rm: bool = False):
        """
        Train discrete range
        """
        pass
