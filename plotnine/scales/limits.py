import sys
from contextlib import suppress

import pandas as pd

from .._utils import array_kind
from ..exceptions import PlotnineError
from ..geoms import geom_blank
from ..mapping.aes import ALL_AESTHETICS, aes
from ..scales.scales import make_scale


# By adding limits, we create a scale of the appropriate type
class _lim:
    aesthetic = None

    def __init__(self, *limits):
        if not limits:
            msg = "{}lim(), is missing limits"
            raise PlotnineError(msg.format(self.aesthetic))
        elif len(limits) == 1:
            limits = limits[0]

        series = pd.Series(limits)

        # Type of transform
        if not any(x is None for x in limits) and limits[0] > limits[1]:
            self.trans = "reverse"
        elif array_kind.continuous(series):
            self.trans = "identity"
        elif array_kind.discrete(series):
            self.trans = None
        elif array_kind.datetime(series):
            self.trans = "datetime"
        elif array_kind.timedelta(series):
            self.trans = "timedelta"
        else:
            msg = f"Unknown type {type(limits[0])} of limits"
            raise TypeError(msg)

        self.limits = limits
        self.limits_series = series

    def get_scale(self, plot):
        """
        Create a scale
        """
        pass

    def __radd__(self, other):
        scale = self.get_scale(other)
        other.scales.append(scale)
        return other


class xlim(_lim):
    """
    Set x-axis limits

    Parameters
    ----------
    *limits :
        Min and max limits. Must be of size 2.
        You can also pass two values e.g
        `xlim(40, 100)`
    """

    aesthetic = "x"


class ylim(_lim):
    """
    Set y-axis limits

    Parameters
    ----------
    *limits :
        Min and max limits. Must be of size 2.
        You can also pass two values e.g
        `ylim(40, 100)`

    Notes
    -----
    If the 2nd value of `limits` is less than
    the first, a reversed scale will be created.
    """

    aesthetic = "y"


class alphalim(_lim):
    """
    Alpha limits
    """

    aesthetic = "alpha"


class colorlim(_lim):
    """
    Color limits
    """

    aesthetic = "color"


class filllim(_lim):
    """
    Fill limits
    """

    aesthetic = "fill"


class linetypelim(_lim):
    """
    Linetype limits
    """

    aesthetic = "linetype"


class shapelim(_lim):
    """
    Shapee limits
    """

    aesthetic = "shape"


class sizelim(_lim):
    """
    Size limits
    """

    aesthetic = "size"


class strokelim(_lim):
    """
    Stroke limits
    """

    aesthetic = "stroke"


class lims:
    """
    Set aesthetic limits

    Parameters
    ----------
    kwargs :
        Aesthetic and the values of the limits.
        e.g `x=(40, 100)`

    Notes
    -----
    If the 2nd value of `limits` is less than
    the first, a reversed scale will be created.
    """

    def __init__(self, **kwargs):
        self._kwargs = kwargs

    def __radd__(self, other):
        """
        Add limits to ggplot object
        """
        thismodule = sys.modules[__name__]
        for ae, value in self._kwargs.items():
            try:
                klass = getattr(thismodule, f"{ae}lim")
            except AttributeError as e:
                msg = "Cannot change limits for '{}'"
                raise PlotnineError(msg) from e

            other += klass(value)

        return other


def expand_limits(**kwargs):
    """
    Expand the limits any aesthetic using data

    Parameters
    ----------
    kwargs : dict | dataframe
        Data to use in expanding the limits.
        The keys should be aesthetic names
        e.g. *x*, *y*, *colour*, ...
    """
    pass
