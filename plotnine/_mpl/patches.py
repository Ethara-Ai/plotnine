from __future__ import annotations

from typing import TYPE_CHECKING

from matplotlib import artist
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.transforms import Bbox

from plotnine._mpl.utils import rel_position

if TYPE_CHECKING:
    from plotnine.typing import StripPosition

    from .text import StripText


# We subclass because we want to learn the size and location
# of the box when the layout manager is running.
# With MPLs default text & boxpatch, the patch gets its
# dimension information at draw time.


class StripTextPatch(FancyBboxPatch):
    """
    Strip text background box
    """

    text: StripText
    """
    The text artists that is wrapped by this box
    """

    position: StripPosition
    """
    The position of the strip_text associated with this patch
    """

    expand: float = 1
    """
    Factor by which to expand the thickness of this patch.

    This value is used by the layout manager to increase the breadth
    of the narrower strip_backgrounds.
    """

    def __init__(self, text: StripText):
        super().__init__(
            # The position, width and height are determine in
            # .get_window_extent.
            (0, 0),
            width=1,
            height=1,
            boxstyle="square, pad=0",
            clip_on=False,
            zorder=2.2,
        )

        self.text = text
        self.position = text.draw_info.position

    def get_window_extent(self, renderer=None):
        """
        Location & dimensions of the box in display coordinates
        """
        pass

    @artist.allow_rasterization
    def draw(self, renderer):
        """
        Draw patch
        """
        pass


class InsideStrokedRectangle(Rectangle):
    """
    A rectangle whose stroked is fully contained within it
    """

    @artist.allow_rasterization
    def draw(self, renderer):
        """
        Draw with the bounds of the rectangle adjusted to contain the stroke
        """
        pass
