from __future__ import annotations

from dataclasses import dataclass
from itertools import chain
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

from .._utils import array_kind, match
from .._utils.registry import alias
from ..exceptions import PlotnineError
from ..iapi import range_view
from ._expand import expand_range
from ._runtime_typing import TransUser  # noqa: TCH001
from .range import RangeContinuous
from .scale_continuous import scale_continuous
from .scale_datetime import scale_datetime
from .scale_discrete import scale_discrete

if TYPE_CHECKING:
    from typing import Sequence

    from mizani.transforms import trans


# positions scales have a couple of differences (quirks) that
# make necessary to override some of the scale_discrete and
# scale_continuous methods
#
# scale_position_discrete and scale_position_continuous
# are intermediate base classes where the required overriding
# is done
@dataclass(kw_only=True)
class scale_position_discrete(scale_discrete):
    """
    Base class for discrete position scales
    """

    def __post_init__(self):
        super().__post_init__()
        # Keeps two ranges, range and range_c
        self._range_c = RangeContinuous()
        if isinstance(self.limits, tuple):
            self.limits = list(self.limits)

        # All positions have no guide
        self.guide = None

    def reset(self):
        # Can't reset discrete scale because
        # no way to recover values
        pass

    def is_empty(self) -> bool:
        pass

    def train(self, x, drop=False):
        # The discrete position scale is capable of doing
        # training for continuous data.
        # This complicates training and mapping, but makes it
        # possible to place objects at non-integer positions,
        # as is necessary for jittering etc.
        pass

    def map(self, x, limits=None):
        # Discrete values are converted into integers starting
        # at 1
        pass

    @property
    def final_limits(self):
        pass

    def dimension(self, expand=(0, 0, 0, 0), limits=None):
        """
        Get the phyical size of the scale

        Unlike limits, this always returns a numeric vector of length 2
        """
        pass

    def expand_limits(
        self,
        limits: Sequence[str],
        expand: tuple[float, float] | tuple[float, float, float, float],
        coord_limits: tuple[float, float],
        trans: trans,
    ) -> range_view:
        # Turn discrete limits into a tuple of continuous limits
        pass


@dataclass(kw_only=True)
class scale_position_continuous(scale_continuous[None]):
    """
    Base class for continuous position scales
    """

    guide: None = None

    def map(self, x, limits=None):
        # Position aesthetics don't map, because the coordinate
        # system takes care of it.
        # But the continuous scale has to deal with out of bound points
        pass


@dataclass(kw_only=True)
class scale_x_discrete(scale_position_discrete):
    """
    Discrete x position
    """

    _aesthetics = ["x", "xmin", "xmax", "xend", "xintercept"]


@dataclass(kw_only=True)
class scale_y_discrete(scale_position_discrete):
    """
    Discrete y position
    """

    _aesthetics = ["y", "ymin", "ymax", "yend", "yintercept"]


# Not part of the user API
@alias
class scale_x_ordinal(scale_x_discrete):
    pass


@alias
class scale_y_ordinal(scale_y_discrete):
    pass


@dataclass(kw_only=True)
class scale_x_continuous(scale_position_continuous):
    """
    Continuous x position
    """

    _aesthetics = ["x", "xmin", "xmax", "xend", "xintercept"]


@dataclass(kw_only=True)
class scale_y_continuous(scale_position_continuous):
    """
    Continuous y position
    """

    _aesthetics = [
        "y",
        "ymin",
        "ymax",
        "yend",
        "yintercept",
        "ymin_final",
        "ymax_final",
        "lower",
        "middle",
        "upper",
    ]


# Transformed scales
@dataclass(kw_only=True)
class scale_x_datetime(scale_datetime, scale_x_continuous):  # pyright: ignore[reportIncompatibleVariableOverride]
    """
    Continuous x position for datetime data points
    """

    guide: None = None


@dataclass(kw_only=True)
class scale_y_datetime(scale_datetime, scale_y_continuous):  # pyright: ignore[reportIncompatibleVariableOverride]
    """
    Continuous y position for datetime data points
    """

    guide: None = None


@alias
class scale_x_date(scale_x_datetime):
    pass


@alias
class scale_y_date(scale_y_datetime):
    pass


@dataclass(kw_only=True)
class scale_x_timedelta(scale_x_continuous):
    """
    Continuous x position for timedelta data points
    """

    trans: TransUser = "pd_timedelta"


@dataclass(kw_only=True)
class scale_y_timedelta(scale_y_continuous):
    """
    Continuous y position for timedelta data points
    """

    trans: TransUser = "pd_timedelta"


@dataclass(kw_only=True)
class scale_x_sqrt(scale_x_continuous):
    """
    Continuous x position sqrt transformed scale
    """

    trans: TransUser = "sqrt"


@dataclass(kw_only=True)
class scale_y_sqrt(scale_y_continuous):
    """
    Continuous y position sqrt transformed scale
    """

    trans: TransUser = "sqrt"


@dataclass(kw_only=True)
class scale_x_log10(scale_x_continuous):
    """
    Continuous x position log10 transformed scale
    """

    trans: TransUser = "log10"


@dataclass(kw_only=True)
class scale_y_log10(scale_y_continuous):
    """
    Continuous y position log10 transformed scale
    """

    trans: TransUser = "log10"


@dataclass(kw_only=True)
class scale_x_reverse(scale_x_continuous):
    """
    Continuous x position reverse transformed scale
    """

    trans: TransUser = "reverse"


@dataclass(kw_only=True)
class scale_y_reverse(scale_y_continuous):
    """
    Continuous y position reverse transformed scale
    """

    trans: TransUser = "reverse"


@dataclass(kw_only=True)
class scale_x_symlog(scale_x_continuous):
    """
    Continuous x position symmetric logarithm transformed scale
    """

    trans: TransUser = "symlog"


@dataclass(kw_only=True)
class scale_y_symlog(scale_y_continuous):
    """
    Continuous y position symmetric logarithm transformed scale
    """

    trans: TransUser = "symlog"
