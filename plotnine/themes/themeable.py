"""
Provide theamables, the elements of plot can be style with theme()

From the ggplot2 documentation the axis.title inherits from text.
What this means is that axis.title and text have the same elements
that may be themed, but the scope of what they apply to is different.
The scope of text covers all text in the plot, axis.title applies
only to the axis.title. In matplotlib terms this means that a theme
that covers text also has to cover axis.title.
"""

from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING
from warnings import warn

import numpy as np

from .._utils import has_alpha_channel, to_rgba
from .._utils.registry import RegistryHierarchyMeta
from ..exceptions import PlotnineError, deprecated_themeable_name
from .elements import element_blank
from .elements.element_base import element_base

if TYPE_CHECKING:
    from collections.abc import Mapping
    from typing import Any, Optional, Sequence, Type

    from matplotlib.artist import Artist
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure

    from plotnine import theme
    from plotnine.themes.targets import ThemeTargets


class themeable(metaclass=RegistryHierarchyMeta):
    """
    Abstract class of things that can be themed.

    Every subclass of themeable is stored in a dict at
    [](`~plotnine.theme.themeables.themeable.register`) with the name
    of the subclass as the key.

    It is the base of a class hierarchy that uses inheritance in a
    non-traditional manner. In the textbook use of class inheritance,
    superclasses are general and subclasses are specializations. In some
    since the hierarchy used here is the opposite in that superclasses
    are more specific than subclasses.

    It is probably better to think if this hierarchy of leveraging
    Python's multiple inheritance to implement composition. For example
    the `axis_title` themeable is *composed of* the `x_axis_title` and the
    `y_axis_title`. We are just using multiple inheritance to specify
    this composition.

    When implementing a new themeable based on the ggplot2 documentation,
    it is important to keep this in mind and reverse the order of the
    "inherits from" in the documentation.

    For example, to implement,

    - `axis_title_x` - `x` axis label (element_text;
      inherits from `axis_title`)
    - `axis_title_y` - `y` axis label (element_text;
      inherits from `axis_title`)


    You would have this implementation:


    ```python
    class axis_title_x(themeable):
        ...

    class axis_title_y(themeable):
        ...

    class axis_title(axis_title_x, axis_title_y):
        ...
    ```

    If the superclasses fully implement the subclass, the body of the
    subclass should be "pass". Python(__mro__) will do the right thing.

    When a method does require implementation, call `super()`{.py}
    then add the themeable's implementation to the axes.

    Notes
    -----
    A user should never create instances of class
    [](`~plotnine.themes.themeable.Themeable`) or subclasses of it.
    """

    _omit: Sequence[str] = ()
    """
    Properties to ignore during the apply stage.

    These properties may have been used when creating the artists and
    applying them would create a conflict or an error.
    """

    def __init__(self, theme_element: element_base | str | float):
        self.theme_element = theme_element
        if isinstance(theme_element, element_base):
            self._properties: dict[str, Any] = theme_element.properties
        else:
            # The specific themeable takes this value and
            # does stuff with rcParams or sets something
            # on some object attached to the axes/figure
            self._properties = {"value": theme_element}

    @staticmethod
    def from_class_name(name: str, theme_element: Any) -> themeable:
        """
        Create a themeable by name

        Parameters
        ----------
        name : str
            Class name
        theme_element : element object
            An element of the type required by the theme.
            For lines, text and rects it should be one of:
            [](`~plotnine.themes.element_line`),
            [](`~plotnine.themes.element_rect`),
            [](`~plotnine.themes.element_text`) or
            [](`~plotnine.themes.element_blank`)

        Returns
        -------
        out : plotnine.themes.themeable.themeable
        """
        pass

    @classmethod
    def registry(cls) -> Mapping[str, Any]:
        return themeable._registry

    def is_blank(self) -> bool:
        """
        Return True if theme_element is made of element_blank
        """
        return isinstance(self.theme_element, element_blank)

    def merge(self, other: themeable):
        """
        Merge properties of other into self

        Raises
        ------
        ValueError
            If any of the properties are blank
        """
        pass

    def __eq__(self, other: object) -> bool:
        "Mostly for unittesting."
        return other is self or (
            isinstance(other, type(self))
            and self._properties == other._properties
        )

    @property
    def rcParams(self) -> dict[str, Any]:
        """
        Return themeables rcparams to an rcparam dict before plotting.

        Returns
        -------
        dict
            Dictionary of legal matplotlib parameters.

        This method should always call super(...).rcParams and
        update the dictionary that it returns with its own value, and
        return that dictionary.

        This method is called before plotting. It tends to be more
        useful for general themeables. Very specific themeables
        often cannot be be themed until they are created as a
        result of the plotting process.
        """
        pass

    @property
    def properties(self):
        """
        Return only the properties that can be applied
        """
        pass

    def apply(self, theme: theme):
        """
        Called by the theme to apply the themeable

        Subclasses should not have to override this method
        """
        pass

    def apply_ax(self, ax: Axes):
        """
        Called after a chart has been plotted.

        Subclasses can override this method to customize the plot
        according to the theme.

        This method should be implemented as `super().apply_ax()`{.py}
        followed by extracting the portion of the axes specific to this
        themeable then applying the properties.


        Parameters
        ----------
        ax : matplotlib.axes.Axes
        """

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        """
        Apply theme to the figure
        """

    def blank_ax(self, ax: Axes):
        """
        Blank out theme elements
        """

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        """
        Blank out elements on the figure
        """


class Themeables(dict[str, themeable]):
    """
    Collection of themeables

    The key is the name of the class.
    """

    def update(self, other: Themeables, **kwargs):  # type: ignore
        """
        Update themeables with those from `other`

        This method takes care of inserting the `themeable`
        into the underlying dictionary. Before doing the
        insertion, any existing themeables that will be
        affected by a new from `other` will either be merged
        or removed. This makes sure that a general themeable
        of type [](`~plotnine.theme.themeables.text`) can be
        added to override an existing specific one of type
        [](`~plotnine.theme.themeables.axis_text_x`).
        """
        pass

    @property
    def _dict(self):
        """
        Themeables in reverse based on the inheritance hierarchy.

        Themeables should be applied or merged in order from general
        to specific. i.e.
            - apply [](`~plotnine.theme.themeables.axis_line`)
              before [](`~plotnine.theme.themeables.axis_line_x`)
            - merge [](`~plotnine.theme.themeables.axis_line_x`)
              into [](`~plotnine.theme.themeables.axis_line`)
        """
        pass

    def setup(self, theme: theme):
        """
        Setup themeables for theming
        """
        pass

    def items(self):
        """
        List of (name, themeable) in reverse based on the inheritance.
        """
        return self._dict.items()

    def values(self):
        """
        List of themeables in reverse based on the inheritance hierarchy.
        """
        pass

    def getp(self, key: str | tuple[str, str], default: Any = None) -> Any:
        """
        Get the value a specific themeable(s) property

        Themeables store theming attribute values in the
        [](`~plotnine.themes.themeables.Themeable.properties`)
        [](`dict`). The goal of this method is to look a value from
        that dictionary, and fallback along the inheritance hierarchy
        of themeables.

        Parameters
        ----------
        key :
            Themeable and property name to lookup. If a `str`,
            the name is assumed to be "value".

        default :
            Value to return if lookup fails
        Returns
        -------
        out : object
            Value

        Raises
        ------
        KeyError
            If key is in not in any of themeables
        """
        pass

    def get_ha(self, name: str) -> float:
        """
        Get the horizontal alignement of themeable as a float

        The themeable should be and element_text
        """
        pass

    def get_va(self, name) -> float:
        """
        Get the vertical alignement of themeable as a float

        The themeable should be and element_text
        """
        pass

    def property(self, name: str, key: str = "value") -> Any:
        """
        Get the value a specific themeable(s) property

        Themeables store theming attribute values in the
        [](`~plotnine.theme.themeables.Themeable.properties`)
        [](`dict`). The goal of this method is to look a value from
        that dictionary, and fallback along the inheritance hierarchy
        of themeables.

        Parameters
        ----------
        name : str
            Themeable name
        key : str
            Property name to lookup

        Returns
        -------
        out : object
            Value

        Raises
        ------
        KeyError
            If key is in not in any of themeables
        """
        pass

    def is_blank(self, name: str) -> bool:
        """
        Return True if the themeable *name* is blank

        If the *name* is not in the list of themeables then
        the lookup falls back to inheritance hierarchy.
        If none of the themeables are in the hierarchy are
        present, `False` is returned.

        Parameters
        ----------
        names : str
            Themeable, in order of most specific to most
            general.
        """
        for th in themeable._hierarchy[name]:
            if element := self.get(th):
                return element.is_blank()

        return False


class MixinSequenceOfValues(themeable):
    """
    Make themeable also accept a sequence to values

    This makes it possible to apply a different style value similar artists.

    e.g.

        theme(axis_text_x=element_text(color=("red", "green", "blue")))

    The number of values in the list must match the number of objects
    targeted by the themeable..
    """

    def set(
        self, artists: Sequence[Artist], props: Optional[dict[str, Any]] = None
    ):
        pass


def blend_alpha(
    properties: dict[str, Any], key: str = "color"
) -> dict[str, Any]:
    """
    Blend color with alpha

    When setting color property values of matplotlib objects,
    for a color with an alpha channel, we don't want the alpha
    property if any to have any effect on that color.
    """
    pass


# element_text themeables


class axis_title_x(themeable):
    """
    x axis label

    Parameters
    ----------
    theme_element : element_text
    """

    _omit = ["margin"]

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        pass

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        pass


class axis_title_y(themeable):
    """
    y axis label

    Parameters
    ----------
    theme_element : element_text
    """

    _omit = ["margin"]

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        pass

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        pass


class axis_title(axis_title_x, axis_title_y):
    """
    Axis labels

    Parameters
    ----------
    theme_element : element_text
    """


class legend_title(themeable):
    """
    Legend title

    Parameters
    ----------
    theme_element : element_text
    """

    _omit = ["margin", "ha", "va"]

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        pass

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        pass


class legend_text_legend(MixinSequenceOfValues):
    """
    Legend text for the common legend

    Parameters
    ----------
    theme_element : element_text

    Notes
    -----
    Horizontal alignment `ha` has no effect when the text is to the
    left or to the right. Likewise vertical alignment `va` has no
    effect when the text at the top or the bottom.
    """

    _omit = ["margin", "ha", "va"]

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        pass

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        pass


class legend_text_colorbar(MixinSequenceOfValues):
    """
    Colorbar text

    Parameters
    ----------
    theme_element : element_text

    Notes
    -----
    Horizontal alignment `ha` has no effect when the text is to the
    left or to the right. Likewise vertical alignment `va` has no
    effect when the text at the top or the bottom.
    """

    _omit = ["margin", "ha", "va"]

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        pass

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        pass


legend_text_colourbar = legend_text_colorbar


class legend_text(legend_text_legend, legend_text_colorbar):
    """
    Legend text

    Parameters
    ----------
    theme_element : element_text
    """


class plot_title(themeable):
    """
    Plot title

    Parameters
    ----------
    theme_element : element_text

    Notes
    -----
    The default horizontal alignment for the title is center. However the
    title will be left aligned if and only if there is a subtitle and its
    horizontal alignment has not been set (so it defaults to the left).

    The defaults ensure that, short titles are not awkwardly left-aligned,
    and that a title and a subtitle will not be awkwardly mis-aligned in
    the center or with different alignments.
    """

    _omit = ["margin"]

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        pass

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        pass


class plot_subtitle(themeable):
    """
    Plot subtitle

    Parameters
    ----------
    theme_element : element_text

    Notes
    -----
    The default horizontal alignment for the subtitle is left. And when
    it is present, by default it drags the title to the left. The subtitle
    drags the title to the left only if none of the two has their horizontal
    alignment are set.
    """

    _omit = ["margin"]

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        pass

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        pass


class plot_caption(themeable):
    """
    Plot caption

    Parameters
    ----------
    theme_element : element_text
    """

    _omit = ["margin"]

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        pass

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        pass


class plot_footer(themeable):
    """
    Plot footer

    Parameters
    ----------
    theme_element : element_text
    """

    _omit = ["margin"]

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        pass

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        pass


class plot_tag(themeable):
    """
    Plot tag

    Parameters
    ----------
    theme_element : element_text

    Notes
    -----
    The `ha` & `va` of element_text have no effect in some cases. e.g.
    if [](:class:`~plotnine.themes.themeable.plot_tag_position`) is "margin"
    and the tag is at the top it cannot be vertically aligned.

    Also `ha` & `va` can be floats if it makes sense to justify the tag
    over a span. e.g. along the panel or plot, or when aligning with
    other tags in a composition.
    """

    _omit = ["margin"]

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        pass

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        pass


class plot_title_position(themeable):
    """
    How to align the plot title and plot subtitle

    Parameters
    ----------
    theme_element : Literal["panel", "plot"], default = "panel"
        If "panel", the title / subtitle are aligned with respect
        to the panels. If "plot", they are aligned with the plot,
        excluding the margin space
    """


class plot_caption_position(themeable):
    """
    How to align the plot caption

    Parameters
    ----------
    theme_element : Literal["panel", "plot"], default = "panel"
        If "panel", the caption is aligned with respect to the
        panels. If "plot", it is aligned with the plot, excluding
        the margin space.
    """


class plot_footer_position(themeable):
    """
    How to align the plot footer

    Parameters
    ----------
    theme_element : Literal["panel", "plot"], default = "plot"
        If "panel", the footer is aligned with respect to the
        panels. If "plot", it is aligned with the plot, excluding
        the margin space.
    """


class plot_tag_location(themeable):
    """
    The area where the tag will be positioned

    Parameters
    ----------
    theme_element : Literal["margin", "plot", "panel"], default = "margin"
        If "margin", it is placed within the plot_margin.
        If "plot", it is placed in the figure, ignoring any margins.
        If "panel", it is placed within the panel area.
    """


class plot_tag_position(themeable):
    """
    Position of the tag

    Parameters
    ----------
    theme_element : Literal["topleft", "top", "topright", "left" \
                    "right", "bottomleft", "bottom", "bottomleft"] \
                    | tuple[float, float], default = "topleft"
        If the value is a string, the tag will be managed by the layout
        manager. If it is a tuple of (x, y) coordinates, they should be
        in figure space and the tag will be ignored by the layout manager.
    """


class strip_text_x(MixinSequenceOfValues):
    """
    Facet labels along the horizontal axis

    Parameters
    ----------
    theme_element : element_text
    """

    _omit = ["margin", "ha", "va"]

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        pass

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        pass


class strip_text_y(MixinSequenceOfValues):
    """
    Facet labels along the vertical axis

    Parameters
    ----------
    theme_element : element_text
    """

    _omit = ["margin", "ha", "va"]

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        pass

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        pass


class strip_text(strip_text_x, strip_text_y):
    """
    Facet labels along both axes

    Parameters
    ----------
    theme_element : element_text
    """


class title(
    axis_title,
    legend_title,
    plot_title,
    plot_subtitle,
    plot_caption,
    plot_footer,
    plot_tag,
):
    """
    All titles on the plot

    Parameters
    ----------
    theme_element : element_text
    """


class axis_text_x(MixinSequenceOfValues):
    """
    x-axis tick labels

    Parameters
    ----------
    theme_element : element_text

    Notes
    -----
    Use the `margin` to control the gap between the ticks and the
    text. e.g.

    ```python
    theme(axis_text_x=element_text(margin={"t": 5, "units": "pt"}))
    ```

    creates a margin of 5 points.
    """

    _omit = ["margin", "va"]

    def apply_ax(self, ax: Axes):
        pass

    def blank_ax(self, ax: Axes):
        pass


class axis_text_y(MixinSequenceOfValues):
    """
    y-axis tick labels

    Parameters
    ----------
    theme_element : element_text

    Notes
    -----
    Use the `margin` to control the gap between the ticks and the
    text. e.g.

    ```python
    theme(axis_text_y=element_text(margin={"r": 5, "units": "pt"}))
    ```

    creates a margin of 5 points.
    """

    _omit = ["margin", "ha"]

    def apply_ax(self, ax: Axes):
        pass

    def blank_ax(self, ax: Axes):
        pass


class axis_text(axis_text_x, axis_text_y):
    """
    Axis tick labels

    Parameters
    ----------
    theme_element : element_text

    Notes
    -----
    Use the `margin` to control the gap between the ticks and the
    text. e.g.

    ```python
    theme(axis_text=element_text(margin={"t": 5, "r": 5, "units": "pt"}))
    ```

    creates a margin of 5 points.
    """


class text(axis_text, legend_text, strip_text, title):
    """
    All text elements in the plot

    Parameters
    ----------
    theme_element : element_text
    """

    @property
    def rcParams(self) -> dict[str, Any]:
        pass


# element_line themeables


class axis_line_x(themeable):
    """
    x-axis line

    Parameters
    ----------
    theme_element : element_line
    """

    position = "bottom"
    _omit = ["solid_capstyle"]

    def apply_ax(self, ax: Axes):
        pass

    def blank_ax(self, ax: Axes):
        pass


class axis_line_y(themeable):
    """
    y-axis line

    Parameters
    ----------
    theme_element : element_line
    """

    position = "left"
    _omit = ["solid_capstyle"]

    def apply_ax(self, ax: Axes):
        pass

    def blank_ax(self, ax: Axes):
        pass


class axis_line(axis_line_x, axis_line_y):
    """
    x & y axis lines

    Parameters
    ----------
    theme_element : element_line
    """


class axis_ticks_minor_x(MixinSequenceOfValues):
    """
    x-axis tick lines

    Parameters
    ----------
    theme_element : element_line
    """

    def apply_ax(self, ax: Axes):
        pass

    def blank_ax(self, ax: Axes):
        pass


class axis_ticks_minor_y(MixinSequenceOfValues):
    """
    y-axis minor tick lines

    Parameters
    ----------
    theme_element : element_line
    """

    def apply_ax(self, ax: Axes):
        pass

    def blank_ax(self, ax: Axes):
        pass


class axis_ticks_major_x(MixinSequenceOfValues):
    """
    x-axis major tick lines

    Parameters
    ----------
    theme_element : element_line
    """

    def apply_ax(self, ax: Axes):
        pass

    def blank_ax(self, ax: Axes):
        pass


class axis_ticks_major_y(MixinSequenceOfValues):
    """
    y-axis major tick lines

    Parameters
    ----------
    theme_element : element_line
    """

    def apply_ax(self, ax: Axes):
        pass

    def blank_ax(self, ax: Axes):
        pass


class axis_ticks_major(axis_ticks_major_x, axis_ticks_major_y):
    """
    x & y axis major tick lines

    Parameters
    ----------
    theme_element : element_line
    """


class axis_ticks_minor(axis_ticks_minor_x, axis_ticks_minor_y):
    """
    x & y axis minor tick lines

    Parameters
    ----------
    theme_element : element_line
    """


class axis_ticks_x(axis_ticks_major_x, axis_ticks_minor_x):
    """
    x major and minor axis tick lines

    Parameters
    ----------
    theme_element : element_line
    """


class axis_ticks_y(axis_ticks_major_y, axis_ticks_minor_y):
    """
    y major and minor axis tick lines

    Parameters
    ----------
    theme_element : element_line
    """


class axis_ticks(axis_ticks_major, axis_ticks_minor):
    """
    x & y major and minor axis tick lines

    Parameters
    ----------
    theme_element : element_line
    """


class legend_ticks(themeable):
    """
    The ticks on a legend

    Parameters
    ----------
    theme_element : element_line
    """

    _omit = ["solid_capstyle"]

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        pass

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        pass


class panel_grid_major_x(themeable):
    """
    Vertical major grid lines

    Parameters
    ----------
    theme_element : element_line
    """

    def apply_ax(self, ax: Axes):
        pass

    def blank_ax(self, ax: Axes):
        pass


class panel_grid_major_y(themeable):
    """
    Horizontal major grid lines

    Parameters
    ----------
    theme_element : element_line
    """

    def apply_ax(self, ax: Axes):
        pass

    def blank_ax(self, ax: Axes):
        pass


class panel_grid_minor_x(themeable):
    """
    Vertical minor grid lines

    Parameters
    ----------
    theme_element : element_line
    """

    def apply_ax(self, ax: Axes):
        pass

    def blank_ax(self, ax: Axes):
        pass


class panel_grid_minor_y(themeable):
    """
    Horizontal minor grid lines

    Parameters
    ----------
    theme_element : element_line
    """

    def apply_ax(self, ax: Axes):
        pass

    def blank_ax(self, ax: Axes):
        pass


class panel_grid_major(panel_grid_major_x, panel_grid_major_y):
    """
    Major grid lines

    Parameters
    ----------
    theme_element : element_line
    """


class panel_grid_minor(panel_grid_minor_x, panel_grid_minor_y):
    """
    Minor grid lines

    Parameters
    ----------
    theme_element : element_line
    """


class panel_grid(panel_grid_major, panel_grid_minor):
    """
    Grid lines

    Parameters
    ----------
    theme_element : element_line
    """


class plot_footer_line(themeable):
    """
    Line above the footer

    Parameters
    ----------
    theme_element : element_line
    """

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        pass

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        pass


class line(axis_line, axis_ticks, panel_grid, legend_ticks, plot_footer_line):
    """
    All line elements

    Parameters
    ----------
    theme_element : element_line
    """

    @property
    def rcParams(self) -> dict[str, Any]:
        pass


# element_rect themeables


class legend_key(MixinSequenceOfValues):
    """
    Legend key background

    Parameters
    ----------
    theme_element : element_rect
    """

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        pass

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        pass


class legend_frame(themeable):
    """
    Frame around colorbar

    Parameters
    ----------
    theme_element : element_rect
    """

    _omit = ["facecolor"]

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        pass

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        pass


class legend_background(themeable):
    """
    Legend background

    Parameters
    ----------
    theme_element : element_rect
    """

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        pass

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        pass


class legend_box_background(themeable):
    """
    Legend box background

    Parameters
    ----------
    theme_element : element_rect

    Notes
    -----
    Not Implemented. We would have to place the outermost
    VPacker/HPacker boxes that hold the individual legends
    onto an object that has a patch.
    """


class panel_background(legend_key):
    """
    Panel background

    Parameters
    ----------
    theme_element : element_rect
    """

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        pass

    def apply_ax(self, ax: Axes):
        pass

    def blank_ax(self, ax: Axes):
        pass


class panel_border(MixinSequenceOfValues):
    """
    Panel border

    Parameters
    ----------
    theme_element : element_rect
    """

    _omit = ["facecolor"]

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        pass

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        pass


class plot_background(themeable):
    """
    Plot background

    Parameters
    ----------
    theme_element : element_rect
    """

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        pass

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        pass


class plot_footer_background(themeable):
    """
    Footer background

    The background is placed across the entire with of the plot,
    or the composition. And the height is determined by the height
    of the footer including the top and bottom margin.

    Parameters
    ----------
    theme_element : element_rect
    """

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        pass

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        pass


class strip_background_x(MixinSequenceOfValues):
    """
    Horizontal facet label background

    Parameters
    ----------
    theme_element : element_rect
    """

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        pass

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        pass


class strip_background_y(MixinSequenceOfValues):
    """
    Vertical facet label background

    Parameters
    ----------
    theme_element : element_rect
    """

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        pass

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        pass


class strip_background(strip_background_x, strip_background_y):
    """
    Facet label background

    Parameters
    ----------
    theme_element : element_rect
    """


class rect(
    legend_frame,
    legend_background,
    panel_background,
    panel_border,
    plot_background,
    plot_footer_background,
    strip_background,
):
    """
    All rectangle elements

    Parameters
    ----------
    theme_element : element_rect
    """


# themeables with scalar values


class axis_ticks_length_major_x(themeable):
    """
    x-axis major-tick length

    Parameters
    ----------
    theme_element : float | complex
        Value in points. A negative value creates the ticks
        inside the plot panel. A complex value (e.g. `3j`)
        creates ticks that span both in and out of the panel.
    """

    def apply_ax(self, ax: Axes):
        pass


class axis_ticks_length_major_y(themeable):
    """
    y-axis major-tick length

    Parameters
    ----------
    theme_element : float | complex
        Value in points. A negative value creates the ticks
        inside the plot panel. A complex value (e.g. `3j`)
        creates ticks that span both in and out of the panel.
    """

    def apply_ax(self, ax: Axes):
        pass


class axis_ticks_length_major(
    axis_ticks_length_major_x, axis_ticks_length_major_y
):
    """
    Axis major-tick length

    Parameters
    ----------
    theme_element : float
        Value in points. A negative value creates the ticks
        inside the plot panel. A complex value (e.g. `3j`)
        creates ticks that span both in and out of the panel.
    """


class axis_ticks_length_minor_x(themeable):
    """
    x-axis minor-tick length

    Parameters
    ----------
    theme_element : float | complex
        Value in points. A negative value creates the ticks
        inside the plot panel. A complex value (e.g. `3j`)
        creates ticks that span both in and out of the panel.
    """

    def apply_ax(self, ax: Axes):
        pass


class axis_ticks_length_minor_y(themeable):
    """
    x-axis minor-tick length

    Parameters
    ----------
    theme_element : float | complex
        Value in points. A negative value creates the ticks
        inside the plot panel. A complex value (e.g. `3j`)
        creates ticks that span both in and out of the panel.
    """

    def apply_ax(self, ax: Axes):
        pass


class axis_ticks_length_minor(
    axis_ticks_length_minor_x, axis_ticks_length_minor_y
):
    """
    Axis minor-tick length

    Parameters
    ----------
    theme_element : float | complex
        Value in points. A negative value creates the ticks
        inside the plot panel. A complex value (e.g. `3j`)
        creates ticks that span both in and out of the panel.
    """


class axis_ticks_length(axis_ticks_length_major, axis_ticks_length_minor):
    """
    Axis tick length

    Parameters
    ----------
    theme_element : float | complex
        Value in points. A negative value creates the ticks
        inside the plot panel. A complex value (e.g. `3j`)
        creates ticks that span both in and out of the panel.
    """


class panel_spacing_x(themeable):
    """
    Horizontal spacing between the facet panels

    Parameters
    ----------
    theme_element : float
        Size as a fraction of the figure width.
    """


class panel_spacing_y(themeable):
    """
    Vertical spacing between the facet panels

    Parameters
    ----------
    theme_element : float
        Size as a fraction of the figure width.

    Notes
    -----
    It is deliberate to have the vertical spacing be a fraction of
    the width. That means that when
    [](`~plotnine.theme.themeables.panel_spacing_x`) is the
    equal [](`~plotnine.theme.themeables.panel_spacing_x`),
    the spaces in both directions will be equal.
    """


class panel_spacing(panel_spacing_x, panel_spacing_y):
    """
    Spacing between the facet panels

    Parameters
    ----------
    theme_element : float
        Size as a fraction of the figure's dimension.
    """


# TODO: Distinct margins in all four directions
class plot_margin_left(themeable):
    """
    Plot Margin on the left

    Parameters
    ----------
    theme_element : float
        Must be in the [0, 1] range. It is specified
        as a fraction of the figure width and figure
        height.
    """


class plot_margin_right(themeable):
    """
    Plot Margin on the right

    Parameters
    ----------
    theme_element : float
        Must be in the [0, 1] range. It is specified
        as a fraction of the figure width and figure
        height.
    """


class plot_margin_top(themeable):
    """
    Plot Margin at the top

    Parameters
    ----------
    theme_element : float
        Must be in the [0, 1] range. It is specified
        as a fraction of the figure width and figure
        height.
    """


class plot_margin_bottom(themeable):
    """
    Plot Margin at the bottom

    Parameters
    ----------
    theme_element : float
        Must be in the [0, 1] range. It is specified
        as a fraction of the figure width and figure
        height.
    """


class plot_margin(
    plot_margin_left, plot_margin_right, plot_margin_top, plot_margin_bottom
):
    """
    Plot Margin

    Parameters
    ----------
    theme_element : float
        Must be in the [0, 1] range. It is specified
        as a fraction of the figure width and figure
        height.
    """


class panel_ontop(themeable):
    """
    Place panel background & gridlines over/under the data layers

    Parameters
    ----------
    theme_element : bool
        Default is False.
    """

    def apply_ax(self, ax: Axes):
        pass


class aspect_ratio(themeable):
    """
    Aspect ratio of the panel(s)

    Parameters
    ----------
    theme_element : float
        `panel_height / panel_width`

    Notes
    -----
    For a fixed relationship between the `x` and `y` scales,
    use [](`~plotnine.coords.coord_fixed`).
    """


class dpi(themeable):
    """
    DPI with which to draw/save the figure

    Parameters
    ----------
    theme_element : int
    """

    # fig.set_dpi does not work
    # https://github.com/matplotlib/matplotlib/issues/24644

    @property
    def rcParams(self) -> dict[str, Any]:
        pass


class figure_size(themeable):
    """
    Figure size in inches

    Parameters
    ----------
    theme_element : tuple
        (width, height) in inches
    """

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        pass


class legend_box(themeable):
    """
    How to box up multiple legends

    Parameters
    ----------
    theme_element : Literal["vertical", "horizontal"]
        Whether to stack up the legends vertically or
        horizontally.
    """


class legend_box_margin(themeable):
    """
    Padding between the legends and the box

    Parameters
    ----------
    theme_element : int
        Value in points.
    """


class legend_box_just(themeable):
    """
    Justification of guide boxes

    Parameters
    ----------
    theme_element : Literal["left", "right", "center", "top", "bottom", \
                    "baseline"], default=None
        If `None`, the value that will apply depends on
        [](`~plotnine.theme.themeables.legend_box`).
    """


class legend_justification_right(themeable):
    """
    Justification of legends placed on the right

    Parameters
    ----------
    theme_element : Literal["bottom", "center", "top"] | float
        How to justify the entire group with 1 or more guides. i.e. How
        to slide the legend along the right column.
        If a float, it should be in the range `[0, 1]`, where
        `0` is `"bottom"` and `1` is `"top"`.
    """


class legend_justification_left(themeable):
    """
    Justification of legends placed on the left

    Parameters
    ----------
    theme_element : Literal["bottom", "center", "top"] | float
        How to justify the entire group with 1 or more guides. i.e. How
        to slide the legend along the left column.
        If a float, it should be in the range `[0, 1]`, where
        `0` is `"bottom"` and `1` is `"top"`.
    """


class legend_justification_top(themeable):
    """
    Justification of legends placed at the top

    Parameters
    ----------
    theme_element : Literal["left", "center", "right"] | float
        How to justify the entire group with 1 or more guides. i.e. How
        to slide the legend along the top row.
        If a float, it should be in the range `[0, 1]`, where
        `0` is `"left"` and `1` is `"right"`.
    """


class legend_justification_bottom(themeable):
    """
    Justification of legends placed at the bottom

    Parameters
    ----------
    theme_element : Literal["left", "center", "right"] | float
        How to justify the entire group with 1 or more guides. i.e. How
        to slide the legend along the bottom row.
        If a float, it should be in the range `[0, 1]`, where
        `0` is `"left"` and `1` is `"right"`.
    """


class legend_justification_inside(themeable):
    """
    Justification of legends placed inside the axes

    Parameters
    ----------
    theme_element : Literal["left", "right", "center", "top", "bottom"] | \
                    float | tuple[float, float]
        How to justify the entire group with 1 or more guides. i.e. What
        point of the legend box to place at the destination point in the
        panels area.

        If a float, it should be in the range `[0, 1]`, and it implies the
        horizontal part and with the vertical part fixed at `0.5`.

        Therefore a float value of `0.8` equivalent to a tuple value of
        `(0.8, 0.5)`.
    """


class legend_justification(
    legend_justification_right,
    legend_justification_left,
    legend_justification_top,
    legend_justification_bottom,
    legend_justification_inside,
):
    """
    Justification of any legend

    Parameters
    ----------
    theme_element : Literal["left", "right", "center", "top", "bottom"] | \
                    float | tuple[float, float]
        How to justify the entire group with 1 or more guides.
    """


class legend_direction(themeable):
    """
    Layout items in the legend

    Parameters
    ----------
    theme_element : Literal["vertical", "horizontal"]
        Vertically or horizontally
    """


class legend_key_width(themeable):
    """
    Legend key background width

    Parameters
    ----------
    theme_element : float
        Value in points
    """


class legend_key_height(themeable):
    """
    Legend key background height

    Parameters
    ----------
    theme_element : float
        Value in points.
    """


class legend_key_size(legend_key_width, legend_key_height):
    """
    Legend key background width and height

    Parameters
    ----------
    theme_element : float
        Value in points.
    """


class legend_ticks_length(themeable):
    """
    Length of ticks in the legend

    Parameters
    ----------
    theme_element : float
        A good value should be in the range `[0, 0.5]`.
    """


class legend_margin(themeable):
    """
    Padding between the legend and the inner box

    Parameters
    ----------
    theme_element : float
        Value in points
    """


class legend_box_spacing(themeable):
    """
    Spacing between the legend and the plotting area

    Parameters
    ----------
    theme_element : float
        Value in points.
    """


class legend_spacing(themeable):
    """
    Spacing between two adjacent legends

    Parameters
    ----------
    theme_element : float
        Value in points.
    """


class legend_position_inside(themeable):
    """
    Location of legend

    Parameters
    ----------
    theme_element : tuple[float, float]
        Where to place legends that are inside the panels / facets area.
        The values should be in the range `[0, 1]`. The default is to
        put it in the center (`(.5, .5)`) of the panels area.
    """


class legend_position(legend_position_inside):
    """
    Location of legend

    Parameters
    ----------
    theme_element : Literal["right", "left", "top", "bottom", "inside"] | \
                    tuple[float, float] | Literal["none"]
        Where to put the legend. Along the edge or inside the panels.

        If "inside", the default location is
        [](:class:`~plotnine.themes.themeable.legend_position_inside`).

        A tuple of values implies "inside" the panels at those exact values,
        which should be in the range `[0, 1]` within the panels area.

        A value of `"none"` turns off the legend.
    """


class legend_title_position(themeable):
    """
    Position of legend title

    Parameters
    ----------
    theme_element : Literal["top", "bottom", "left", "right"] | None
        Position of the legend title. The default depends on the position
        of the legend.
    """


class legend_text_position(themeable):
    """
    Position of the legend text

    Alignment of legend title

    Parameters
    ----------
    theme_element : Literal["top", "bottom", "left", "right"] | \
                    Sequence[Literal["top", "bottom"]] | \
                    Sequence[Literal["left", "right"]] | \
                    Literal["top-bottom", "bottom-top"] | \
                    Literal["left-right", "right-left"] | \
                    None
        Position of the legend key text.
        It must be compatible with the position of the legend e.g.
        when the legend is at the top or bottom, text can only be top
        or bottom as well.
        The default depends on the position of the legend.
        Use a sequence to specify the position of each text, or
        hyphenated values like `"left-right"` to alternate the position.

    Notes
    -----
    Sequences and alternation only works well for colorbars.
    """


class legend_key_spacing_x(themeable):
    """
    Horizontal spacing between two entries in a legend

    Parameters
    ----------
    theme_element : int
        Size in points
    """


class legend_key_spacing_y(themeable):
    """
    Vertical spacing between two entries in a legend

    Parameters
    ----------
    theme_element : int
        Size in points
    """


class legend_key_spacing(legend_key_spacing_x, legend_key_spacing_y):
    """
    Spacing between two entries in a legend

    Parameters
    ----------
    theme_element : int
        Size in points
    """


class strip_align_x(themeable):
    """
    Vertical alignment of the strip & its background w.r.t the panel border

    Parameters
    ----------
    theme_element : float
        Value as a proportion of the strip size. A good value
        should be the range `[-1, 0.5]`. A negative value
        puts the strip inside the axes. A positive value creates
        a margin between the strip and the axes. `0` puts the
        strip on top of the panels.
    """


class strip_align_y(themeable):
    """
    Horizontal alignment of the strip & its background w.r.t the panel border

    Parameters
    ----------
    theme_element : float
        Value as a proportion of the strip size. A good value
        should be the range `[-1, 0.5]`. A negative value
        puts the strip inside the axes. A positive value creates
        a margin between the strip and the axes. `0` puts the
        strip exactly beside the panels.
    """


class strip_align(strip_align_x, strip_align_y):
    """
    Alignment of the strip & its background w.r.t the panel border

    Parameters
    ----------
    theme_element : float
        Value as a proportion of the strip text size. A good value
        should be the range `[-1, 0.5]`. A negative value
        puts the strip inside the axes and a positive value
        creates a space between the strip and the axes.
    """


class svg_usefonts(themeable):
    """
    How to renderer fonts for svg images

    Parameters
    ----------
    theme_element : bool
        If `True`, assume fonts are installed on the machine where
        the SVG will be viewed.

        If `False`, embed characters as paths; this is supported by
        most SVG renderers.

        You should probably set this to `True` if you intend to edit
        the svg file.
    """

    @property
    def rcParams(self) -> dict[str, Any]:
        pass


# Deprecated


class subplots_adjust(themeable):
    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        pass


@deprecated_themeable_name
class legend_entry_spacing(legend_key_spacing):
    pass


@deprecated_themeable_name
class legend_entry_spacing_x(legend_key_spacing_x):
    pass


@deprecated_themeable_name
class legend_entry_spacing_y(legend_key_spacing_y):
    pass


class legend_title_align(themeable):
    def __init__(self):
        msg = (
            "Themeable 'legend_title_align' is deprecated. Use the "
            "horizontal and vertical alignment parameters ha & va "
            "of 'element_text' with 'lenged_title'."
        )
        warn(msg, FutureWarning, stacklevel=1)


class axis_ticks_direction_x(themeable):
    """
    x-axis tick direction

    Parameters
    ----------
    theme_element : Literal["in", "out"]
        `in` for ticks inside the panel.
        `out` for ticks outside the panel.
    """

    def __init__(self, theme_element):
        msg = (
            f"Themeable '{self.__class__.__name__}' is deprecated and"
            "will be removed in a future version. "
            "Use +ve or -ve values of the axis_ticks_length"
            "to affect the direction of the ticks."
        )
        warn(msg, FutureWarning, stacklevel=1)
        super().__init__(theme_element)

    def apply_ax(self, ax: Axes):
        pass


class axis_ticks_direction_y(themeable):
    """
    y-axis tick direction

    Parameters
    ----------
    theme_element : Literal["in", "out"]
        `in` for ticks inside the panel.
        `out` for ticks outside the panel.
    """

    def __init__(self, theme_element):
        msg = (
            f"Themeable '{self.__class__.__name__}' is deprecated and"
            "will be removed in a future version. "
            "Use +ve/-ve/complex values of the axis_ticks_length"
            "to affect the direction of the ticks."
        )
        warn(msg, FutureWarning, stacklevel=1)
        super().__init__(theme_element)

    def apply_ax(self, ax: Axes):
        pass


class axis_ticks_direction(axis_ticks_direction_x, axis_ticks_direction_y):
    """
    axis tick direction

    Parameters
    ----------
    theme_element : Literal["in", "out"]
        `in` for ticks inside the panel.
        `out` for ticks outside the panel.
    """


class axis_ticks_pad_major_x(themeable):
    """
    x-axis major-tick padding

    Parameters
    ----------
    theme_element : float
        Value in points.
    """

    def apply_ax(self, ax: Axes):
        pass


class axis_ticks_pad_major_y(themeable):
    """
    y-axis major-tick padding

    Parameters
    ----------
    theme_element : float
        Value in points.

    Note
    ----
    Padding is not applied when the
    [](`~plotnine.theme.themeables.axis_ticks_major_y`) are
    blank, but it does apply when the
    [](`~plotnine.theme.themeables.axis_ticks_length_major_y`)
    is zero.
    """

    def apply_ax(self, ax: Axes):
        pass


class axis_ticks_pad_major(axis_ticks_pad_major_x, axis_ticks_pad_major_y):
    """
    Axis major-tick padding

    Parameters
    ----------
    theme_element : float
        Value in points.

    Note
    ----
    Padding is not applied when the
    [](`~plotnine.theme.themeables.axis_ticks_major`) are blank,
    but it does apply when the
    [](`~plotnine.theme.themeables.axis_ticks_length_major`) is zero.
    """


class axis_ticks_pad_minor_x(themeable):
    """
    x-axis minor-tick padding

    Parameters
    ----------
    theme_element : float

    Note
    ----
    Padding is not applied when the
    [](`~plotnine.theme.themeables.axis_ticks_minor_x`) are
    blank, but it does apply when the
    [](`~plotnine.theme.themeables.axis_ticks_length_minor_x`) is zero.
    """

    def apply_ax(self, ax: Axes):
        pass


class axis_ticks_pad_minor_y(themeable):
    """
    y-axis minor-tick padding

    Parameters
    ----------
    theme_element : float

    Note
    ----
    Padding is not applied when the
    [](`~plotnine.theme.themeables.axis_ticks_minor_y`) are
    blank, but it does apply when the
    [](`~plotnine.theme.themeables.axis_ticks_length_minor_y`)
    is zero.
    """

    def apply_ax(self, ax: Axes):
        pass


class axis_ticks_pad_minor(axis_ticks_pad_minor_x, axis_ticks_pad_minor_y):
    """
    Axis minor-tick padding

    Parameters
    ----------
    theme_element : float

    Note
    ----
    Padding is not applied when the
    [](`~plotnine.theme.themeables.axis_ticks_minor`) are
    blank, but it does apply when the
    [](`~plotnine.theme.themeables.axis_ticks_length_minor`) is zero.
    """


class axis_ticks_pad(axis_ticks_pad_major, axis_ticks_pad_minor):
    """
    Axis tick padding

    Parameters
    ----------
    theme_element : float
        Value in points.

    Note
    ----
    Padding is not applied when the
    [](`~plotnine.theme.themeables.axis_ticks`) are blank,
    but it does apply when the
    [](`~plotnine.theme.themeables.axis_ticks_length`) is zero.
    """

    def __init__(self, theme_element):
        x = theme_element
        msg = (
            f"Themeable '{self.__class__.__name__}' is deprecated and"
            "will be removed in a future version. "
            "Use the margin parameter of axis_text. e.g.\n"
            f"axis_text_x(margin={{'t': {x}}})\n"
            f"axis_text_y(margin={{'r': {x}}})\n"
            f"axis_text(margin={{'t': {x}, 'r': {x}}})"
        )
        warn(msg, FutureWarning, stacklevel=1)
        super().__init__(theme_element)
