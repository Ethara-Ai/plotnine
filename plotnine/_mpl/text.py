from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING

from matplotlib import artist
from matplotlib.text import Text

from plotnine._utils import ha_as_float, va_as_float

from .patches import StripTextPatch
from .utils import bbox_in_axes_space, rel_position

if TYPE_CHECKING:
    from matplotlib.backend_bases import RendererBase

    from plotnine.iapi import strip_draw_info


class StripText(Text):
    """
    Strip Text
    """

    draw_info: strip_draw_info
    patch: StripTextPatch

    def __init__(self, info: strip_draw_info):
        kwargs = {
            "rotation": info.rotation,
            "transform": info.ax.transAxes,
            "clip_on": False,
            "zorder": 3.3,
            # Since the text can be rotated, it is simpler to anchor it at
            # the center, align it, then do the rotation. Vertically,
            # center_baseline places the text in the visual center, but
            # only if it is one line. For multiline text, we are better
            # off with plain center.
            "ha": "center",
            "va": "center_baseline" if info.is_oneline else "center",
            "rotation_mode": "anchor",
        }

        super().__init__(0, 0, info.label, **kwargs)
        self.draw_info = info
        self.patch = StripTextPatch(self)

    # TODO: This should really be part of the unit conversions in the
    # margin class.
    @lru_cache(2)
    def _line_height(self, renderer) -> float:
        """
        The line height in display space of the text on the canvas
        """
        pass

    def _set_position(self, renderer):
        """
        Set the postion of the text within the strip_background
        """
        pass

    def _set_position_top(self, renderer):
        """
        Set position of the text within the top strip_background
        """
        pass

    def _set_position_right(self, renderer):
        """
        Set position of the text within the bottom strip_background
        """
        pass

    @artist.allow_rasterization
    def draw(self, renderer: RendererBase):
        """
        Draw text along with the patch
        """
        pass
