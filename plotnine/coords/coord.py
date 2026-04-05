from __future__ import annotations

import typing
from copy import copy

import numpy as np

from ..iapi import panel_ranges

if typing.TYPE_CHECKING:
    from typing import Any

    import numpy.typing as npt
    import pandas as pd

    from plotnine import ggplot
    from plotnine.iapi import labels_view, panel_view
    from plotnine.scales.scale import scale
    from plotnine.typing import (
        FloatArray,
        FloatArrayLike,
        FloatSeries,
    )


class coord:
    """
    Base class for all coordinate systems
    """

    # If the coordinate system is linear
    is_linear = False

    # Additional parameters created acc. to the data,
    # if the coordinate system needs them
    params: dict[str, Any]

    def __radd__(self, other: ggplot) -> ggplot:
        """
        Add coordinates to ggplot object
        """
        other.coordinates = copy(self)
        return other

    def setup_data(self, data: list[pd.DataFrame]) -> list[pd.DataFrame]:
        """
        Allow the coordinate system to manipulate the layer data

        Parameters
        ----------
        data :
            Data for all Layer

        Returns
        -------
        :
            Modified layer data
        """
        pass

    def setup_params(self, data: list[pd.DataFrame]):
        """
        Create additional parameters

        A coordinate system may need to create parameters
        depending on the *original* data that the layers get.

        Parameters
        ----------
        data :
            Data for each layer before it is manipulated in
            any way.
        """
        pass

    def setup_layout(self, layout: pd.DataFrame) -> pd.DataFrame:
        """
        Allow the coordinate system alter the layout dataframe

        Parameters
        ----------
        layout :
            Dataframe in which data is assigned to panels and scales

        Returns
        -------
        :
            layout dataframe altered to according to the requirements
            of the coordinate system.

        Notes
        -----
        The input dataframe may be changed.
        """
        pass

    def aspect(self, panel_params: panel_view) -> float | None:
        """
        Return desired aspect ratio for the plot

        If not overridden by the subclass, this method
        returns `None`, which means that the coordinate
        system does not influence the aspect ratio.
        """
        pass

    def labels(self, cur_labels: labels_view) -> labels_view:
        """
        Modify labels

        Parameters
        ----------
        cur_labels :
            Current labels. The coord can modify them as necessary.

        Returns
        -------
        :
            Modified labels. Same object as the input.
        """
        pass

    def transform(
        self, data: pd.DataFrame, panel_params: panel_view, munch: bool = False
    ) -> pd.DataFrame:
        """
        Transform data before it is plotted

        This is used to "transform the coordinate axes".
        Subclasses should override this method
        """
        pass

    def setup_panel_params(self, scale_x: scale, scale_y: scale) -> panel_view:
        """
        Compute the range and break information for the panel
        """
        pass

    def range(self, panel_params: panel_view) -> panel_ranges:
        """
        Return the range along the dimensions of the coordinate system
        """
        pass

    def backtransform_range(self, panel_params: panel_view) -> panel_ranges:
        """
        Backtransform the panel range in panel_params to data coordinates

        Coordinate systems that do any transformations should override
        this method. e.g. coord_trans has to override this method.
        """
        pass

    def distance(
        self,
        x: FloatSeries,
        y: FloatSeries,
        panel_params: panel_view,
    ) -> npt.NDArray[Any]:
        pass

    def munch(
        self, data: pd.DataFrame, panel_params: panel_view
    ) -> pd.DataFrame:
        pass


def dist_euclidean(x: FloatArrayLike, y: FloatArrayLike) -> FloatArray:
    """
    Calculate euclidean distance
    """
    pass


def interp(start: int, end: int, n: int) -> FloatArray:
    """
    Interpolate
    """
    pass


def munch_data(data: pd.DataFrame, dist: FloatArray) -> pd.DataFrame:
    """
    Breakup path into small segments
    """
    pass
