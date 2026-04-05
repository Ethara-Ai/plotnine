from __future__ import annotations

from typing import TYPE_CHECKING, List

from ..iapi import strip_draw_info, strip_label_details

if TYPE_CHECKING:
    from typing import Sequence

    from matplotlib.axes import Axes
    from typing_extensions import Self

    from plotnine import theme
    from plotnine.facets.facet import facet
    from plotnine.facets.layout import Layout
    from plotnine.iapi import layout_details
    from plotnine.typing import StripPosition


class strip:
    """
    A strip

    This class exists to have in one place all that is required to draw
    strip text onto an axes. As Matplotlib does not have a layout manager
    that makes it easy to adorn an axes with artists, we have to compute
    the space required for the text and the background strip on which it
    is drawn. This is very finicky and fails once the facets become
    complicated.
    """

    position: StripPosition
    label_info: strip_label_details

    def __init__(
        self,
        vars: Sequence[str],
        layout_info: layout_details,
        facet: facet,
        ax: Axes,
        position: StripPosition,
    ):
        self.vars = vars
        self.ax = ax
        self.position = position
        self.facet = facet
        self.figure = facet.figure
        self.theme = facet.theme
        self.layout_info = layout_info
        label_info = strip_label_details.make(layout_info, vars, position)
        self.label_info = facet.labeller(label_info)

    def get_draw_info(self) -> strip_draw_info:
        """
        Get information required to draw strips

        Returns
        -------
        out :
            A structure with all the coordinates (x, y) required
            to draw the strip text and the background box
            (box_x, box_y, box_width, box_height).
        """
        pass

    def draw(self):
        """
        Create a background patch and put a label on it
        """
        pass


class Strips(List[strip]):
    """
    List of strips for a plot
    """

    facet: facet

    @staticmethod
    def from_facet(facet: facet) -> Strips:
        pass

    @property
    def axs(self) -> list[Axes]:
        pass

    @property
    def layout(self) -> Layout:
        pass

    @property
    def theme(self) -> theme:
        return self.facet.theme

    @property
    def top_strips(self) -> Strips:
        pass

    @property
    def right_strips(self) -> Strips:
        pass

    def draw(self):
        pass

    def setup(self) -> Self:
        """
        Calculate the box information for all strips

        It is stored in self.strip_info
        """
        pass
