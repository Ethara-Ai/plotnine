import numpy as np
import pandas as pd

from .._utils import resolution
from ..doctools import document
from ..exceptions import PlotnineError
from ..mapping.evaluation import after_stat
from .stat import stat


@document
class stat_count(stat):
    """
    Counts the number of cases at each x position

    {usage}

    Parameters
    ----------
    {common_parameters}
    width : float, default=None
        Bar width. If None, set to 90% of the resolution of the data.

    See Also
    --------
    plotnine.geom_histogram : The default `geom` for this `stat`.
    plotnine.stat_bin
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "count"  # Number of observations at a position
    "prop"   # Ratio of points in the panel at a position
    ```

    """

    REQUIRED_AES = {"x"}
    DEFAULT_PARAMS = {
        "geom": "histogram",
        "position": "stack",
        "width": None,
    }
    DEFAULT_AES = {"y": after_stat("count")}
    CREATES = {"count", "prop"}

    def setup_params(self, data):
        pass

    def compute_group(self, data, scales):
        pass
