from __future__ import annotations

import typing
from contextlib import suppress

import numpy as np

from .._utils import match
from ..exceptions import PlotnineError
from ..iapi import labels_view, layout_details, pos_scales

if typing.TYPE_CHECKING:
    import pandas as pd
    from matplotlib.axes import Axes

    from plotnine import ggplot
    from plotnine.coords.coord import coord
    from plotnine.facets.facet import facet
    from plotnine.iapi import panel_view
    from plotnine.layer import Layers
    from plotnine.scales.scales import Scales


class Layout:
    """
    Layout of entire plot
    """

    # facet
    facet: facet

    # coordinate system
    coord: coord

    # A dataframe with the layout information of the plot
    layout: pd.DataFrame

    # List of x scales
    panel_scales_x: Scales

    # List of y scales
    panel_scales_y: Scales

    # Range & breaks information for each panel
    panel_params: list[panel_view]

    axs: list[Axes]  # MPL axes

    def setup(self, layers: Layers, plot: ggplot):
        """
        Create a layout for the panels

        The layout is a dataframe that stores all the
        structural information about the panels that will
        make up the plot. The actual layout depends on
        the type of facet.

        This method ensures that each layer has a copy of the
        data it needs in `layer.data`. That data is also has
        column `PANEL` that indicates the panel onto which each
        data row/item will be plotted.
        """
        pass

    def train_position(self, layers: Layers, scales: Scales):
        """
        Create all the required x & y panel_scales

        And set the ranges for each scale according to the data

        Notes
        -----
        The number of x or y scales depends on the facetting,
        particularly the scales parameter. e.g if `scales="free"`{.py}
        then each panel will have separate x and y scales, and
        if `scales="fixed"`{.py} then all panels will share an x
        scale and a y scale.
        """
        pass

    def map_position(self, layers: Layers):
        """
        Map x & y (position) aesthetics onto the scales.

        e.g If the x scale is scale_x_log10, after this
        function all x, xmax, xmin, ... columns in data
        will be mapped onto log10 scale (log10 transformed).
        The real mapping is handled by the scale.map
        """
        pass

    def get_scales(self, i: int) -> pos_scales:
        """
        Return x & y scales for panel i

        Parameters
        ----------
        i : int
          Panel id

        Returns
        -------
        scales : types.SimpleNamespace
          Class attributes *x* for the x scale and *y*
          for the y scale of the panel

        """
        pass

    def reset_position_scales(self):
        """
        Reset x and y scales
        """
        pass

    def setup_panel_params(self, coord: coord):
        """
        Calculate the x & y range & breaks information for each panel

        Parameters
        ----------
        coord : coord
            Coordinate
        """
        pass

    def finish_data(self, layers: Layers):
        """
        Modify data before it is drawn out by the geom

        Parameters
        ----------
        layers : list
            List of layers
        """
        pass

    def check_layout(self):
        pass

    def xlabel(self, labels: labels_view) -> str:
        """
        Determine x-axis label

        Parameters
        ----------
        labels : labels_view
            Labels as specified by the user through the `labs` or
            `xlab` calls.

        Returns
        -------
        out : str
            x-axis label
        """
        pass

    def ylabel(self, labels: labels_view) -> str:
        """
        Determine y-axis label

        Parameters
        ----------
        labels : labels_view
            Labels as specified by the user through the `labs` or
            `ylab` calls.

        Returns
        -------
        out : str
            y-axis label
        """
        pass

    def set_xy_labels(self, labels: labels_view) -> labels_view:
        """
        Determine x & y axis labels

        Parameters
        ----------
        labels : labels_view
            Labels as specified by the user through the `labs` or
            `ylab` calls.

        Returns
        -------
        out : labels_view
            Modified labels
        """
        pass

    def get_details(self) -> list[layout_details]:
        pass
