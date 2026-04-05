from __future__ import annotations

from contextlib import suppress
from dataclasses import dataclass
from typing import TYPE_CHECKING, Sequence, cast
from warnings import warn

import numpy as np
import pandas as pd
from mizani.bounds import censor, expand_range_distinct, rescale, zero_range
from mizani.palettes import identity_pal

from .._utils import match
from ..exceptions import PlotnineError, PlotnineWarning
from ..iapi import range_view, scale_view
from ._expand import expand_range
from ._runtime_typing import (
    ContinuousBreaksUser,
    ContinuousLimitsUser,
    GuideTypeT,
    MinorBreaksUser,
    TransUser,
)
from .range import RangeContinuous
from .scale import scale

if TYPE_CHECKING:
    from typing import Optional

    from mizani.transforms import trans
    from mizani.typing import PCensor, PRescale

    from plotnine.typing import (
        CoordRange,
        FloatArrayLike,
        TFloatArrayLike,
    )


@dataclass(kw_only=True)
class scale_continuous(
    scale[
        RangeContinuous,
        ContinuousBreaksUser,
        ContinuousLimitsUser,
        # subclasses are still generic and must specify the
        # type of the guide
        GuideTypeT,
    ]
):
    """
    Base class for all continuous scales

    Notes
    -----
    If using the class directly all arguments must be
    keyword arguments.
    """

    limits: ContinuousLimitsUser = None
    """
    Limits of the scale. Most commonly, these are the minimum & maximum
    values for the scale. If not specified they are derived from the data.
    It may also be a function that takes the derived limits and transforms
    them into the final limits.
    """

    rescaler: PRescale = rescale
    """
    Function to rescale data points so that they can be handled by the
    palette. Default is to rescale them onto the [0, 1] range. Scales
    that inherit from this class may have another default.
    """

    oob: PCensor = censor
    """
    Function to deal with out of bounds (limits) data points. Default
    is to turn them into `np.nan`, which then get dropped.
    """

    breaks: ContinuousBreaksUser = True
    """
    Major breaks
    """

    minor_breaks: MinorBreaksUser = True
    """
    If a list-like, it is the minor breaks points. If an integer, it is the
    number of minor breaks between any set of major breaks.
    If a function, it should have the signature `func(limits)` and return a
    list-like of consisting of the minor break points.
    If `None`, no minor breaks are calculated. The default is to automatically
    calculate them.
    """

    trans: TransUser = None
    """
    The transformation of the scale. Either name of a trans function or
    a trans function. See [](`mizani.transforms`) for possible options.
    """

    def __post_init__(self):
        super().__post_init__()
        self._range = RangeContinuous()
        self._trans = self._make_trans()
        self.limits = self._prep_limits(self.limits)

    def _prep_limits(
        self, value: ContinuousLimitsUser
    ) -> ContinuousLimitsUser:
        """
        Limits for the continuous scale

        Parameters
        ----------
        value : array_like | callable
            Limits in the dataspace.
        """
        pass

    def _make_trans(self) -> trans:
        """
        Return a valid transform object

        When scales specialise on a specific transform (other than
        the identity transform), the user should know when they
        try to change the transform.

        Parameters
        ----------
        t : mizani.transforms.trans
            Transform object
        """
        pass

    @property
    def final_limits(self) -> tuple[float, float]:
        pass

    def train(self, x: FloatArrayLike):
        """
        Train continuous scale
        """
        pass

    def transform_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform dataframe
        """
        pass

    def transform(self, x: TFloatArrayLike) -> TFloatArrayLike:
        """
        Transform array|series x
        """
        pass

    def inverse_df(self, df):
        """
        Inverse Transform dataframe
        """
        pass

    def inverse(self, x: TFloatArrayLike) -> TFloatArrayLike:
        """
        Inverse transform array|series x
        """
        pass

    @property
    def is_linear_scale(self) -> bool:
        """
        Return True if the scale is linear

        Depends on the transformation.
        """
        pass

    @property
    def domain_is_numerical(self) -> bool:
        """
        Return True if transformation acts on numerical data.

        Depends on the transformation.
        """
        pass

    @property
    def is_log_scale(self) -> bool:
        """
        Return True if the scale is log transformationed
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
        limits: tuple[float, float],
        expand: tuple[float, float] | tuple[float, float, float, float],
        coord_limits: CoordRange | None,
        trans: trans,
    ) -> range_view:
        """
        Calculate the final range in coordinate space
        """
        pass

    def view(
        self,
        limits: Optional[CoordRange] = None,
        range: Optional[CoordRange] = None,
    ) -> scale_view:
        """
        Information about the trained scale
        """
        pass

    def default_expansion(self, mult=0.05, add=0, expand=True):
        """
        Get the default expansion for continuous scale
        """
        pass

    def palette(self, x):
        """
        Map an data values to values of the scale
        """
        pass

    def map(
        self, x: FloatArrayLike, limits: Optional[tuple[float, float]] = None
    ) -> FloatArrayLike:
        pass

    def get_breaks(
        self, limits: Optional[tuple[float, float]] = None
    ) -> Sequence[float]:
        """
        Generate breaks for the axis or legend

        Parameters
        ----------
        limits : list_like | None
            If None the self.limits are used
            They are expected to be in transformed
            space.

        Returns
        -------
        out : array_like

        Notes
        -----
        Breaks are calculated in data space and
        returned in transformed space since all
        data is plotted in transformed space.
        """
        pass

    def get_bounded_breaks(
        self, limits: Optional[tuple[float, float]] = None
    ) -> Sequence[float]:
        """
        Return Breaks that are within limits
        """
        pass

    def get_minor_breaks(
        self,
        major: Sequence[float],
        limits: Optional[tuple[float, float]] = None,
    ) -> Sequence[float]:
        """
        Return minor breaks
        """
        pass

    def get_labels(
        self, breaks: Optional[Sequence[float]] = None
    ) -> Sequence[str]:
        """
        Generate labels for the axis or legend

        Parameters
        ----------
        breaks: None | array_like
            If None, use self.breaks.
        """
        pass
