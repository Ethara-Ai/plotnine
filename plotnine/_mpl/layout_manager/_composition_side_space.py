from __future__ import annotations

from typing import TYPE_CHECKING

from plotnine._mpl.layout_manager._layout_tree import LayoutTree
from plotnine._mpl.layout_manager._plot_side_space import PlotSideSpaces

from ._composition_layout_items import CompositionLayoutItems
from ._side_space import GridSpecParams, _side_space

if TYPE_CHECKING:
    from plotnine.composition._compose import Compose


class _composition_side_space(_side_space):
    """
    Base class for the side space around a composition
    """

    def __init__(self, items: CompositionLayoutItems):
        self.items = items
        self.gridspec = items.cmp._gridspec
        self._calculate()


class composition_left_space(_composition_side_space):
    plot_margin: float = 0

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
    def items_left_relative(self):
        """
        Left (relative to the gridspec) of the cmp items in figure dimensions
        """
        pass

    @property
    def items_left(self):
        """
        Left of the composition items in figure space
        """
        pass


class composition_right_space(_composition_side_space):
    """
    Space for annotations to the right of the actual composition

    Ordered from the edge of the figure and going inwards
    """

    plot_margin: float = 0

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
    def items_right_relative(self):
        """
        Right (relative to the gridspec) of the panels in figure dimensions
        """
        pass

    @property
    def items_right(self):
        """
        Right of the panels in figure space
        """
        pass


class composition_top_space(_composition_side_space):
    """
    Space for annotations above the actual composition

    Ordered from the edge of the figure and going inwards
    """

    plot_margin: float = 0
    plot_title_margin_top: float = 0
    plot_title: float = 0
    plot_title_margin_bottom: float = 0
    plot_subtitle_margin_top: float = 0
    plot_subtitle: float = 0
    plot_subtitle_margin_bottom: float = 0

    def _calculate(self):
        pass

    @property
    def offset(self) -> float:
        """
        Distance from top of the figure to the top of the composition gridspec

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
    def items_top_relative(self):
        """
        Top (relative to the gridspec) of the panels in figure dimensions
        """
        pass

    @property
    def items_top(self):
        """
        Top of the composition items in figure space
        """
        pass


class composition_bottom_space(_composition_side_space):
    """
    Space in the figure for artists below the panel area

    Ordered from the edge of the figure and going inwards
    """

    plot_footer_margin_bottom: float = 0
    plot_footer: float = 0
    plot_footer_margin_top: float = 0
    plot_margin: float = 0
    plot_caption_margin_bottom: float = 0
    plot_caption: float = 0
    plot_caption_margin_top: float = 0

    def _calculate(self):
        pass

    @property
    def offset(self) -> float:
        """
        Distance from bottom of the figure to the composition gridspec

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
    def footer_height(self):
        """
        The height of the footer including the margins
        """
        pass

    @property
    def items_bottom_relative(self):
        """
        Bottom (relative to the gridspec) of the panels in figure dimensions
        """
        pass

    @property
    def items_bottom(self):
        """
        Bottom of the panels in figure space
        """
        pass


class CompositionSideSpaces:
    """
    Compute the spaces required to layout the composition

    This is meant for the top-most composition
    """

    def __init__(self, cmp: Compose):
        self.cmp = cmp
        self.gridspec = cmp._gridspec
        self.sub_gridspec = cmp._sub_gridspec
        self.items = CompositionLayoutItems(cmp)

        self.l = composition_left_space(self.items)
        """All subspaces to the left of the panels"""

        self.r = composition_right_space(self.items)
        """All subspaces to the right of the panels"""

        self.t = composition_top_space(self.items)
        """All subspaces above the top of the panels"""

        self.b = composition_bottom_space(self.items)
        """All subspaces below the bottom of the panels"""

        self._create_plot_sidespaces()
        self.tree = LayoutTree.create(cmp)

    def arrange(self):
        """
        Resize composition and place artists in final positions
        """
        pass

    def _arrange_plots(self):
        """
        Arrange all the plots in the composition
        """
        pass

    def _create_plot_sidespaces(self):
        """
        Create sidespaces for all the plots in the composition
        """
        pass

    def resize_gridspec(self):
        """
        Apply the space calculations to the sub_gridspec

        After calling this method, the sub_gridspec will be appropriately
        sized to accomodate the content of the annotations.
        """
        pass

    def calculate_gridspec_params(self) -> GridSpecParams:
        """
        Grid spacing between compositions w.r.t figure
        """
        pass

    @property
    def plot_width(self) -> float:
        """
        Width [figure dimensions] of the whole plot composition
        """
        pass

    @property
    def plot_height(self) -> float:
        """
        Height [figure dimensions] of the whole plot composition
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

    @property
    def plot_left(self) -> float:
        """
        Distance up to left most artist in the composition
        """
        pass

    @property
    def plot_right(self) -> float:
        """
        Distance up to right most artist in the composition
        """
        pass

    @property
    def plot_bottom(self) -> float:
        """
        Distance up to bottom most artist in the composition
        """
        pass

    @property
    def plot_top(self) -> float:
        """
        Distance upto top most artist in the composition
        """
        pass

    @property
    def panel_left(self) -> float:
        """
        Distance up to left most artist in the composition
        """
        pass

    @property
    def panel_right(self) -> float:
        """
        Distance up to right most artist in the composition
        """
        pass

    @property
    def panel_bottom(self) -> float:
        """
        Distance up to bottom most artist in the composition
        """
        pass

    @property
    def panel_top(self) -> float:
        """
        Distance upto top most artist in the composition
        """
        pass
