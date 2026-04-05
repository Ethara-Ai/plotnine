from __future__ import annotations

import typing
from abc import ABC
from contextlib import suppress
from copy import deepcopy
from itertools import chain, repeat

import numpy as np

from .._utils import (
    data_mapping_as_kwargs,
    remove_missing,
)
from .._utils.registry import Register
from ..exceptions import PlotnineError
from ..layer import layer
from ..mapping.aes import rename_aesthetics
from ..mapping.evaluation import evaluate

if typing.TYPE_CHECKING:
    from typing import Any

    import pandas as pd
    from matplotlib.axes import Axes
    from matplotlib.offsetbox import DrawingArea

    from plotnine import aes, ggplot
    from plotnine.coords.coord import coord
    from plotnine.facets.layout import Layout
    from plotnine.iapi import panel_view
    from plotnine.mapping import Environment
    from plotnine.typing import DataLike


_BASE_PARAMS: dict[str, Any] = {
    "stat": "identity",
    "position": "identity",
    "na_rm": False,
}


class geom(ABC, metaclass=Register):
    """Base class of all Geoms"""

    DEFAULT_AES: dict[str, Any] = {}
    """Default aesthetics for the geom"""

    REQUIRED_AES: set[str] = set()
    """Required aesthetics for the geom"""

    NON_MISSING_AES: set[str] = set()
    """Required aesthetics for the geom"""

    DEFAULT_PARAMS: dict[str, Any] = {}
    """Required parameters for the geom"""

    data: DataLike
    """Geom/layer specific dataframe"""

    mapping: aes
    """Mappings i.e. `aes(x="col1", fill="col2")`{.py}"""

    aes_params: dict[str, Any] = {}  # setting of aesthetic
    params: dict[str, Any]  # parameter settings

    # Plot namespace, it gets its value when the plot is being
    # built.
    environment: Environment

    # The geom responsible for the legend if draw_legend is
    # not implemented
    legend_geom: str = "point"

    # Documentation for the aesthetics. It is added under the
    # documentation for mapping parameter. Use {aesthetics}
    # placeholder to insert a table for all the aesthetics and
    # their default values.
    _aesthetics_doc: str = "{aesthetics_table}"

    def __init__(
        self,
        mapping: aes | None = None,
        data: DataLike | None = None,
        **kwargs: Any,
    ):
        kwargs = rename_aesthetics(kwargs)
        kwargs = data_mapping_as_kwargs((data, mapping), kwargs)
        self._raw_kwargs = kwargs  # Will be used to create stat & layer

        # separate aesthetics and parameters
        possible_params = _BASE_PARAMS | self.DEFAULT_PARAMS
        self.aes_params = {
            ae: kwargs[ae] for ae in self.aesthetics() & set(kwargs)
        }
        self.params = possible_params | {
            k: v for k, v in kwargs.items() if k in possible_params
        }
        self.mapping = kwargs["mapping"]
        self.data = kwargs["data"]

    @classmethod
    def aesthetics(cls: type[geom]) -> set[str]:
        """
        Return all the aesthetics for this geom

        geoms should not override this method.
        """
        pass

    def __deepcopy__(self, memo: dict[Any, Any]) -> geom:
        """
        Deep copy without copying the self.data dataframe

        geoms should not override this method.
        """
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        old = self.__dict__
        new = result.__dict__

        # don't make a deepcopy of data, or environment
        shallow = {"data", "_raw_kwargs", "environment"}
        for key, item in old.items():
            if key in shallow:
                new[key] = item  # pyright: ignore[reportIndexIssue]
                memo[id(new[key])] = new[key]
            else:
                new[key] = deepcopy(item, memo)  # pyright: ignore[reportIndexIssue]

        return result

    def setup_params(self, data: pd.DataFrame):
        """
        Override this method to verify and/or adjust parameters

        Parameters
        ----------
        data :
            Data
        """

    def setup_aes_params(self, data: pd.DataFrame):
        """
        Override this method to verify and/or adjust aesthetic parameters

        Parameters
        ----------
        data :
            Data
        """

    def setup_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Modify the data before drawing takes place

        This function is called *before* position adjustments are done.
        It is used by geoms to create the final aesthetics used for
        drawing. The base class method does nothing, geoms can override
        this method for two reasons:

        1. The `stat` does not create all the aesthetics (usually
           position aesthetics) required for drawing the `geom`,
           but those aesthetics can be computed from the available
           data. For example [](`~plotnine.geoms.geom_boxplot`)
           and [](`~plotnine.geoms.geom_violin`).

        2. The `geom` inherits from another `geom` (superclass) which
           does the drawing and the superclass requires certain aesthetics
           to be present in the data. For example
           [](`~plotnine.geoms.geom_tile`) and
           [](`~plotnine.geoms.geom_area`).

        Parameters
        ----------
        data :
            Data used for drawing the geom.

        Returns
        -------
        :
            Data used for drawing the geom.
        """
        pass

    def use_defaults(
        self, data: pd.DataFrame, aes_modifiers: dict[str, Any]
    ) -> pd.DataFrame:
        """
        Combine data with defaults and set aesthetics from parameters

        geoms should not override this method.

        Parameters
        ----------
        data :
            Data used for drawing the geom.
        aes_modifiers :
            Aesthetics to evaluate

        Returns
        -------
        :
            Data used for drawing the geom.
        """
        pass

    def draw_layer(self, data: pd.DataFrame, layout: Layout, coord: coord):
        """
        Draw layer across all panels

        geoms should not override this method.

        Parameters
        ----------
        data :
            DataFrame specific for this layer
        layout :
            Layout object created when the plot is getting
            built
        coord :
            Type of coordinate axes
        params :
            Combined *geom* and *stat* parameters. Also
            includes the stacking order of the layer in
            the plot (*zorder*)
        """
        pass

    def draw_panel(
        self,
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
    ):
        """
        Plot all groups

        For efficiency, geoms that do not need to partition
        different groups before plotting should override this
        method and avoid the groupby.

        Parameters
        ----------
        data :
            Data to be plotted by this geom. This is the
            dataframe created in the plot_build pipeline.
        panel_params :
            The scale information as may be required by the
            axes. At this point, that information is about
            ranges, ticks and labels. Attributes are of interest
            to the geom are:

            ```python
            "panel_params.x.range"  # tuple
            "panel_params.y.range"  # tuple
            ```
        coord :
            Coordinate (e.g. coord_cartesian) system of the geom.
        ax :
            Axes on which to plot.
        params :
            Combined parameters for the geom and stat. Also
            includes the `zorder`.
        """
        pass

    @staticmethod
    def draw_group(
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
    ):
        """
        Plot data belonging to a group.

        Parameters
        ----------
        data :
            Data to be plotted by this geom. This is the
            dataframe created in the plot_build pipeline.
        panel_params :
            The scale information as may be required by the
            axes. At this point, that information is about
            ranges, ticks and labels. Keys of interest to
            the geom are:

            ```python
            "x_range"  # tuple
            "y_range"  # tuple
            ```
        coord : coord
            Coordinate (e.g. coord_cartesian) system of the geom.
        ax : axes
            Axes on which to plot.
        params : dict
            Combined parameters for the geom and stat. Also
            includes the `zorder`.
        """
        pass

    @staticmethod
    def draw_unit(
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
    ):
        """
        Plot data belonging to a unit.

        A matplotlib plot function may require that an aethestic
        have a single unique value. e.g. `linestyle="dashed"`{.py}
        and not `linestyle=["dashed", "dotted", ...]`{.py}.
        A single call to such a function can only plot lines with
        the same linestyle. However, if the plot we want has more
        than one line with different linestyles, we need to group
        the lines with the same linestyle and plot them as one
        unit. In this case, draw_group calls this function to do
        the plotting. For an example see
        [](`~plotnine.geoms.geom_point`).

        Parameters
        ----------
        data :
            Data to be plotted by this geom. This is the
            dataframe created in the plot_build pipeline.
        panel_params :
            The scale information as may be required by the
            axes. At this point, that information is about
            ranges, ticks and labels. Keys of interest to
            the geom are:

            ```python
            "x_range"  # tuple
            "y_range"  # tuple
            ```

            In rare cases a geom may need access to the x or y scales.
            Those are available at:

            ```python
            "scales"   # SimpleNamespace
            ```
        coord :
            Coordinate (e.g. coord_cartesian) system of the
            geom.
        ax :
            Axes on which to plot.
        params :
            Combined parameters for the geom and stat. Also
            includes the `zorder`.
        """
        pass

    def __radd__(self, other: ggplot) -> ggplot:
        """
        Add layer representing geom object on the right

        Parameters
        ----------
        plot :
            ggplot object

        Returns
        -------
        :
            ggplot object with added layer.
        """
        other += layer(geom=self)
        return other

    def handle_na(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Remove rows with NaN values

        geoms that infer extra information from missing values
        should override this method. For example
        [](`~plotnine.geoms.geom_path`).

        Parameters
        ----------
        data :
            Data

        Returns
        -------
        :
            Data without the NaNs.

        Notes
        -----
        Shows a warning if the any rows are removed and the
        `na_rm` parameter is False. It only takes into account
        the columns of the required aesthetics.
        """
        pass

    @staticmethod
    def draw_legend(
        data: pd.Series[Any], da: DrawingArea, lyr: layer
    ) -> DrawingArea:
        """
        Draw a rectangle in the box

        Parameters
        ----------
        data :
            A row of the data plotted to this layer
        da :
            Canvas on which to draw
        lyr :
            Layer that the geom belongs to.

        Returns
        -------
        :
            The DrawingArea after a layer has been drawn onto it.
        """
        pass

    @staticmethod
    def legend_key_size(
        data: pd.Series[Any], min_size: tuple[int, int], lyr: layer
    ) -> tuple[int, int]:
        """
        Calculate the size of key that would fit the layer contents

        Parameters
        ----------
        data :
            A row of the data plotted to this layer
        min_size :
            Initial size which should be expanded to fit the contents.
        lyr :
            Layer
        """
        pass
