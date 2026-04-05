from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal, Sequence

import numpy as np
import pandas as pd
from mizani.bounds import expand_range_distinct
from mizani.palettes import none_pal

from .._utils import match
from ..iapi import range_view, scale_view
from ._expand import expand_range
from ._runtime_typing import DiscreteBreaksUser, DiscreteLimitsUser
from .range import RangeDiscrete
from .scale import scale

if TYPE_CHECKING:
    from typing import Optional

    from mizani.transforms import trans

    from plotnine.typing import AnyArrayLike, CoordRange


@dataclass(kw_only=True)
class scale_discrete(
    scale[
        RangeDiscrete,
        DiscreteBreaksUser,
        DiscreteLimitsUser,
        Literal["legend"] | None,
    ]
):
    """
    Base class for all discrete scales
    """

    limits: DiscreteLimitsUser = None
    """
    Limits of the scale. These are the categories (unique values) of
    the variables. If is only a subset of the values, those that are
    left out will be treated as missing data and represented with a
    `na_value`.
    """

    breaks: DiscreteBreaksUser = True
    """
    List of major break points. Or a callable that takes a tuple of limits
    and returns a list of breaks. If `True`, automatically calculate the
    breaks.
    """

    drop: bool = True
    """
    Whether to drop unused categories from the scale
    """

    na_translate: bool = True
    """
    If `True` translate missing values and show them. If `False` remove
    missing values.
    """

    na_value: Any = np.nan
    """
    If `na_translate=True`, what aesthetic value should be assigned to the
    missing values. This parameter does not apply to position scales where
    `nan` is always placed on the right.
    """

    guide: Literal["legend"] | None = "legend"

    def __post_init__(self):
        super().__post_init__()
        self._range = RangeDiscrete()

    @property
    def final_limits(self) -> Sequence[str]:
        pass

    def train(self, x: AnyArrayLike, drop=False):
        """
        Train scale

        Parameters
        ----------
        x:
            A column of data to train over
        drop :
            Whether to drop(not include) unused categories

        A discrete range is stored in a list
        """
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
        """
        Calculate the final range in coordinate space
        """
        pass

    def view(
        self,
        limits: Optional[Sequence[str]] = None,
        range: Optional[CoordRange] = None,
    ) -> scale_view:
        """
        Information about the trained scale
        """
        pass

    def default_expansion(self, mult=0, add=0.6, expand=True):
        """
        Get the default expansion for a discrete scale
        """
        pass

    def palette(self, n: int) -> Sequence[Any]:
        """
        Map integer `n` to `n` values of the scale
        """
        pass

    def map(self, x, limits: Optional[Sequence[str]] = None) -> Sequence[Any]:
        """
        Map values in x to a palette
        """
        pass

    def get_breaks(
        self, limits: Optional[Sequence[str]] = None
    ) -> Sequence[str]:
        """
        Return an ordered list of breaks

        The form is suitable for use by the guides e.g.
            ['fair', 'good', 'very good', 'premium', 'ideal']
        """
        pass

    def get_bounded_breaks(
        self, limits: Optional[Sequence[str]] = None
    ) -> Sequence[str]:
        """
        Return Breaks that are within limits
        """
        pass

    def get_labels(
        self, breaks: Optional[Sequence[str]] = None
    ) -> Sequence[str]:
        """
        Generate labels for the legend/guide breaks
        """
        pass

    def transform_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform dataframe
        """
        pass

    def transform(self, x):
        """
        Transform array|series x
        """
        pass

    def inverse_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Inverse Transform dataframe
        """
        pass
