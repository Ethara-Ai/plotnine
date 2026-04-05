from __future__ import annotations

import itertools
import types
import typing
from copy import copy, deepcopy

import numpy as np
import pandas as pd
import pandas.api.types as pdtypes

from .._utils import cross_join, match
from ..exceptions import PlotnineError
from ..scales.scales import Scales
from .strips import Strips

if typing.TYPE_CHECKING:
    from typing import Any, Literal, Optional, Sequence

    import numpy.typing as npt
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure

    from plotnine import ggplot, theme
    from plotnine._mpl.gridspec import p9GridSpec
    from plotnine.coords.coord import coord
    from plotnine.facets.labelling import CanBeStripLabellingFunc
    from plotnine.facets.layout import Layout
    from plotnine.iapi import layout_details, panel_view
    from plotnine.layer import Layers
    from plotnine.mapping import Environment
    from plotnine.scales.scale import scale


class facet:
    """
    Base class for all facets

    Parameters
    ----------
    scales :
        Whether `x` or `y` scales should be allowed (free)
        to vary according to the data on each of the panel.
    shrink :
        Whether to shrink the scales to the output of the
        statistics instead of the raw data. Default is `True`.
    labeller :
        How to label the facets. A string value if it should be
        one of `["label_value", "label_both", "label_context"]`{.py}.
    as_table :
        If `True`, the facets are laid out like a table with
        the highest values at the bottom-right. If `False`
        the facets are laid out like a plot with the highest
        value a the top-right
    drop :
        If `True`, all factor levels not used in the data
        will automatically be dropped. If `False`, all
        factor levels will be shown, regardless of whether
        or not they appear in the data.
    dir :
        Direction in which to layout the panels. `h` for
        horizontal and `v` for vertical.
    """

    # number of columns
    ncol: int

    # number of rows
    nrow: int

    as_table = True
    drop = True
    shrink = True

    # Which axis scales are free
    free: dict[Literal["x", "y"], bool]

    # A dict of parameters created depending on the data
    # (Intended for extensions)
    params: dict[str, Any]

    # Theme object, automatically updated before drawing the plot
    theme: theme

    # Figure object on which the facet panels are created
    figure: Figure

    # coord object, automatically updated before drawing the plot
    coordinates: coord

    # layout object, automatically updated before drawing the plot
    layout: Layout

    # Axes
    axs: list[Axes]

    # ggplot object that the facet belongs to
    plot: ggplot

    # Facet strips
    strips: Strips

    # The plot environment
    environment: Environment

    def __init__(
        self,
        scales: Literal["fixed", "free", "free_x", "free_y"] = "fixed",
        shrink: bool = True,
        labeller: CanBeStripLabellingFunc = "label_value",
        as_table: bool = True,
        drop: bool = True,
        dir: Literal["h", "v"] = "h",
    ):
        from .labelling import as_labeller

        self.shrink = shrink
        self.labeller = as_labeller(labeller)
        self.as_table = as_table
        self.drop = drop
        self.dir = dir
        allowed_scales = ["fixed", "free", "free_x", "free_y"]
        if scales not in allowed_scales:
            raise ValueError(
                "Argument `scales` must be one of {allowed_scales}."
            )
        self.free = {
            "x": scales in ("free_x", "free"),
            "y": scales in ("free_y", "free"),
        }

    def __radd__(self, other: ggplot) -> ggplot:
        """
        Add facet to ggplot object
        """
        other.facet = copy(self)
        other.facet.environment = other.environment
        return other

    def setup(self, plot: ggplot):
        pass

    def setup_data(self, data: list[pd.DataFrame]) -> list[pd.DataFrame]:
        """
        Allow the facet to manipulate the data

        Parameters
        ----------
        data :
            Data for each of the layers

        Returns
        -------
        :
            Data for each of the layers

        Notes
        -----
        This method will be called after [](`~plotnine.facet.setup_params`),
        therefore the `params` property will be set.
        """
        pass

    def setup_params(self, data: list[pd.DataFrame]):
        """
        Create facet parameters

        Parameters
        ----------
        data :
            Plot data and data for the layers
        """
        pass

    def init_scales(
        self,
        layout: pd.DataFrame,
        x_scale: Optional[scale] = None,
        y_scale: Optional[scale] = None,
    ) -> types.SimpleNamespace:
        pass

    def map(self, data: pd.DataFrame, layout: pd.DataFrame) -> pd.DataFrame:
        """
        Assign a data points to panels

        Parameters
        ----------
        data :
            Data for a layer
        layout :
            As returned by self.compute_layout

        Returns
        -------
        :
            Data with all points mapped to the panels
            on which they will be plotted.
        """
        pass

    def compute_layout(
        self,
        data: list[pd.DataFrame],
    ) -> pd.DataFrame:
        """
        Compute layout

        Parameters
        ----------
        data :
            Dataframe for a each layer
        """
        pass

    def finish_data(self, data: pd.DataFrame, layout: Layout) -> pd.DataFrame:
        """
        Modify data before it is drawn out by the geom

        The default is to return the data without modification.
        Subclasses should override this method as the require.

        Parameters
        ----------
        data :
            A single layer's data.
        layout :
            Layout

        Returns
        -------
        :
            Modified layer data
        """
        pass

    def train_position_scales(self, layout: Layout, layers: Layers) -> facet:
        """
        Compute ranges for the x and y scales
        """
        pass

    def make_strips(self, layout_info: layout_details, ax: Axes) -> Strips:
        """
        Create strips for the facet

        Parameters
        ----------
        layout_info :
            Layout information. Row from the layout table

        ax :
            Axes to label
        """
        pass

    def set_limits_breaks_and_labels(self, panel_params: panel_view, ax: Axes):
        """
        Add limits, breaks and labels to the axes

        Parameters
        ----------
        panel_params :
            range information for the axes
        ax :
            Axes
        """
        pass

    def __deepcopy__(self, memo: dict[Any, Any]) -> facet:
        """
        Deep copy without copying the dataframe and environment
        """
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        old = self.__dict__
        new = result.__dict__

        # don't make a deepcopy of the figure & the axes
        shallow = {"axs", "first_ax", "last_ax"}
        for key, item in old.items():
            if key in shallow:
                new[key] = item
                memo[id(new[key])] = new[key]
            else:
                new[key] = deepcopy(item, memo)

        return result

    def _make_gridspec(self):
        """
        Create gridspec for the panels
        """
        pass

    def _make_axes(self) -> tuple[p9GridSpec, list[Axes]]:
        """
        Create and return subplot axes
        """
        pass

    def _aspect_ratio(self) -> Optional[float]:
        """
        Return the aspect_ratio
        """
        pass


def combine_vars(
    data: list[pd.DataFrame],
    environment: Environment,
    vars: Sequence[str],
    drop: bool = True,
) -> pd.DataFrame:
    """
    Generate all combinations of data needed for facetting

    The first data frame in the list should be the default data
    for the plot. Other data frames in the list are ones that are
    added to the layers.
    """
    pass


def unique_combs(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate all possible combinations of the values in the columns
    """
    pass


def layout_null() -> pd.DataFrame:
    """
    Layout Null
    """
    pass


def add_missing_facets(
    data: pd.DataFrame,
    layout: pd.DataFrame,
    vars: Sequence[str],
    facet_vals: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Add missing facets
    """
    pass


def eval_facet_vars(
    data: pd.DataFrame, vars: Sequence[str], env: Environment
) -> pd.DataFrame:
    """
    Evaluate facet variables

    Parameters
    ----------
    data :
        Factet dataframe
    vars :
        Facet variables
    env :
        Plot environment

    Returns
    -------
    :
        Facet values that correspond to the specified
        variables.
    """
    pass
