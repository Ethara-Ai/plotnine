"""
Routines to adjust subplot params so that subplots are
nicely fit in the figure. In doing so, only axis labels, tick labels, axes
titles and offsetboxes that are anchored to axes are currently considered.

Internally, this module assumes that the margins (left margin, etc.) which are
differences between `Axes.get_tightbbox` and `Axes.bbox` are independent of
Axes position. This may fail if `Axes.adjustable` is `datalim` as well as
such cases as when left or right margin are affected by xlabel.
"""

from __future__ import annotations

from copy import copy
from functools import cached_property
from typing import TYPE_CHECKING

from plotnine.exceptions import PlotnineError
from plotnine.facets import facet_grid, facet_null, facet_wrap

from ._plot_layout_items import PlotLayoutItems
from ._side_space import GridSpecParams, _side_space

if TYPE_CHECKING:
    from plotnine import ggplot
    from plotnine._mpl.gridspec import p9GridSpec
    from plotnine.iapi import outside_legend


class _plot_side_space(_side_space):
    """
    Base class for the side space around a plot
    """

    def __init__(self, items: PlotLayoutItems):
        self.items = items
        self.gridspec = items.plot._gridspec
        self._calculate()

    @cached_property
    def _legend_size(self) -> tuple[float, float]:
        """
        Return size of legend in figure coordinates

        We need this to accurately justify the legend by proportional
        values e.g. 0.2, instead of just left, right, top,  bottom &
        center.
        """
        pass

    @cached_property
    def legend_width(self) -> float:
        """
        Return width of legend in figure coordinates
        """
        pass

    @cached_property
    def legend_height(self) -> float:
        """
        Return height of legend in figure coordinates
        """
        pass

    @property
    def has_tag(self) -> bool:
        """
        Return True if the space/margin to this side of the panel has a tag

        If it does, then it will be included in the layout
        """
        pass

    @property
    def has_legend(self) -> bool:
        """
        Return True if the space/margin to this side of the panel has a legend

        If it does, then it will be included in the layout
        """
        pass

    @property
    def tag_width(self) -> float:
        """
        The width of the tag including the margins

        The value is zero except if all these are true:
            - The tag is in the margin `theme(plot_tag_position = "margin")`
            - The tag at one one of the the following locations;
              left, right, topleft, topright, bottomleft or bottomright
        """
        pass

    @property
    def tag_height(self) -> float:
        """
        The height of the tag including the margins

        The value is zero except if all these are true:
            - The tag is in the margin `theme(plot_tag_position = "margin")`
            - The tag at one one of the the following locations;
              top, bottom, topleft, topright, bottomleft or bottomright
        """
        pass

    @property
    def axis_title_clearance(self) -> float:
        """
        The distance between the axis title and the panel

         Figure
         ----------------------------
        |         Panel              |
        |         -----------        |
        |        |           |       |
        |        |           |       |
        |  Y<--->|           |       |
        |        |           |       |
        |        |           |       |
        |         -----------        |
        |                            |
         ----------------------------

        We use this value to when aligning axis titles in a
        plot composition.
        """
        pass


class left_space(_plot_side_space):
    """
    Space in the figure for artists on the left of the panel area

    Ordered from the edge of the figure and going inwards
    """

    plot_margin: float = 0
    tag_alignment: float = 0
    """
    Space added to align the tag in this plot with others in a composition

    This value is calculated during the layout process, and it ensures that
    all tags on this side of the plot take up the same amount of space in
    the margin. e.g. from

         ------------------------------------
        | plot_margin | tag | artists        |
        |------------------------------------|
        | plot_margin | A long tag | artists |
         ------------------------------------

    to

         ------------------------------------
        | plot_margin |     tag    | artists |
        |------------------------------------|
        | plot_margin | A long tag | artists |
         ------------------------------------

    And the tag is justified within that space e.g if ha="left" we get

         ------------------------------------
        | plot_margin | tag        | artists |
        |------------------------------------|
        | plot_margin | A long tag | artists |
         ------------------------------------

    So, contrary to the order in which the space items are laid out, the 
    tag_alignment does not necessarily come before the plot_tag.
    """
    plot_tag_margin_left: float = 0
    plot_tag: float = 0
    plot_tag_margin_right: float = 0
    margin_alignment: float = 0
    """
    Space added to align this plot with others in a composition

    This value is calculated during the layout process in a tree structure
    that has convenient access to the sides/edges of the panels in the
    composition.
    """
    legend: float = 0
    legend_box_spacing: float = 0
    axis_title_y_margin_left: float = 0
    axis_title_y: float = 0
    axis_title_y_margin_right: float = 0
    axis_title_alignment: float = 0
    """
    Space added to align the axis title with others in a composition

    This value is calculated during the layout process. The amount is
    the difference between the largest and smallest axis_title_clearance
    among the items in the composition.
    """
    axis_text_y_margin_left: float = 0
    axis_text_y: float = 0
    axis_text_y_margin_right: float = 0
    axis_ticks_y: float = 0

    def _calculate(self):
        pass

    @property
    def offset(self) -> float:
        """
        Distance from left of the figure to the left of the plot gridspec

              ----------------(1, 1)
             |      ----      |
             |  dx |    |     |
             |<--->|    |     |
             |     |    |     |
             |      ----      |
        (0, 0)----------------

        """
        pass

    def x1(self, item: str) -> float:
        """
        Lower x-coordinate in figure space of the item
        """
        pass

    def x2(self, item: str) -> float:
        """
        Higher x-coordinate in figure space of the item
        """
        pass

    @property
    def panel_left_relative(self):
        """
        Left (relative to the gridspec) of the panels in figure dimensions
        """
        pass

    @property
    def panel_left(self):
        """
        Left of the panels in figure space
        """
        pass

    @property
    def plot_left(self):
        """
        Distance up to the left-most artist in figure space
        """
        pass

    @property
    def tag_width(self):
        """
        The width of the tag including the margins
        """
        pass


class right_space(_plot_side_space):
    """
    Space in the figure for artists on the right of the panel area

    Ordered from the edge of the figure and going inwards
    """

    plot_margin: float = 0
    tag_alignment: float = 0
    plot_tag_margin_right: float = 0
    plot_tag: float = 0
    plot_tag_margin_left: float = 0
    margin_alignment: float = 0
    legend: float = 0
    legend_box_spacing: float = 0
    strip_text_y_extra_width: float = 0

    def _calculate(self):
        pass

    @property
    def offset(self):
        """
        Distance from right of the figure to the right of the plot gridspec

              ---------------(1, 1)
             |     ----      |
             |    |    | -dx |
             |    |    |<--->|
             |    |    |     |
             |     ----      |
        (0, 0)---------------

        """
        pass

    def x1(self, item: str) -> float:
        """
        Lower x-coordinate in figure space of the item
        """
        pass

    def x2(self, item: str) -> float:
        """
        Higher x-coordinate in figure space of the item
        """
        pass

    @property
    def panel_right_relative(self):
        """
        Right (relative to the gridspec) of the panels in figure dimensions
        """
        pass

    @property
    def panel_right(self):
        """
        Right of the panels in figure space
        """
        pass

    @property
    def plot_right(self):
        """
        Distance up to the right-most artist in figure space
        """
        pass

    @property
    def tag_width(self):
        """
        The width of the tag including the margins
        """
        pass


class top_space(_plot_side_space):
    """
    Space in the figure for artists above the panel area

    Ordered from the edge of the figure and going inwards
    """

    plot_margin: float = 0
    tag_alignment: float = 0
    plot_tag_margin_top: float = 0
    plot_tag: float = 0
    plot_tag_margin_bottom: float = 0
    margin_alignment: float = 0
    plot_title_margin_top: float = 0
    plot_title: float = 0
    plot_title_margin_bottom: float = 0
    plot_subtitle_margin_top: float = 0
    plot_subtitle: float = 0
    plot_subtitle_margin_bottom: float = 0
    legend: float = 0
    legend_box_spacing: float = 0
    strip_text_x_extra_height: float = 0

    def _calculate(self):
        pass

    @property
    def offset(self) -> float:
        """
        Distance from top of the figure to the top of the plot gridspec

              ----------------(1, 1)
             |       ^        |
             |       |-dy     |
             |       v        |
             |      ----      |
             |     |    |     |
             |     |    |     |
             |     |    |     |
             |      ----      |
             |                |
        (0, 0)----------------
        """
        pass

    def y1(self, item: str) -> float:
        """
        Lower y-coordinate in figure space of the item
        """
        pass

    def y2(self, item: str) -> float:
        """
        Higher y-coordinate in figure space of the item
        """
        pass

    @property
    def panel_top_relative(self):
        """
        Top (relative to the gridspec) of the panels in figure dimensions
        """
        pass

    @property
    def panel_top(self):
        """
        Top of the panels in figure space
        """
        pass

    @property
    def plot_top(self):
        """
        Distance up to the top-most artist in figure space
        """
        pass

    @property
    def tag_height(self):
        """
        The height of the tag including the margins
        """
        pass


class bottom_space(_plot_side_space):
    """
    Space in the figure for artists below the panel area

    Ordered from the edge of the figure and going inwards
    """

    plot_footer_margin_bottom: float = 0
    plot_footer: float = 0
    plot_footer_margin_top: float = 0
    plot_margin: float = 0
    tag_alignment: float = 0
    plot_tag_margin_bottom: float = 0
    plot_tag: float = 0
    plot_tag_margin_top: float = 0
    margin_alignment: float = 0
    plot_caption_margin_bottom: float = 0
    plot_caption: float = 0
    plot_caption_margin_top: float = 0
    legend: float = 0
    legend_box_spacing: float = 0
    axis_title_x_margin_bottom: float = 0
    axis_title_x: float = 0
    axis_title_x_margin_top: float = 0
    axis_title_alignment: float = 0
    """
    Space added to align the axis title with others in a composition

    This value is calculated during the layout process in a tree structure
    that has convenient access to the sides/edges of the panels in the
    composition. It's amount is the difference in height between this axis
    text (and it's margins) and the tallest axis text (and it's margin).
    """
    axis_text_x_margin_bottom: float = 0
    axis_text_x: float = 0
    axis_text_x_margin_top: float = 0
    axis_ticks_x: float = 0

    def _calculate(self):
        pass

    @property
    def offset(self) -> float:
        """
        Distance from bottom of the figure to the bottom of the plot gridspec

              ----------------(1, 1)
             |                |
             |      ----      |
             |     |    |     |
             |     |    |     |
             |     |    |     |
             |      ----      |
             |       ^        |
             |       |dy      |
             |       v        |
        (0, 0)----------------
        """
        pass

    def y1(self, item: str) -> float:
        """
        Lower y-coordinate in figure space of the item
        """
        pass

    def y2(self, item: str) -> float:
        """
        Higher y-coordinate in figure space of the item
        """
        pass

    @property
    def panel_bottom_relative(self):
        """
        Bottom (relative to the gridspec) of the panels in figure dimensions
        """
        pass

    @property
    def panel_bottom(self):
        """
        Bottom of the panels in figure space
        """
        pass

    @property
    def plot_bottom(self):
        """
        Distance up to the bottom-most artist in figure space
        """
        pass

    @property
    def footer_height(self):
        """
        The height of the footer including the margins
        """
        pass

    @property
    def tag_height(self):
        """
        The height of the tag including the margins
        """
        pass


class PlotSideSpaces:
    """
    Compute the all the spaces required in the layout

    These are:

    1. The space of each artist between the panel and the edge of the
       figure.
    2. The space in-between the panels

    From these values, we put together the grid-spec parameters required
    by matplotblib to position the axes. We also use the values to adjust
    the coordinates of all the artists that occupy these spaces, placing
    them in their final positions.
    """

    W: float
    """Figure Width [inches]"""

    H: float
    """Figure Height [inches]"""

    w: float
    """Axes width w.r.t figure in [0, 1]"""

    h: float
    """Axes height w.r.t figure in [0, 1]"""

    sh: float
    """horizontal spacing btn panels w.r.t figure"""

    sw: float
    """vertical spacing btn panels w.r.t figure"""

    def __init__(self, plot: ggplot):
        self.plot = plot
        self.gridspec = plot._gridspec
        self.sub_gridspec = plot._sub_gridspec
        self.items = PlotLayoutItems(plot)

        self.l = left_space(self.items)
        """All subspaces to the left of the panels"""

        self.r = right_space(self.items)
        """All subspaces to the right of the panels"""

        self.t = top_space(self.items)
        """All subspaces above the top of the panels"""

        self.b = bottom_space(self.items)
        """All subspaces below the bottom of the panels"""

        self.W, self.H = plot.theme.getp("figure_size")

    def arrange(self):
        """
        Resize plot and place artists in final positions around the panels
        """
        pass

    def resize_gridspec(self):
        """
        Apply the space calculations to the sub_gridspec

        After calling this method, the sub_gridspec will be appropriately
        sized to accomodate the artists around the panels.
        """
        pass

    def calculate_gridspec_params(self) -> GridSpecParams:
        """
        Grid spacing between panels w.r.t figure
        """
        pass

    @property
    def plot_width(self) -> float:
        """
        Width [figure dimensions] of the whole plot
        """
        pass

    @property
    def plot_height(self) -> float:
        """
        Height [figure dimensions] of the whole plot
        """
        pass

    @property
    def panel_width(self) -> float:
        """
        Width [figure dimensions] of panels
        """
        pass

    @property
    def panel_height(self) -> float:
        """
        Height [figure dimensions] of panels
        """
        pass

    @property
    def horizontal_space(self) -> float:
        """
        Horizontal non-panel space [figure dimensions]
        """
        pass

    @property
    def vertical_space(self) -> float:
        """
        Vertical non-panel space [figure dimensions]
        """
        pass

    def increase_horizontal_plot_margin(self, dw: float):
        """
        Increase the plot_margin to the right & left of the panels
        """
        pass

    def increase_vertical_plot_margin(self, dh: float):
        """
        Increase the plot_margin to the above & below of the panels
        """
        pass

    @property
    def plot_area_coordinates(
        self,
    ) -> tuple[tuple[float, float], tuple[float, float]]:
        """
        Lower-left and upper-right coordinates of the plot area

        This is the area surrounded by the plot_margin.
        """
        pass

    @property
    def panel_area_coordinates(
        self,
    ) -> tuple[tuple[float, float], tuple[float, float]]:
        """
        Lower-left and upper-right coordinates of the panel area

        This is the area in which the panels are drawn.
        """
        pass

    def _calculate_panel_spacing(self) -> GridSpecParams:
        """
        Spacing between the panels (wspace & hspace)

        Both spaces are calculated from a fraction of the width.
        This ensures that the same fraction gives equals space
        in both directions.
        """
        pass

    def _calculate_panel_spacing_facet_grid(self) -> tuple[float, float]:
        """
        Calculate spacing parts for facet_grid
        """
        pass

    def _calculate_panel_spacing_facet_wrap(self) -> tuple[float, float]:
        """
        Calculate spacing parts for facet_wrap
        """
        pass

    def _calculate_panel_spacing_facet_null(self) -> tuple[float, float]:
        """
        Calculate spacing parts for facet_null
        """
        pass

    def _reduce_height(self, gsparams: GridSpecParams, ratio: float):
        """
        Reduce the height of axes to get the aspect ratio
        """
        pass

    def _reduce_width(self, gsparams: GridSpecParams, ratio: float):
        """
        Reduce the width of axes to get the aspect ratio
        """
        pass

    @property
    def aspect_ratio(self) -> float:
        """
        Default aspect ratio of the panels
        """
        pass

    @cached_property
    def gs(self) -> p9GridSpec:
        """
        The gridspec
        """
        pass

    def to_figure_space(
        self,
        position: tuple[float, float],
    ) -> tuple[float, float]:
        """
        Convert position from gridspec space to figure space
        """
        pass
