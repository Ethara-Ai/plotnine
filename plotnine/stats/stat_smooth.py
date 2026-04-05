import warnings

import numpy as np
import pandas as pd

from ..doctools import document
from ..exceptions import PlotnineWarning
from .smoothers import predictdf
from .stat import stat


@document
class stat_smooth(stat):
    """
    Calculate a smoothed conditional mean

    {usage}

    Parameters
    ----------
    {common_parameters}
    method : str | callable, default="auto"
        The available methods are:
        ```python
        "auto"       # Use loess if (n<1000), glm otherwise
        "lm", "ols"  # Linear Model
        "wls"        # Weighted Linear Model
        "rlm"        # Robust Linear Model
        "glm"        # Generalized linear Model
        "gls"        # Generalized Least Squares
        "lowess"     # Locally Weighted Regression (simple)
        "loess"      # Locally Weighted Regression
        "mavg"       # Moving Average
        "gpr"        # Gaussian Process Regressor
        ```

        If a `callable` is passed, it must have the signature:

        ```python
        def my_smoother(data, xseq, params):
            # * data - has the x and y values for the model
            # * xseq - x values to be predicted
            # * params - stat parameters
            #
            # It must return a new dataframe. Below is the
            # template used internally by Plotnine

            # Input data into the model
            x, y = data["x"], data["y"]

            # Create and fit a model
            model = Model(x, y)
            results = Model.fit()

            # Create output data by getting predictions on
            # the xseq values
            data = pd.DataFrame({
                "x": xseq,
                "y": results.predict(xseq)})

            # Compute confidence intervals, this depends on
            # the model. However, given standard errors and the
            # degrees of freedom we can compute the confidence
            # intervals using the t-distribution.
            #
            # For an alternative, implement confidence intervals by
            # the bootstrap method
            if params["se"]:
                from plotnine.utils.smoothers import tdist_ci
                y = data["y"]            # The predicted value
                df = 123                 # Degrees of freedom
                stderr = results.stderr  # Standard error
                level = params["level"]  # The parameter value
                low, high = tdist_ci(y, df, stderr, level)
                data["se"] = stderr
                data["ymin"] = low
                data["ymax"] = high

            return data
        ```

        For *loess* smoothing you must install the `scikit-misc` package.
        You can install it using with `pip install scikit-misc` or
        `pip install plotnine[all]`.
    formula : formula_like, default=None
        An object that can be used to construct a patsy design matrix.
        This is usually a string. You can only use a formula if `method`
        is one of *lm*, *ols*, *wls*, *glm*, *rlm* or *gls*, and in the
        [formula](https://patsy.readthedocs.io/en/stable/formulas.html)
        you may refer to the `x` and `y` aesthetic variables.
    se : bool, default=True
        If `True`{.py} draw confidence interval around the smooth line.
    n : int, default=80
        Number of points to evaluate the smoother at. Some smoothers
        like *mavg* do not support this.
    fullrange : bool, default: False
        If `True`{.py} the fit will span the full range of the plot.
    level : float, default=0.95
        Level of confidence to use if `se=True`{.py}.
    span : float, default=2/3.
        Controls the amount of smoothing for the *loess* smoother.
        Larger number means more smoothing. It should be in the
        `(0, 1)` range.
    method_args : dict, default={}
        Additional arguments passed on to the modelling method.

    See Also
    --------
    plotnine.geom_smooth : The default `geom` for this `stat`.
    statsmodels.regression.linear_model.OLS
    statsmodels.regression.linear_model.WLS
    statsmodels.robust.robust_linear_model.RLM
    statsmodels.genmod.generalized_linear_model.GLM
    statsmodels.regression.linear_model.GLS
    statsmodels.nonparametric.smoothers_lowess.lowess
    skmisc.loess.loess
    pandas.DataFrame.rolling
    sklearn.gaussian_process.GaussianProcessRegressor

    Notes
    -----
    [](`~plotnine.geoms.geom_smooth`) and [](`~plotnine.stats.stat_smooth`) are
    effectively aliases, they both use the same arguments.
    Use [](`~plotnine.geoms.geom_smooth`) unless
    you want to display the results with a non-standard geom.
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "se"    # Standard error of points in bin
    "ymin"  # Lower confidence limit
    "ymax"  # Upper confidence limit
    ```

    Calculated aesthetics are accessed using the `after_stat` function.
    e.g. `after_stat('se')`{.py}.
    """

    REQUIRED_AES = {"x", "y"}
    DEFAULT_PARAMS = {
        "geom": "smooth",
        "method": "auto",
        "se": True,
        "n": 80,
        "formula": None,
        "fullrange": False,
        "level": 0.95,
        "span": 0.75,
        "method_args": {},
    }
    CREATES = {"se", "ymin", "ymax"}

    def setup_data(self, data):
        """
        Override to modify data before compute_layer is called
        """
        pass

    def setup_params(self, data):
        pass

    def compute_group(self, data, scales):
        pass
