from __future__ import annotations

import typing

import numpy as np
import pandas as pd

from ..doctools import document
from ..exceptions import PlotnineError
from ..mapping.evaluation import after_stat
from ..scales.scale_continuous import scale_continuous
from .stat import stat

if typing.TYPE_CHECKING:
    from typing import Callable

    from plotnine.typing import FloatArrayLike


@document
class stat_function(stat):
    """
    Superimpose a function onto a plot

    {usage}

    Parameters
    ----------
    {common_parameters}
    fun : callable
        Function to evaluate.
    n : int, default=101
        Number of points at which to evaluate the function.
    xlim : tuple, default=None
        `x` limits for the range. The default depends on
        the `x` aesthetic. There is not an `x` aesthetic
        then the `xlim` must be provided.
    args : Optional[tuple[Any] | dict[str, Any]], default=None
        Arguments to pass to `fun`.

    See Also
    --------
    plotnine.geom_path : The default `geom` for this `stat`.
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "x"   # x points at which the function is evaluated
    "fx"  # points evaluated at each x
    ```

    """

    DEFAULT_PARAMS = {
        "geom": "path",
        "fun": None,
        "n": 101,
        "args": None,
        "xlim": None,
    }

    DEFAULT_AES = {"y": after_stat("fx")}
    CREATES = {"fx"}

    def __init__(self, mapping=None, data=None, **kwargs):
        if data is None:

            def _data_func(data: pd.DataFrame) -> pd.DataFrame:
                pass

            data = _data_func

        super().__init__(mapping, data, **kwargs)

    def setup_params(self, data):
        pass

    def compute_group(self, data, scales):
        pass
