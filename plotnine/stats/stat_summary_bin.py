from typing import TYPE_CHECKING, cast

import numpy as np
import pandas as pd

from .._utils import groupby_apply
from ..doctools import document
from ..exceptions import PlotnineWarning
from ..scales.scale_discrete import scale_discrete
from .binning import fuzzybreaks
from .stat import stat
from .stat_summary import make_summary_fun

if TYPE_CHECKING:
    from plotnine.typing import IntArray


@document
class stat_summary_bin(stat):
    """
    Summarise y values at x intervals

    {usage}

    Parameters
    ----------
    {common_parameters}
    binwidth : float | tuple, default=None
        The width of the bins. The default is to use bins bins that
        cover the range of the data. You should always override this
        value, exploring multiple widths to find the best to illustrate
        the stories in your data.
    bins : int | tuple, default=30
        Number of bins. Overridden by binwidth.
    breaks : array_like | tuple[array_like, array_like], default=None
        Bin boundaries. This supersedes the `binwidth`, `bins`
        and `boundary` arguments.
    boundary : float | tuple, default=None
        A boundary between two bins. As with center, things are
        shifted when boundary is outside the range of the data.
        For example, to center on integers, use `width=1`{.py} and
        `boundary=0.5`{.py}, even if 1 is outside the range of the
        data. At most one of center and boundary may be specified.
    fun_data : str | callable, default="mean_se"
        If a string, should be one of `mean_cl_boot`, `mean_cl_normal`,
        `mean_sdl`, `median_hilow`, `mean_se`.
        If a function, it should that takes an array and return a
        dataframe with three rows indexed as `y`, `ymin` and `ymax`.
    fun_y : callable, default=None
        A function that takes an array_like and returns a single value
    fun_ymax : callable, default=None
        A function that takes an array_like and returns a single value
    fun_args : dict, default=None
        Arguments to any of the functions. Provided the names of the
        arguments of the different functions are in not conflict, the
        arguments will be assigned to the right functions. If there is
        a conflict, create a wrapper function that resolves the
        ambiguity in the argument names.
    random_state : int | ~numpy.random.RandomState, default=None
        Seed or Random number generator to use. If `None`, then
        numpy global generator [](`numpy.random`) is used.

    Notes
    -----
    The *binwidth*, *bins*, *breaks* and *boundary* arguments can be a
    tuples with two values `(xaxis-value, yaxis-value)` of the
    required type.

    See Also
    --------
    plotnine.geom_pointrange : The default `geom` for this `stat`.
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "bin"    # bin identifier
    "width"  # bin width
    "ymin"   # ymin computed by the summary function
    "ymax"   # ymax computed by the summary function
    ```

    Calculated aesthetics are accessed using the `after_stat` function.
    e.g. `after_stat('ymin')`{.py}.
    """

    REQUIRED_AES = {"x", "y"}
    DEFAULT_PARAMS = {
        "geom": "pointrange",
        "bins": 30,
        "breaks": None,
        "binwidth": None,
        "boundary": None,
        "fun_data": None,
        "fun_y": None,
        "fun_ymin": None,
        "fun_ymax": None,
        "fun_args": None,
        "random_state": None,
    }
    CREATES = {"bin", "width", "ymin", "ymax"}

    def setup_params(self, data):
        pass

    def compute_group(self, data, scales):
        pass
