from warnings import warn

import pandas as pd

from ..doctools import document
from ..exceptions import PlotnineWarning
from .stat import stat


# method_args are any of the keyword args (other than q) for
# statsmodels.regression.quantile_regression.QuantReg.fit
@document
class stat_quantile(stat):
    """
    Compute quantile regression lines

    {usage}

    Parameters
    ----------
    {common_parameters}
    quantiles : tuple, default=(0.25, 0.5, 0.75)
        Quantiles of y to compute
    formula : str, default="y ~ x"
        Formula relating y variables to x variables
    method_args : dict, default=None
        Extra arguments passed on to the model fitting method,
        [](`~statsmodels.regression.quantile_regression.QuantReg.fit`).

    See Also
    --------
    plotnine.geom_quantile : The default `geom` for this `stat`.
    statsmodels.regression.quantile_regression.QuantReg
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "quantile"  # quantile
    "group"     # group identifier
    ```

    Calculated aesthetics are accessed using the `after_stat` function.
    e.g. `after_stat('quantile')`{.py}.
    """

    REQUIRED_AES = {"x", "y"}
    DEFAULT_PARAMS = {
        "geom": "quantile",
        "quantiles": (0.25, 0.5, 0.75),
        "formula": "y ~ x",
        "method_args": {},
    }
    CREATES = {"quantile", "group"}

    def setup_params(self, data):
        pass

    def compute_group(self, data, scales):
        pass


def quant_pred(q, data, params):
    """
    Quantile precitions
    """
    pass
