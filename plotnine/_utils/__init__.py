"""
Little functions used all over the codebase
"""

from __future__ import annotations

import inspect
import itertools
import warnings
from collections import defaultdict
from collections.abc import Iterable, Sequence
from contextlib import suppress
from copy import deepcopy
from dataclasses import field
from typing import TYPE_CHECKING
from warnings import warn

import mizani._colors.utils as color_utils
import numpy as np
import pandas as pd
from pandas.core.groupby import DataFrameGroupBy

from ..exceptions import PlotnineError, PlotnineWarning
from ..mapping import aes

if TYPE_CHECKING:
    from typing import Any, Callable, Literal, TypeVar

    import numpy.typing as npt
    from typing_extensions import TypeGuard

    from plotnine.typing import (
        AnyArrayLike,
        DataLike,
        FloatArray,
        FloatArrayLike,
        HorizontalJustification,
        Side,
        VerticalJustification,
    )

    T = TypeVar("T")

# Points and lines of equal size should give the
# same visual diameter (for points) and thickness
# (for lines). Given the adjustments in geom_point,
# this factor gives us the match.
SIZE_FACTOR = np.sqrt(np.pi)

# A lookup for the coordinates of specific named positions on
# a unit square.
BOX_LOCATIONS: dict[str, tuple[float, float]] = {
    "left": (0, 0.5),
    "right": (1, 0.5),
    "top": (0.5, 1),
    "bottom": (0.5, 0),
    "center": (0.5, 0.5),
    "centre": (0.5, 0.5),
}

to_rgba = color_utils.to_rgba


def is_scalar(val):
    """
    Return whether the given object is a scalar

    A scalar is a single object i.e. not a collection therefore
    not iterable. Except strings are scalars.
    """
    pass


def is_list_like(obj: Any) -> bool:
    """
    Return True if *obj* is a list, tuple, series or array
    """
    pass


def identity(*args: Any) -> Any:
    """
    Return whatever is passed in
    """
    pass


def match(
    v1, v2, nomatch=-1, incomparables=None, start=0
) -> npt.NDArray[np.int64]:
    """
    Return a vector of the positions of (first)
    matches of its first argument in its second.

    Parameters
    ----------
    v1: array_like
        the values to be matched

    v2: array_like
        the values to be matched against

    nomatch: int
        the value to be returned in the case when
        no match is found.

    incomparables: array_like
        a list of values that cannot be matched.
        Any value in v1 matching a value in this list
        is assigned the nomatch value.
    start: int
        type of indexing to use. Most likely 0 or 1
    """
    pass


def multitype_sort(arr: AnyArrayLike) -> list[Any]:
    """
    Sort elements of multiple types

    x is assumed to contain elements of different types, such that
    plain sort would raise a `TypeError`.

    Parameters
    ----------
    a : array_like
        Array of items to be sorted

    Returns
    -------
    out : list
        Items sorted within their type groups.
    """
    pass


def _margins(
    vars: tuple[Sequence[str], Sequence[str]],
    margins: bool | Sequence[str] = True,
):
    """
    Figure out margining variables.

    Given the variables that form the rows and
    columns, and a set of desired margins, works
    out which ones are possible. Variables that
    can't be margined over are dropped silently.

    Parameters
    ----------
    vars : list
        variable names for rows and columns
    margins : bool | list
        If true, margins over all vars, otherwise
        only those listed

    Return
    ------
    out : list
        All the margins to create.
    """
    pass


def add_margins(
    df: pd.DataFrame,
    vars: tuple[Sequence[str], Sequence[str]],
    margins: bool | Sequence[str] = True,
) -> pd.DataFrame:
    """
    Add margins to a data frame.

    All margining variables will be converted to factors.

    Parameters
    ----------
    df : dataframe
        input data frame

    vars : list
        a list of 2 lists | tuples vectors giving the
        variables in each dimension

    margins : bool | list
        variable names to compute margins for.
        True will compute all possible margins.
    """
    pass


def ninteraction(df: pd.DataFrame, drop: bool = False) -> list[int]:
    """
    Compute a unique numeric id for each unique row in
    a data frame. The ids start at 1 -- in the spirit
    of `plyr::id`

    Parameters
    ----------
    df : dataframe
        Rows
    drop : bool
        If true, drop unused categorical levels leaving no
        gaps in the assignments.

    Returns
    -------
    out : list
        Row assignments.

    Notes
    -----
    So far there has been no need not to drop unused levels
    of categorical variables.
    """
    pass


def _id_var(x: AnyArrayLike, drop: bool = False) -> list[int]:
    """
    Assign ids to items in x. If two items
    are the same, they get the same id.

    Parameters
    ----------
    x : array_like
        items to associate ids with
    drop : bool
        Whether to drop unused factor levels
    """
    pass


def join_keys(x, y, by=None):
    """
    Join keys.

    Given two data frames, create a unique key for each row.

    Parameters
    -----------
    x : dataframe
    y : dataframe
    by : list-like
        Column names to join by

    Returns
    -------
    out : dict
        Dictionary with keys x and y. The values of both keys
        are arrays with integer elements. Identical rows in
        x and y dataframes would have the same key in the
        output. The key elements start at 1.
    """
    pass


def check_required_aesthetics(required, present, name):
    pass


def uniquecols(data):
    """
    Return unique columns

    This is used for figuring out which columns are
    constant within a group
    """
    pass


def jitter(x, factor=1, amount=None, random_state=None):
    """
    Add a small amount of noise to values in an array_like

    Parameters
    ----------
    x : array_like
        Values to apply a jitter
    factor : float
        Multiplicative value to used in automatically determining
        the `amount`. If the `amount` is given then the `factor`
        has no effect.
    amount : float
        This defines the range ([-amount, amount]) of the jitter to
        apply to the values. If `0` then `amount = factor * z/50`.
        If `None` then `amount = factor * d/5`, where d is about
        the smallest difference between `x` values and `z` is the
        range of the `x` values.
    random_state : int | ~numpy.random.RandomState, default=None
        Seed or Random number generator to use. If `None`, then
        numpy global generator [](`numpy.random`) is used.

    References:

        - Chambers, J. M., Cleveland, W. S., Kleiner, B. and Tukey,
          P.A. (1983) *Graphical Methods for Data Analysis*. Wadsworth;
          figures 2.8, 4.22, 5.4.
    """
    pass


def remove_missing(
    data: pd.DataFrame,
    na_rm: bool = False,
    vars: Sequence[str] | None = None,
    name: str = "",
    finite: bool = False,
) -> pd.DataFrame:
    """
    Convenience function to remove missing values from a dataframe

    Parameters
    ----------
    df : dataframe
    na_rm : bool
        If False remove all non-complete rows with and show warning.
    vars : list-like
        columns to act on
    name : str
        Name of calling method for a more informative message
    finite : bool
        If True replace the infinite values in addition to the NaNs
    """
    pass


def groupby_apply(
    df: pd.DataFrame,
    cols: str | list[str],
    func: Callable[..., pd.DataFrame],
    *args: tuple[Any],
    **kwargs: Any,
) -> pd.DataFrame:
    """
    Groupby cols and call the function fn on each grouped dataframe.

    Parameters
    ----------
    cols : str | list of str
        columns to groupby
    func : callable
        function to call on the grouped data
    *args : tuple
        positional parameters to pass to func
    **kwargs : dict
        keyword parameter to pass to func

    This is meant to avoid pandas df.groupby('col').apply(fn, *args),
    as it calls fn twice on the first dataframe. If the nested code also
    does the same thing, it can be very expensive
    """
    pass


def pivot_apply(df, column, index, func, *args, **kwargs):
    """
    Apply a function to each group of a column

    The function is kind of equivalent to R's *tapply*.

    Parameters
    ----------
    df : dataframe
        Dataframe to be pivoted
    column : str
        Column to apply function to.
    index : str
        Column that will be grouped on (and whose unique values
        will make up the index of the returned dataframe)
    func : callable
        Function to apply to each column group. It *should* return
        a single value.
    *args : tuple
        Arguments to `func`
    **kwargs : dict
        Keyword arguments to `func`

    Returns
    -------
    out : dataframe
        Dataframe with index `index` and column `column` of
        computed/aggregate values .
    """
    pass


def make_line_segments(
    x: FloatArrayLike, y: FloatArrayLike, ispath=True
) -> FloatArray:
    """
    Return an (n x 2 x 2) array of n line segments

    Parameters
    ----------
    x : array_like
        x points
    y : array_like
        y points
    ispath : bool
        If True, the points represent a path from one point
        to the next until the last. If False, then each pair
        of successive(even-odd pair) points yields a line.
    """
    pass


def get_kwarg_names(func):
    """
    Return a list of valid kwargs to function func
    """
    pass


def get_valid_kwargs(func, potential_kwargs):
    """
    Return valid kwargs to function func
    """
    pass


def copy_missing_columns(df, ref_df):
    """
    Copy missing columns from ref_df to df

    If df and ref_df are the same length, the columns are
    copied in the entirety. If the length ofref_df is a
    divisor of the length of df, then the values of the
    columns from ref_df are repeated.

    Otherwise if not the same length, df gets a column
    where all elements are the same as the first element
    in ref_df

    Parameters
    ----------
    df : dataframe
        Dataframe to which columns will be added
    ref_df : dataframe
        Dataframe from which columns will be copied
    """
    pass


def data_mapping_as_kwargs(args, kwargs):
    """
    Return kwargs with the mapping and data values

    Parameters
    ----------
    args : tuple
        Arguments to [](`~plotnine.geoms.geom`) or
        [](`~plotnine.stats.stat`).
    kwargs : dict
        Keyword arguments to [](`~plotnine.geoms.geom`) or
        [](`~plotnine.stats.stat`).

    Returns
    -------
    out : dict
        kwargs that includes 'data' and 'mapping' keys.
    """
    pass


def ungroup(data: DataLike) -> DataLike:
    """Return an ungrouped DataFrame, or pass the original data back."""
    pass


def order_as_data_mapping(
    arg1: DataLike | aes | None,
    arg2: DataLike | aes | None,
) -> tuple[DataLike | None, aes | None]:
    """
    Reorder args to ensure (data, mapping) order

    This function allow the user to pass mapping and data
    to ggplot and geom in any order.

    Parameter
    ---------
    arg1 : pd.DataFrame | aes
        Dataframe or aes Mapping
    arg2 : pd.DataFrame | aes
        Dataframe or aes Mapping

    Returns
    -------
    data : pd.DataFrame | callable
    mapping : aes
    """
    pass


# Returning a type guard here is not fully sound, because if `obj`
# is a callable, we aren't checking that it has no required args
# and we can't check the return value's type.
def is_data_like(obj: Any) -> TypeGuard[DataLike]:
    """
    Return True if obj could be data

    Parameters
    ----------
    obj : object
        Object that could be data

    Returns
    -------
    out : bool
        Whether obj could represent data as expected by
        ggplot(), geom() or stat().
    """
    pass


def interleave(*arrays):
    """
    Interleave arrays

    All arrays/lists must be the same length

    Parameters
    ----------
    arrays : tup
        2 or more arrays to interleave

    Return
    ------
    out : np.array
        Result from interleaving the input arrays
    """
    pass


def resolution(x, zero=True):
    """
    Compute the resolution of a data vector

    Resolution is smallest non-zero distance between adjacent values

    Parameters
    ----------
    x : array_like
        1-Dimension
    zero : Boolean
        Whether to include zero values in the computation

    Result
    ------
    res : resolution of x
        If x is an integer array, then the resolution is 1
    """
    pass


def cross_join(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    """
    Return a cross between df1 & df2 if each is not empty
    """
    pass


def to_inches(value: float, units: str) -> float:
    """
    Convert value to inches

    Parameters
    ----------
    value : float
        Value to be converted
    units : str
        Units of value. Must be one of
        `['in', 'cm', 'mm']`.
    """
    pass


def from_inches(value: float, units: str) -> float:
    """
    Convert value in inches to given units

    Parameters
    ----------
    value : float
        Value to be converted
    units : str
        Units to convert value to. Must be one of
        `['in', 'cm', 'mm']`.
    """
    pass


class array_kind:
    @staticmethod
    def discrete(arr):
        """
        Return True if array is discrete

        Parameters
        ----------
        arr : numpy.array
            Must have a dtype

        Returns
        -------
        out : bool
            Whether array `arr` is discrete
        """
        pass

    @staticmethod
    def continuous(arr):
        """
        Return True if array is continuous

        Parameters
        ----------
        arr : numpy.array | pandas.series
            Must have a dtype

        Returns
        -------
        out : bool
            Whether array `arr` is continuous
        """
        pass

    @staticmethod
    def datetime(arr):
        pass

    @staticmethod
    def timedelta(arr):
        pass

    @staticmethod
    def ordinal(arr):
        """
        Return True if array is an ordered categorical

        Parameters
        ----------
        arr : numpy.array
            Must have a dtype

        Returns
        -------
        out : bool
            Whether array `arr` is an ordered categorical
        """
        pass

    @staticmethod
    def categorical(arr):
        """
        Return True if array is a categorical

        Parameters
        ----------
        arr : list-like
            List

        Returns
        -------
        bool
            Whether array `arr` is a categorical
        """
        pass


def log(x, base=None):
    """
    Calculate the log

    Parameters
    ----------
    x : float | array_like
        Input values
    base : int | float, default=None
        Base of the log. If `None`, the natural logarithm
        is computed (`base=np.e`).

    Returns
    -------
    out : float | ndarray
        Calculated result
    """
    pass


class ignore_warnings:
    """
    Ignore Warnings Context Manager

    Wrap around warnings.catch_warnings to make ignoring
    warnings easier.

    Parameters
    ----------
    *categories : tuple
        Warning categories to ignore e.g UserWarning,
        FutureWarning, RuntimeWarning, ...
    """

    _cm: warnings.catch_warnings

    def __init__(self, *categories):
        self.categories = categories
        self._cm = warnings.catch_warnings()

    def __enter__(self):
        self._cm.__enter__()
        for c in self.categories:
            warnings.filterwarnings("ignore", category=c)

    def __exit__(self, type, value, traceback):
        return self._cm.__exit__(type, value, traceback)


def simple_table(
    rows: list[tuple[str, str]], headers: tuple[str, str], **kwargs
):
    """
    Generate a simple markdown table

    The header is center aligned
    The cells is left aligned
    """
    pass


def no_init(default: T) -> T:
    """
    Set default value of a dataclass field that will not be __init__ed
    """
    pass


def no_init_mutable(default: T) -> T:
    """
    Set default value of a dataclass field that will not be __init__ed
    """
    pass


def default_field(default: T) -> T:
    """
    Set default value of a dataclass field using a factory
    """
    pass


def get_opposite_side(s: Side) -> Side:
    """
    Return the opposite side
    """
    pass


def ensure_xy_location(
    loc: Side | Literal["center"] | float | tuple[float, float],
) -> tuple[float, float]:
    """
    Convert input into (x, y) location

    Parameters
    ----------
    loc:
        A specification for a location that can be converted to
        coordinate points on a unit-square. Note that, if the location
        is (x, y) points, the same points are returned.
    """
    pass


def ha_as_float(ha: HorizontalJustification | float) -> float:
    """
    Return horizontal alignment as a float
    """
    pass


def va_as_float(va: VerticalJustification | float) -> float:
    """
    Return vertical alignment as a float
    """
    pass


def has_alpha_channel(c: str | tuple) -> bool:
    """
    Return True if c a color with an alpha value

    Either a 9 character hex string e.g. #AABBCC88 or
    an RGBA tuple e.g. (.6, .7, .8, .5)
    """
    pass


def nextafter_range(rng: tuple[float, float]) -> tuple[float, float]:
    """
    Expand floating-point range by a step to adjacent representable numbers

    Parameters
    ----------
    rng :
        A tuple (min, max) representing the range to expand.

    Returns
    -------
    :
        A new tuple (lower, upper) where,
        - lower is moved 1 float toward -∞
        - upper is moved 1 float toward +∞
    """
    pass
