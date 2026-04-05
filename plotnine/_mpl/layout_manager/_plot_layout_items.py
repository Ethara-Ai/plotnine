from __future__ import annotations

from itertools import chain
from typing import TYPE_CHECKING

from matplotlib.text import Text

from plotnine._mpl.patches import StripTextPatch
from plotnine.exceptions import PlotnineError

from ..utils import (
    ArtistGeometry,
    JustifyBoundaries,
    TextJustifier,
    get_subplotspecs,
    rel_position,
)

if TYPE_CHECKING:
    from typing import (
        Any,
        Iterator,
        Literal,
        TypeAlias,
    )

    from matplotlib.axes import Axes
    from matplotlib.axis import Tick
    from matplotlib.lines import Line2D
    from matplotlib.patches import Rectangle
    from matplotlib.transforms import Transform

    from plotnine import ggplot
    from plotnine._mpl.offsetbox import FlexibleAnchoredOffsetbox
    from plotnine._mpl.text import StripText
    from plotnine.iapi import legend_artists
    from plotnine.themes.elements import margin as Margin
    from plotnine.typing import (
        StripPosition,
    )

    from ._plot_side_space import PlotSideSpaces

    AxesLocation: TypeAlias = Literal[
        "all", "first_row", "last_row", "first_col", "last_col"
    ]
    TagLocation: TypeAlias = Literal["margin", "plot", "panel"]
    TagPosition: TypeAlias = (
        Literal[
            "topleft",
            "top",
            "topright",
            "left",
            "right",
            "bottomleft",
            "bottom",
            "bottomright",
        ]
        | tuple[float, float]
    )


class PlotLayoutItems:
    """
    Objects required to compute the layout
    """

    def __init__(self, plot: ggplot):
        def get(name: str) -> Any:
            """
            Return themeable target or None
            """
            if self._is_blank(name):
                return None
            else:
                t = getattr(self.plot.theme.targets, name)
                if isinstance(t, Text) and t.get_text() == "":
                    return None
                return t

        self.plot = plot
        self.geometry = ArtistGeometry(self.plot.figure)

        self.axis_title_x: Text | None = get("axis_title_x")
        self.axis_title_y: Text | None = get("axis_title_y")

        # # The legends references the structure that contains the
        # # AnchoredOffsetboxes (groups of legends)
        self.legends: legend_artists | None = get("legends")
        self.plot_caption: Text | None = get("plot_caption")
        self.plot_footer: Text | None = get("plot_footer")
        self.plot_subtitle: Text | None = get("plot_subtitle")
        self.plot_title: Text | None = get("plot_title")
        self.plot_tag: Text | None = get("plot_tag")
        self.strip_text_x: list[StripText] | None = get("strip_text_x")
        self.strip_text_y: list[StripText] | None = get("strip_text_y")

        self.plot_footer_background: Rectangle | None = get(
            "plot_footer_background"
        )
        self.plot_footer_line: Line2D | None = get("plot_footer_line")

    def _is_blank(self, name: str) -> bool:
        return self.plot.theme.T.is_blank(name)

    def _filter_axes(self, location: AxesLocation = "all") -> list[Axes]:
        """
        Return subset of axes
        """
        pass

    def axis_text_x(self, ax: Axes) -> Iterator[Text]:
        """
        Return all x-axis labels for an axes that will be shown
        """
        pass

    def axis_text_y(self, ax: Axes) -> Iterator[Text]:
        """
        Return all y-axis labels for an axes that will be shown
        """
        pass

    def axis_ticks_x(self, ax: Axes) -> Iterator[Tick]:
        """
        Return all XTicks that will be shown
        """
        pass

    def axis_ticks_y(self, ax: Axes) -> Iterator[Tick]:
        """
        Return all YTicks that will be shown
        """
        pass

    def strip_text_x_extra_height(self, position: StripPosition) -> float:
        """
        Height taken up by the top strips that is outside the panels
        """
        pass

    def strip_text_y_extra_width(self, position: StripPosition) -> float:
        """
        Width taken up by the top strips that is outside the panels
        """
        pass

    def axis_ticks_x_max_height_at(self, location: AxesLocation) -> float:
        """
        Return maximum height[figure space] of x ticks
        """
        pass

    def axis_text_x_max_height(self, ax: Axes) -> float:
        """
        Return maximum height[figure space] of x tick labels
        """
        pass

    def axis_text_x_max_height_at(self, location: AxesLocation) -> float:
        """
        Return maximum height[figure space] of x tick labels
        """
        pass

    def axis_ticks_y_max_width_at(self, location: AxesLocation) -> float:
        """
        Return maximum width[figure space] of y ticks
        """
        pass

    def axis_text_y_max_width(self, ax: Axes) -> float:
        """
        Return maximum width[figure space] of y tick labels
        """
        pass

    def axis_text_y_max_width_at(self, location: AxesLocation) -> float:
        """
        Return maximum width[figure space] of y tick labels
        """
        pass

    def axis_text_y_top_protrusion(self, location: AxesLocation) -> float:
        """
        Return maximum height[figure space] above the axes of y tick labels
        """
        pass

    def axis_text_y_bottom_protrusion(self, location: AxesLocation) -> float:
        """
        Return maximum height[figure space] below the axes of y tick labels
        """
        pass

    def axis_text_x_left_protrusion(self, location: AxesLocation) -> float:
        """
        Return maximum width[figure space] left of the axes of x tick labels
        """
        pass

    def axis_text_x_right_protrusion(self, location: AxesLocation) -> float:
        """
        Return maximum width[figure space] right of the axes of y tick labels
        """
        pass

    def _move_artists(self, spaces: PlotSideSpaces):
        """
        Move the artists to their final positions
        """
        pass

    def _adjust_axis_text_x(self, justify: PlotTextJustifier):
        """
        Adjust x-axis text, justifying vertically as necessary
        """
        pass

    def _adjust_axis_text_y(self, justify: PlotTextJustifier):
        """
        Adjust x-axis text, justifying horizontally as necessary
        """
        pass

    def _strip_text_x_background_equal_heights(self):
        """
        Make the strip_text_x_backgrounds have equal heights

        The smaller heights are expanded to match the largest height
        """
        pass

    def _strip_text_y_background_equal_widths(self):
        """
        Make the strip_text_y_backgrounds have equal widths

        The smaller widths are expanded to match the largest width
        """
        pass

    def _resize_plot_footer_background(self, spaces: PlotSideSpaces):
        """
        Resize the plot footer to the size of the footer
        """
        pass

    def _resize_plot_footer_line(self, spaces: PlotSideSpaces):
        """
        Resize the footer line to be a border above the footer
        """
        pass


def _text_is_visible(text: Text) -> bool:
    """
    Return True if text is visible and is not empty
    """
    pass


class PlotTextJustifier(TextJustifier):
    """
    Justify Text about a plot or it's panels
    """

    def __init__(self, spaces: PlotSideSpaces):
        boundaries = JustifyBoundaries(
            plot_left=spaces.l.plot_left,
            plot_right=spaces.r.plot_right,
            plot_bottom=spaces.b.plot_bottom,
            plot_top=spaces.t.plot_top,
            panel_left=spaces.l.panel_left,
            panel_right=spaces.r.panel_right,
            panel_bottom=spaces.b.panel_bottom,
            panel_top=spaces.t.panel_top,
        )
        super().__init__(spaces.plot.figure, boundaries)


def set_legends_position(legends: legend_artists, spaces: PlotSideSpaces):
    """
    Place legend on the figure and justify is a required
    """
    pass


def set_plot_tag_position(tag: Text, spaces: PlotSideSpaces):
    """
    Set the postion of the plot_tag
    """
    pass


def set_plot_tag_position_in_margin(tag: Text, spaces: PlotSideSpaces):
    """
    Place the tag in an inner margin around the plot

    The panel_margin remains outside the tag. For compositions, the
    tag is placed and within the tag_alignment space.
    """
    pass


def _plot_tag_margin_adjustment(
    margin: Margin, position: str
) -> tuple[float, float]:
    """
    How to adjust the plot_tag to account for the margin
    """
    pass
