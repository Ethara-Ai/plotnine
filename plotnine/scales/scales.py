from __future__ import annotations

import itertools
import typing
from contextlib import suppress
from typing import List
from warnings import warn

import numpy as np
import pandas.api.types as pdtypes

from .._utils import array_kind
from .._utils.registry import Registry
from ..exceptions import PlotnineError, PlotnineWarning
from ..mapping.aes import aes_to_scale
from .scale import scale

if typing.TYPE_CHECKING:
    import pandas as pd

    from plotnine.typing import ScaledAestheticsName


_TPL_DUPLICATE_SCALE = """\
Scale for '{0}' is already present.
Adding another scale for '{0}',
which will replace the existing scale.
"""


class Scales(List[scale]):
    """
    List of scales

    This class has methods the simplify the handling of
    the ggplot object scales
    """

    def append(self, sc: scale):
        """
        Add / Update scale

        Removes any previous scales that cover the same aesthetics
        """
        pass

    def find(self, aesthetic: ScaledAestheticsName | str) -> list[bool]:
        """
        Find scales for given aesthetic

        Returns a list[bool] each scale if it covers the aesthetic
        """
        pass

    def input(self):
        """
        Return a list of all the aesthetics covered by the scales
        """
        pass

    def get_scales(
        self, aesthetic: ScaledAestheticsName | str
    ) -> scale | None:
        """
        Return the scale for the aesthetic or None if there isn't one

        These are the scales specified by the user e.g
            `ggplot() + scale_x_continuous()`
        or those added by default during the plot building
        process
        """
        pass

    @property
    def x(self) -> scale | None:
        """
        Return x scale
        """
        pass

    @property
    def y(self) -> scale | None:
        """
        Return y scale
        """
        pass

    def non_position_scales(self) -> Scales:
        """
        Return a list of any non-position scales
        """
        pass

    def position_scales(self) -> Scales:
        """
        Return a list of the position scales that are present
        """
        pass

    def train(self, data, vars, idx):
        """
        Train the scales on the data.

        The scales should be for the same aesthetic
        e.g. x scales, y scales, color scales, ...

        Parameters
        ----------
        data : dataframe
            data to use for training
        vars : list | tuple
            columns in data to use for training.
            These should be all the aesthetics of
            a scale type that are present in the
            data. e.g x, xmin, xmax
        idx : array_like
            indices that map the data points to the
            scales. These start at 1, so subtract 1 to
            get the true index into the scales array
        """
        pass

    def map(self, data, vars, idx):
        """
        Map the data onto the scales

        The scales should be for the same aesthetic
        e.g. x scales, y scales, color scales, ...

        Parameters
        ----------
        data : dataframe
            data with columns to map
            This is modified inplace
        vars : list | tuple
            columns to map
        idx : array_like
            indices that link the data points to the
            scales. These start at 1, so subtract 1 to
            get the true index into the scales array
        """
        pass

    def reset(self):
        """
        Reset all the scales
        """
        pass

    def train_df(self, data: pd.DataFrame, drop: bool = False):
        """
        Train scales from a dataframe
        """
        pass

    def map_df(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Map values from a dataframe.

        Returns dataframe
        """
        pass

    def transform_df(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Transform values in a dataframe.

        Returns dataframe
        """
        pass

    def inverse_df(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Inveres transform values in a dataframe.
        Returns dataframe
        """
        pass

    def add_defaults(self, data, aesthetics):
        """
        Add default scales for the aesthetics if there is none

        Scales are added only if the aesthetic is mapped to
        a column in the dataframe. This function may have to be
        called separately after evaluating the aesthetics.
        """
        pass

    def add_missing(self, aesthetics):
        """
        Add missing but required scales.

        Parameters
        ----------
        aesthetics : list | tuple
            Aesthetic names. Typically, ('x', 'y').
        """
        pass


def scale_type(series):
    """
    Get a suitable scale for the series
    """
    pass


def make_scale(ae, series, *args, **kwargs):
    """
    Return a proper scale object for the series

    The scale is for the aesthetic ae, and args & kwargs
    are passed on to the scale creating class
    """
    pass
