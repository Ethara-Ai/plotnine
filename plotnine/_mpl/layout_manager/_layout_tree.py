from __future__ import annotations

from dataclasses import dataclass, field
from functools import cached_property
from typing import TYPE_CHECKING, Iterator, cast

import numpy as np

from ._grid import Grid
from ._plot_side_space import PlotSideSpaces

if TYPE_CHECKING:
    from typing import Sequence, TypeAlias

    from plotnine._mpl.gridspec import p9GridSpec
    from plotnine._mpl.layout_manager._plot_side_space import (
        bottom_space,
        left_space,
        right_space,
        top_space,
    )
    from plotnine.composition import Compose

    Node: TypeAlias = "PlotSideSpaces | LayoutTree"


@dataclass
class LayoutTree:
    """
    A Tree representation of the composition

    The purpose of this class (and its subclasses) is to align and
    and resize plots in a composition. For example,

    This composition:

        (p1 | p2) | (p3 / p4)

    where p1, p2, p3 & p4 are ggplot objects would look like this;

         -----------------------------
        |         |         |         |
        |         |         |         |
        |         |         |         |
        |         |         |         |
        |         |         |---------|
        |         |         |         |
        |         |         |         |
        |         |         |         |
        |         |         |         |
         -----------------------------

    and the tree would have this structure;


                         LayoutTree (.nrow=1, .ncol=3)
                             |
               ----------------------------
              |              |             |
        LayoutSpaces    LayoutSpaces   LayoutTree (.nrow=2, .ncol=1)
                                           |
                                      -------------
                                     |             |
                               LayoutSpaces  LayoutSpaces

    This composition:

        (p1 + p2 + p4 + p5 + p6) + plot_layout(ncol=3)

    would look like this:

         -----------------------------
        |         |         |         |
        |         |         |         |
        |    p1   |    p2   |    p3   |
        |         |         |         |
        |---------|---------|---------|
        |         |         |         |
        |    p4   |    p5   |         |
        |         |         |         |
        |         |         |         |
         -----------------------------

    and have this structure


                                    LayoutTree (.nrow=3, .ncol=2)
                                          |
               -------------------------------------------------------
              |             |             |             |             |
        LayoutSpaces  LayoutSpaces  LayoutSpaces  LayoutSpaces  LayoutSpaces

    Each composition is a tree or subtree

    ## How it works

    Initially (and if the composition does not have annotation texts), the
    sub_gridspec occupies all the space available to it with the contained
    items (ggplot / Compose) having equal sizes.

    But if the full plot / composition occupy the same space, their panels
    may have different sizes because they have to share that space with the
    texts (title, subtitle, caption, axis title, axis text, tag), legends
    and plot margins that surround the panels.

    We align the panels, axis titles and tags by adding *_alignment margins;
    and resize the panels by

    Taking the sizes of these elements into account, we align the panels
    in the composition by changing the width and/or height of the gridspec.

    The information about the size (width & height) of the panels is in the
    LayoutSpaces.
    """

    cmp: Compose
    """
    Composition that this tree represents
    """

    nodes: list[PlotSideSpaces | LayoutTree]
    """
    The spaces or tree of spaces in the composition that the tree
    represents.
    """

    sub_gridspec: p9GridSpec = field(init=False, repr=False)
    """
    Gridspec (nxn) that contains the composed items
    """

    def __post_init__(self):
        self.sub_gridspec = self.cmp._sub_gridspec
        self.grid = Grid["Node"](
            self.nrow,
            self.ncol,
            self.nodes,
            order="row_major" if self.cmp.layout.byrow else "col_major",
        )

    @property
    def ncol(self) -> int:
        """
        Number of columns
        """
        pass

    @property
    def nrow(self) -> int:
        """
        Number of rows
        """
        pass

    @staticmethod
    def create(cmp: Compose) -> LayoutTree:
        """
        Create a LayoutTree for this composition

        Parameters
        ----------
        cmp :
            Composition
        """
        pass

    @cached_property
    def sub_compositions(self) -> list[LayoutTree]:
        """
        LayoutTrees of the direct sub compositions of this one
        """
        pass

    def arrange_layout(self):
        """
        Align and resize plots in composition to look good

        Aligning changes the *_alignment attributes of the side_spaces.
        Resizing, changes the parameters of the sub_gridspec.

        Note that we expect that this method will be called only on the
        tree for the top-level composition, and it is called for its
        side-effects.
        """
        pass

    def align(self):
        """
        Align all the edges in this composition & contained compositions

        This function mutates the layout spaces, specifically the
        margin_alignments along the sides of the plot.
        """
        pass

    def resize(self):
        """
        Resize panels and the entire plots

        This function mutates the composition gridspecs; specifically the
        width_ratios and height_ratios.
        """
        pass

    def align_sub_compositions(self):
        """
        Align the compositions contained in this one
        """
        pass

    def resize_sub_compositions(self):
        """
        Resize panels in the compositions contained in this one
        """
        pass

    @cached_property
    def bottom_most_spaces(self) -> list[bottom_space]:
        """
        Bottom spaces of items in the last row
        """
        pass

    @cached_property
    def top_most_spaces(self) -> list[top_space]:
        """
        Top spaces of items in the top row
        """
        pass

    @cached_property
    def left_most_spaces(self) -> list[left_space]:
        """
        Left spaces of items in the last column
        """
        pass

    @cached_property
    def right_most_spaces(self) -> list[right_space]:
        """
        Right spaces of items the last column
        """
        pass

    @property
    def panel_width(self) -> float:
        """
        A width of all panels in this composition
        """
        pass

    @property
    def panel_height(self) -> float:
        """
        A height of all panels in this composition
        """
        pass

    @property
    def plot_width(self) -> float:
        """
        A width of all plots in this tree/composition
        """
        pass

    @property
    def plot_height(self) -> float:
        """
        A height of all plots in this tree/composition
        """
        pass

    @property
    def horizontal_space(self) -> float:
        """
        Horizontal non-panel space in this composition
        """
        pass

    @property
    def vertical_space(self) -> float:
        """
        Vertical non-panel space in this composition
        """
        pass

    @property
    def horizontal_spaces(self) -> Sequence[float]:
        """
        Horizontal non-panel space by column

        For each column, the representative number for the horizontal
        space to left & right of the widest panel.
        """
        pass

    @property
    def vertical_spaces(self) -> Sequence[float]:
        """
        Vertical non-panel space by row

        For each row, the representative number for the vertical
        space is above & below the tallest panel.
        """
        pass

    @property
    def panel_widths(self) -> Sequence[float]:
        """
        Widths [figure space] of panels by column

        For each column, the representative number for the panel width
        is the maximum width among all panels in the column.
        """
        pass

    @property
    def panel_heights(self) -> Sequence[float]:
        """
        Heights [figure space] of panels by row

        For each row, the representative number for the panel height
        is the maximum height among all panels in the row.
        """
        pass

    @property
    def plot_widths(self) -> Sequence[float]:
        """
        Widths [figure space] of the plots by column

        For each column, the representative number is the width of
        the widest plot.
        """
        pass

    @property
    def plot_heights(self) -> Sequence[float]:
        """
        Heights [figure space] of the plots along vertical dimension

        For each row, the representative number is the height of
        the tallest plot.
        """
        pass

    @property
    def panel_width_ratios(self) -> Sequence[float]:
        """
        The relative widths of the panels in the composition

        These are normalised to have a mean = 1.
        """
        pass

    @property
    def panel_height_ratios(self) -> Sequence[float]:
        """
        The relative heights of the panels in the composition

        These are normalised to have a mean = 1.
        """
        pass

    def bottom_spaces_in_row(self, r: int) -> list[bottom_space]:
        """
        The bottom_spaces of plots in a given row

        If an item in the row is a compositions, then it is the
        bottom_spaces in the bottom row of that composition.
        """
        pass

    def top_spaces_in_row(self, r: int) -> list[top_space]:
        """
        The top_spaces of plots in a given row

        If an item in the row is a compositions, then it is the
        top_spaces in the top row of that composition.
        """
        pass

    def left_spaces_in_col(self, c: int) -> list[left_space]:
        """
        The left_spaces plots in a given column

        If an item in the column is a compositions, then it is the
        left_spaces in the left most column of that composition.
        """
        pass

    def right_spaces_in_col(self, c: int) -> list[right_space]:
        """
        The right_spaces of plots in a given column

        If an item in the column is a compositions, then it is the
        right_spaces in the right most column of that composition.
        """
        pass

    def iter_left_spaces(self) -> Iterator[list[left_space]]:
        """
        Left spaces for each non-empty column

        Will not return an empty list.
        """
        pass

    def iter_right_spaces(self) -> Iterator[list[right_space]]:
        """
        Right spaces for each non-empty column

        Will not return an empty list.
        """
        pass

    def iter_bottom_spaces(self) -> Iterator[list[bottom_space]]:
        """
        Bottom spaces for each non-empty row

        Will not return an empty list.
        """
        pass

    def iter_top_spaces(self) -> Iterator[list[top_space]]:
        """
        Top spaces for each non-empty row

        Will not return an empty list.
        """
        pass

    def align_panels(self):
        """
        Align the edges of the panels in the composition
        """
        pass

    def align_tags(self):
        """
        Align the tags in the composition
        """
        pass

    def align_axis_titles(self):
        """
        Align the axis titles along the composing dimension

        Since the alignment value used to for this purpose is one of
        the fields in the _side_space, it affects the space created
        for the panel.

        We could align the titles within self.align but we would have
        to store the value outside the _side_space and pick it up when
        setting the position of the texts!
        """
        pass

    def resize_widths(self):
        """
        Resize the widths of the plots & panels in the composition
        """
        pass

    def resize_heights(self):
        """
        Resize the heights of the plots & panels in the composition
        """
        pass


# For debugging
def _draw_gridspecs(tree: LayoutTree):
    pass


def _draw_sub_gridspecs(tree: LayoutTree):
    pass
