from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, cast

from matplotlib.transforms import Affine2D, Bbox

from plotnine._utils import ha_as_float, va_as_float

from .transforms import ZEROS_BBOX

if TYPE_CHECKING:
    from typing import Literal, Sequence

    from matplotlib.artist import Artist
    from matplotlib.axes import Axes
    from matplotlib.backend_bases import RendererBase
    from matplotlib.figure import Figure
    from matplotlib.gridspec import SubplotSpec
    from matplotlib.text import Text
    from matplotlib.transforms import Transform

    from plotnine.typing import HorizontalJustification, VerticalJustification

    from .gridspec import p9GridSpec


def bbox_in_figure_space(
    artist: Artist, fig: Figure, renderer: RendererBase
) -> Bbox:
    """
    Bounding box of artist in figure coordinates
    """
    pass


def tight_bbox_in_figure_space(
    artist: Artist, fig: Figure, renderer: RendererBase
) -> Bbox:
    """
    Bounding box of artist and its children in figure coordinates
    """
    pass


def bbox_in_axes_space(
    artist: Artist, ax: Axes, renderer: RendererBase
) -> Bbox:
    """
    Bounding box of artist in figure coordinates
    """
    pass


def pts_in_figure_space(fig: Figure, pts: float) -> float:
    """
    Points in figure coordinates
    """
    pass


def get_transPanels(fig: Figure, gs: p9GridSpec) -> Transform:
    """
    Coordinate system of the Panels (facets) area

    (0, 0) is the bottom-left of the bottom-left panel and
    (1, 1) is the top right of the top-right panel.

    The gridspec parameters must be set before calling this function.
    i.e. gs.update have been called.
    """
    pass


def rel_position(rel: float, length: float, low: float, high: float) -> float:
    """
    Relatively position an object of a given length between two position

    Parameters
    ----------
    rel:
        Relative position of the object between the limits.
    length:
        Length of the object
    low:
        Lower limit position
    high:
        Upper limit position
    """
    pass


def get_subplotspecs(axs: list[Axes]) -> list[SubplotSpec]:
    """
    Return the SubplotSpecs of the given axes

    Parameters
    ----------
    axs:
        List of axes

    Notes
    -----
    This functions returns the innermost subplotspec and it expects
    every axes object to have one.
    """
    pass


def draw_gridspec(gs: p9GridSpec, color="black", **kwargs):
    """
    A debug function to draw a rectangle around the gridspec
    """
    pass


def draw_bbox(bbox, figure, color="black", **kwargs):
    """
    A debug function to draw a rectangle around a bounding bbox
    """
    pass


@dataclass
class ArtistGeometry:
    """
    Helper to calculate the position & extents (space) of an artist
    """

    figure: Figure

    def __post_init__(self):
        self.renderer = cast("RendererBase", self.figure._get_renderer())  # pyright: ignore

    def bbox(self, artist: Artist) -> Bbox:
        """
        Bounding box of artist in figure coordinates
        """
        pass

    def tight_bbox(self, artist: Artist) -> Bbox:
        """
        Bounding box of artist and its children in figure coordinates
        """
        pass

    def width(self, artist: Artist) -> float:
        """
        Width of artist in figure space
        """
        pass

    def tight_width(self, artist: Artist) -> float:
        """
        Width of artist and its children in figure space
        """
        pass

    def height(self, artist: Artist) -> float:
        """
        Height of artist in figure space
        """
        pass

    def tight_height(self, artist: Artist) -> float:
        """
        Height of artist and its children in figure space
        """
        pass

    def size(self, artist: Artist) -> tuple[float, float]:
        """
        (width, height) of artist in figure space
        """
        pass

    def tight_size(self, artist: Artist) -> tuple[float, float]:
        """
        (width, height) of artist and its children in figure space
        """
        pass

    def left_x(self, artist: Artist) -> float:
        """
        x value of the left edge of the artist

         ---
        x   |
         ---
        """
        pass

    def right_x(self, artist: Artist) -> float:
        """
        x value of the left edge of the artist

         ---
        |   x
         ---
        """
        pass

    def top_y(self, artist: Artist) -> float:
        """
        y value of the top edge of the artist

         -y-
        |   |
         ---
        """
        pass

    def bottom_y(self, artist: Artist) -> float:
        """
        y value of the bottom edge of the artist

         ---
        |   |
         -y-
        """
        pass

    def max_width(self, artists: Sequence[Artist]) -> float:
        """
        Return the maximum width of list of artists
        """
        pass

    def max_height(self, artists: Sequence[Artist]) -> float:
        """
        Return the maximum height of list of artists
        """
        pass


@dataclass
class JustifyBoundaries:
    """
    Limits about which text can be justified
    """

    plot_left: float
    plot_right: float
    plot_bottom: float
    plot_top: float
    panel_left: float
    panel_right: float
    panel_bottom: float
    panel_top: float


class TextJustifier:
    """
    Justify Text

    The justification methods reinterpret alignment values to be justification
    about a span.
    """

    def __init__(self, figure: Figure, boundaries: JustifyBoundaries):
        self.geometry = ArtistGeometry(figure)
        self.boundaries = boundaries

    def horizontally(
        self,
        text: Text,
        ha: HorizontalJustification | float,
        left: float,
        right: float,
        width: float | None = None,
    ):
        """
        Horizontally Justify text between left and right
        """
        pass

    def vertically(
        self,
        text: Text,
        va: VerticalJustification | float,
        bottom: float,
        top: float,
        height: float | None = None,
    ):
        """
        Vertically Justify text between bottom and top
        """
        pass

    def horizontally_across_panel(
        self, text: Text, ha: HorizontalJustification | float
    ):
        """
        Horizontally Justify text accross the panel(s) width
        """
        pass

    def horizontally_across_plot(
        self, text: Text, ha: HorizontalJustification | float
    ):
        """
        Horizontally Justify text across the plot's width
        """
        pass

    def vertically_along_panel(
        self, text: Text, va: VerticalJustification | float
    ):
        """
        Horizontally Justify text along the panel(s) height
        """
        pass

    def vertically_along_plot(
        self, text: Text, va: VerticalJustification | float
    ):
        """
        Vertically Justify text along the plot's height
        """
        pass

    def horizontally_about(
        self, text: Text, ratio: float, how: Literal["panel", "plot"]
    ):
        """
        Horizontally Justify text across the panel or plot
        """
        pass

    def vertically_about(
        self, text: Text, ratio: float, how: Literal["panel", "plot"]
    ):
        """
        Vertically Justify text along the panel or plot
        """
        pass
