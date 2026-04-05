from __future__ import annotations

import numbers
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
import pandas.api.types as pdtypes

from ..exceptions import PlotnineError
from ._eval_environment import factor, reorder

if TYPE_CHECKING:
    from typing import Any

    from . import aes
    from ._env import Environment


__all__ = ("after_stat", "after_scale", "stage")


EVAL_ENVIRONMENT = {"factor": factor, "reorder": reorder}

_TPL_EVAL_FAIL = """\
Could not evaluate the '{}' mapping: '{}' \
(original error: {})"""

_TPL_BAD_EVAL_TYPE = """\
The '{}' mapping: '{}' produced a value of type '{}',\
but only single items and lists/arrays can be used. \
(original error: {})"""


class stage:
    """
    Stage allows you evaluating mapping at more than one stage

    You can evaluate an expression of a variable in a dataframe, and
    later evaluate an expression that modifies the values mapped to
    the scale.

    Parameters
    ----------
    start : str | array_like | scalar
        Aesthetic expression using primary variables from the layer
        data.
    after_stat : str
        Aesthetic expression using variables calculated by the stat.
    after_scale : str
        Aesthetic expression using aesthetics of the layer.
    """

    def __init__(self, start=None, after_stat=None, after_scale=None):
        self.start = start
        self.after_stat = after_stat
        self.after_scale = after_scale

    def __repr__(self):
        """
        Repr for staged mapping
        """
        # Shorter representation when the mapping happens at a
        # single stage
        if self.after_stat is None and self.after_scale is None:
            return f"{repr(self.start)}"
        if self.start is None and self.after_scale is None:
            return f"after_stat({repr(self.after_stat)})"
        if self.start is None and self.after_stat is None:
            return f"after_scale({repr(self.after_scale)})"
        return (
            f"stage(start={repr(self.start)}, "
            f"after_stat={repr(self.after_stat)}, "
            f"after_scale={repr(self.after_scale)})"
        )


def after_stat(x):
    """
    Evaluate mapping after statistic has been calculated

    Parameters
    ----------
    x : str
        An expression

    See Also
    --------
    plotnine.after_scale
    plotnine.stage
    """
    return stage(after_stat=x)


def after_scale(x):
    """
    Evaluate mapping after variable has been mapped to the scale

    This gives the user a chance to alter the value of a variable
    in the final units of the scale e.g. the rgb hex color.

    Parameters
    ----------
    x : str
        An expression

    See Also
    --------
    plotnine.after_stat
    plotnine.stage
    """
    pass


def evaluate(
    aesthetics: aes | dict[str, Any], data: pd.DataFrame, env: Environment
) -> pd.DataFrame:
    """
    Evaluate aesthetics

    Parameters
    ----------
    aesthetics :
        Aesthetics to evaluate. They must be of the form {name: expr}
    data :
        Dataframe whose columns are/may-be variables in the aesthetic
        expressions i.e. it is a namespace with variables.
    env :
        Environment in which the aesthetics are evaluated

    Returns
    -------
    pd.DataFrame
        Dataframe of the form {name: result}, where each column is the
        result from evaluating an expression.

    Examples
    --------
    >>> from plotnine.mapping import Environment
    >>> var1 = 2
    >>> env = Environment.capture()
    >>> df = pd.DataFrame({'x': range(1, 6)})
    >>> aesthetics = {'y': 'x**var1'}
    >>> evaluate(aesthetics, df, env)
        y
    0   1
    1   4
    2   9
    3  16
    4  25
    """
    pass


def is_known_scalar(value):
    """
    Return True if value is a type we expect in a dataframe
    """
    pass
