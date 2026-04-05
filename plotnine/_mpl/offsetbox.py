from __future__ import annotations

from matplotlib.offsetbox import (
    AnchoredOffsetbox,
    AuxTransformBox,
    DrawingArea,
)
from matplotlib.patches import bbox_artist as mbbox_artist
from matplotlib.transforms import Affine2D, Bbox

from .patches import InsideStrokedRectangle

DEBUG = False


# for debugging use
def _bbox_artist(*args, **kwargs):
    pass


class ColoredDrawingArea(DrawingArea):
    """
    A Drawing Area with a background color
    """

    def __init__(
        self,
        width: float,
        height: float,
        xdescent=0.0,
        ydescent=0.0,
        clip=True,
        color="none",
    ):
        super().__init__(width, height, xdescent, ydescent, clip=clip)

        self.patch = InsideStrokedRectangle(
            (0, 0),
            width=width,
            height=height,
            facecolor=color,
            edgecolor="none",
            linewidth=0,
            antialiased=False,
        )
        self.add_artist(self.patch)


# Fix AuxTransformBox, Adds a dpi_transform
# See https://github.com/matplotlib/matplotlib/pull/7344
class DPICorAuxTransformBox(AuxTransformBox):
    """
    DPI Corrected AuxTransformBox
    """

    def __init__(self, aux_transform):
        super().__init__(aux_transform)
        self.dpi_transform = Affine2D()
        self._dpi_corrected = False

    def get_transform(self):
        """
        Return the [](`~matplotlib.transforms.Transform`) applied
        to the children
        """
        pass

    def _correct_dpi(self, renderer):
        pass

    def get_bbox(self, renderer):
        pass

    def draw(self, renderer):
        """
        Draw the children
        """
        pass


class FlexibleAnchoredOffsetbox(AnchoredOffsetbox):
    """
    An AnchoredOffsetbox that accepts x, y location
    """

    def __init__(self, xy_loc: tuple[float, float] = (0.5, 0.5), **kwargs):
        if "loc" in kwargs:
            raise ValueError(
                "FlexibleAnchoredOffsetbox does not use the 'loc' parameter"
            )

        super().__init__(loc="center", **kwargs)
        self.xy_loc = xy_loc

    def get_offset(self, bbox, renderer):  # type: ignore
        pass
