from .._utils import groupby_apply
from ..doctools import document
from ..mapping.aes import ALL_AESTHETICS
from ..mapping.evaluation import after_stat
from .stat import stat


@document
class stat_sum(stat):
    """
    Sum unique values

    Useful for overplotting on scatterplots.

    {usage}

    Parameters
    ----------
    {common_parameters}

    See Also
    --------
    plotnine.geom_point : The default `geom` for this `stat`.
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "n"     # Number of observations at a position
    "prop"  # Ratio of points in that panel at a position
    ```
    """

    REQUIRED_AES = {"x", "y"}
    DEFAULT_PARAMS = {"geom": "point"}
    DEFAULT_AES = {"size": after_stat("n"), "weight": 1}
    CREATES = {"n", "prop"}

    def compute_panel(self, data, scales):
        pass
