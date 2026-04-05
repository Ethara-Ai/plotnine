from __future__ import annotations

from typing import TYPE_CHECKING, cast

try:
    from matplotlib.gridspec import GridSpecBase, SubplotParams
except ImportError:
    # MPL 3.8
    from matplotlib.figure import SubplotParams
    from matplotlib.gridspec import GridSpecBase

from matplotlib.gridspec import SubplotSpec
from matplotlib.transforms import Bbox, BboxTransformTo, TransformedBbox

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure
    from matplotlib.patches import Rectangle
    from matplotlib.transforms import Transform

    from plotnine._mpl.layout_manager._side_space import GridSpecParams
    from plotnine.composition._plot_layout import plot_layout


class p9GridSpec(GridSpecBase):
    """
    Gridspec for plotnine plots

    This gridspec does not read any subplot parameter values from matplotlib's
    rcparams. And there is no space along the edges and between the subplots.

    This gridspec can also be initialised while contained/nested in a given
    subplot.

    Parameters
    ----------
    nest_into :
        If given, this gridspec will be contained in the subplot.
    """

    _subplot_params: SubplotParams
    """
    The subplot spacing parameters of this gridspec

    These values are relative to where (figure or subplot) that the
    gridspec is contained. Use .get_subplot_params to get the absolute
    values (those in figure coordinates).
    """
    _nested_gridspecs: list[p9GridSpec]
    """
    All gridspecs that are nested into any of the subplots of this one
    """
    _patch: Rectangle

    def __init__(
        self,
        nrows,
        ncols,
        figure: Figure,
        *,
        width_ratios=None,
        height_ratios=None,
        byrow: bool = True,
        nest_into: SubplotSpec | None = None,
    ):
        self.figure = figure
        self._nested_gridspecs = []
        self._nested = nest_into is not None
        self.byrow = byrow

        super().__init__(
            nrows,
            ncols,
            width_ratios=width_ratios,
            height_ratios=height_ratios,
        )

        if nest_into:
            self._parent_subplot_spec = nest_into
            # MPL GridSpecBase expects only the subclasses that will be nested
            # to have the .get_topmost_subplotspec method.
            self.get_topmost_subplotspec = self._get_topmost_subplotspec

            # Register this gridspec as nested
            gs = cast("p9GridSpec", nest_into.get_gridspec())
            gs._nested_gridspecs.append(self)

        self._subplot_params = SubplotParams(
            left=0,
            bottom=0,
            top=1,
            right=1,
            wspace=0,
            hspace=0,
        )

    @staticmethod
    def from_layout(
        layout: plot_layout,
        figure: Figure,
        *,
        nest_into: SubplotSpec | None = None,
    ) -> p9GridSpec:
        """
        Create gridspec from a plot_layout instance
        """
        pass

    def __iter__(self):
        from itertools import product

        if self.byrow:
            for r, c in product(range(self.nrows), range(self.ncols)):
                yield SubplotSpec(self, r * self.ncols + c)
        else:
            for c, r in product(range(self.ncols), range(self.nrows)):
                yield SubplotSpec(self, r * self.ncols + c)

    @property
    def patch(self) -> Rectangle:
        """
        Background patch for the whole gridspec
        """
        pass

    @patch.setter
    def patch(self, value: Rectangle):
        """
        Set value and update position
        """
        pass

    @property
    def nested(self) -> bool:
        """
        Return True if this gridspec is nested
        """
        pass

    def _update_patch_position(self):
        """
        Update the position and size of the patch

        The patch position should be updated whenever the subplot
        parameters change.
        """
        pass

    @property
    def _axes(self) -> list[Axes]:
        """
        Axes that belong to this gridspec
        """
        pass

    def _update_axes_position(self):
        """
        Update the position of the axes in this gridspec
        """
        pass

    def _update_artists(self):
        """
        Update the artist positions that depend on this gridspec
        """
        pass

    def update_params_and_artists(self, gsparams: GridSpecParams):
        """
        Update gridspec params and the artists
        """
        pass

    def get_subplot_params(self, figure=None) -> SubplotParams:
        """
        Return the subplot parameters (in figure coordinates) for the gridspec
        """
        pass

    def _get_topmost_subplotspec(self) -> SubplotSpec:
        """
        Return the topmost `.SubplotSpec` instance associated with the subplot.

        This method starts with an underscore so that mpl's GridSpecBase does
        not think that any/all instances of this class are nested. It is then
        only dynamically assigned (without the underscore) to an instance of
        this class when it is nested into a subplot.
        """
        pass

    @property
    def bbox_relative(self):
        """
        Bounding box for the gridspec relative to the figure

        This bbox is in figure coordinates.
        """
        pass

    @property
    def bbox(self):
        """
        Bounding box of the gridspec

        This bbox is in display coordinates.
        """
        pass

    @property
    def width(self) -> float:
        """
        Width of bbox in figure space
        """
        pass

    @property
    def height(self) -> float:
        """
        Height of bbox in figure space
        """
        pass

    def to_transform(self) -> Transform:
        """
        Return transform of this gridspec

        Where:
            - (0, 0) is the bottom left of the gridspec
            - (1, 1) is the top right of the gridspec

        The output of this transform is in the display units of the figure.
        """
        pass

    def set_height_ratios(self, height_ratios):
        pass

    def set_width_ratios(self, width_ratios):
        pass
