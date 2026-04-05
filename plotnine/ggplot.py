from __future__ import annotations

from collections.abc import Sequence
from copy import copy, deepcopy
from io import BytesIO
from itertools import chain
from pathlib import Path
from types import SimpleNamespace as NS
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Iterable,
    Optional,
    cast,
    overload,
)
from warnings import warn

from ._utils import (
    from_inches,
    is_data_like,
    order_as_data_mapping,
    to_inches,
    ungroup,
)
from ._utils.context import plot_context
from ._utils.ipython import (
    get_ipython,
    get_mimebundle,
    is_inline_backend,
)
from ._utils.quarto import is_knitr_engine, is_quarto_environment
from .coords import coord_cartesian
from .exceptions import PlotnineError, PlotnineWarning
from .facets import facet_null
from .facets.layout import Layout
from .geoms.geom_blank import geom_blank
from .guides.guides import guides
from .iapi import labels_view, mpl_save_view
from .layer import Layers
from .mapping.aes import aes
from .options import get_option
from .scales.scales import Scales
from .themes.theme import theme, theme_get

if TYPE_CHECKING:
    from typing import Protocol

    import pandas as pd
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure
    from typing_extensions import Self

    from plotnine import watermark
    from plotnine._mpl.gridspec import p9GridSpec
    from plotnine._mpl.layout_manager._plot_side_space import PlotSideSpaces
    from plotnine.composition import Compose
    from plotnine.coords.coord import coord
    from plotnine.facets.facet import facet
    from plotnine.typing import DataLike, FigureFormat, MimeBundle

    class PlotAddable(Protocol):
        """
        Object that can be added to a ggplot object
        """

        def __radd__(self, other: ggplot) -> ggplot:
            """
            Add to ggplot object

            Parameters
            ----------
            other :
                ggplot object

            Returns
            -------
            :
                ggplot object
            """
            ...


__all__ = ("ggplot", "ggsave", "save_as_pdf_pages")


class ggplot:
    """
    Create a new ggplot object

    Parameters
    ----------
    data :
        Default data for plot. Every layer that does not
        have data of its own will use this one.
    mapping :
        Default aesthetics mapping for the plot. These will be used
        by all layers unless specifically overridden.

    Notes
    -----
    ggplot object only have partial support for pickling. The mappings used
    by pickled objects should not reference variables in the namespace.
    """

    figure: Figure
    axs: list[Axes]
    _gridspec: p9GridSpec
    """
    Gridspec (1x1) that contains the whole plot
    """

    _sub_gridspec: p9GridSpec
    """
    Gridspec (nxn) that contains the facet panels

     -------------------------
    |  title                  |<----- ._gridspec
    |  subtitle               |
    |                         |
    |   -------------         |
    |  |      |      |<-------+------ ._sub_gridspec
    |  |      |      |        |
    |  |      |      | legend |
    |   -------------         |
    |   axis_ticks            |
    |   axis_text             |
    |   axis_title            |
    |                 caption |
    |-------------------------|
    |          footer         |
     -------------------------
    """

    _sidespaces: PlotSideSpaces

    def __init__(
        self,
        data: Optional[DataLike] = None,
        mapping: Optional[aes] = None,
    ):
        from .mapping._env import Environment

        # Allow some sloppiness
        data, mapping = order_as_data_mapping(data, mapping)
        self.data = data
        self.mapping = mapping if mapping is not None else aes()
        self.facet: facet = facet_null()
        self.labels = labels_view()
        self.layers = Layers()
        self.guides = guides()
        self.scales = Scales()
        self.theme = theme_get()
        self.coordinates: coord = coord_cartesian()
        self.environment = Environment.capture(1)
        self.layout = Layout()
        self.watermarks: list[watermark] = []

        # build artefacts
        self._build_objs = NS(meta={})

    def __str__(self) -> str:
        """
        Return a wrapped display size (in pixels) of the plot
        """
        w, h = self.theme._figure_size_px
        return f"<ggplot: ({w} x {h})>"

    def __repr__(self):
        # knitr relies on __repr__ to automatically print the last object
        # in a cell.
        if is_knitr_engine():
            self.show()
            return ""
        return super().__repr__()

    def _repr_mimebundle_(self, include=None, exclude=None) -> MimeBundle:
        """
        Return dynamic MIME bundle for plot display

        This method is called when a ggplot object is the last in the cell.

        Notes
        -----
        - https://ipython.readthedocs.io/en/stable/config/integrating.html
        """
        pass

    def show(self):
        """
        Show plot using the matplotlib backend set by the user

        This function is called for its side-effects.
        """
        pass

    def __deepcopy__(self, memo: dict[Any, Any]) -> ggplot:
        """
        Deep copy without copying the dataframe and environment
        """
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        old = self.__dict__
        new = result.__dict__

        # don't make a deepcopy of data
        shallow = {"data", "figure", "gs", "_build_objs"}
        for key, item in old.items():
            if key in shallow:
                new[key] = item
                memo[id(new[key])] = new[key]
            else:
                new[key] = deepcopy(item, memo)

        return result

    def __iadd__(self, other: PlotAddable | list[PlotAddable] | None) -> Self:
        """
        Add other to ggplot object

        Parameters
        ----------
        other :
            Either an object that knows how to "radd"
            itself to a ggplot, or a list of such objects.
        """
        if isinstance(other, Sequence):
            for item in other:
                item.__radd__(self)
        elif other is not None:
            other.__radd__(self)
        return self

    @overload
    def __add__(
        self,
        rhs: PlotAddable | list[PlotAddable] | None,
    ) -> ggplot: ...

    @overload
    def __add__(self, rhs: ggplot) -> Compose: ...

    def __add__(
        self,
        rhs: PlotAddable | list[PlotAddable] | None | ggplot,
    ) -> ggplot | Compose:
        """
        Add to ggplot

        Parameters
        ----------
        other :
            Either an object that knows how to "radd"
            itself to a ggplot, or a list of such objects.
        """
        from .composition import Compose

        self = deepcopy(self)

        if isinstance(rhs, (ggplot, Compose)):
            from .composition import Wrap

            return Wrap([self, rhs])

        return self.__iadd__(rhs)

    def __or__(self, rhs: ggplot | Compose) -> Compose:
        """
        Compose 2 plots columnwise
        """
        from .composition import Beside

        return Beside([self, rhs])

    def __truediv__(self, rhs: ggplot | Compose) -> Compose:
        """
        Compose 2 plots rowwise
        """
        from .composition import Stack

        return Stack([self, rhs])

    def __sub__(self, rhs: ggplot | Compose) -> Compose:
        """
        Compose 2 plots columnwise
        """
        from .composition import Beside

        return Beside([self, rhs])

    def __rrshift__(self, other: DataLike) -> ggplot:
        """
        Overload the >> operator to receive a dataframe
        """
        other = ungroup(other)
        if is_data_like(other):
            if self.data is None:
                self.data = other
            else:
                raise PlotnineError("`>>` failed, ggplot object has data.")
        else:
            msg = "Unknown type of data -- {!r}"
            raise TypeError(msg.format(type(other)))
        return self

    def draw(self, *, show: bool = False) -> Figure:
        """
        Render the complete plot

        Parameters
        ----------
        show :
            Whether to show the plot.

        Returns
        -------
        :
            Matplotlib figure
        """
        pass

    def _setup(self) -> Figure:
        """
        Setup this instance for the building process
        """
        pass

    def _create_figure(self):
        """
        Create gridspec for the panels
        """
        pass

    def _build(self):
        """
        Build ggplot for rendering.

        Notes
        -----
        This method modifies the ggplot object. The caller is
        responsible for making a copy and using that to make
        the method call.
        """
        pass

    def _draw_panel_borders(self):
        """
        Draw Panel boders
        """
        pass

    def _draw_layers(self):
        """
        Draw the main plot(s) onto the axes.
        """
        pass

    def _draw_breaks_and_labels(self):
        """
        Draw breaks and labels
        """
        pass

    def _draw_figure_texts(self):
        """
        Draw title, x label, y label and caption onto the figure
        """
        pass

    def _draw_watermarks(self):
        """
        Draw watermark onto figure
        """
        pass

    def _draw_plot_background(self):
        pass

    def _save_filename(self, ext: str) -> Path:
        """
        Make a filename for use by the save method

        Parameters
        ----------
        ext : str
            Extension e.g. png, pdf, ...
        """
        pass

    def save_helper(
        self: ggplot,
        filename: Optional[str | Path | BytesIO] = None,
        format: Optional[str] = None,
        path: Optional[str] = None,
        width: Optional[float] = None,
        height: Optional[float] = None,
        units: str = "in",
        dpi: Optional[float] = None,
        limitsize: bool | None = None,
        verbose: bool = True,
        **kwargs: Any,
    ) -> mpl_save_view:
        """
        Create MPL figure that will be saved

        Notes
        -----
        This method has the same arguments as [](`~plotnine.ggplot.save`).
        Use it to get access to the figure that will be saved.
        """
        pass

    def save(
        self,
        filename: Optional[str | Path | BytesIO] = None,
        format: Optional[str] = None,
        path: str = "",
        width: Optional[float] = None,
        height: Optional[float] = None,
        units: str = "in",
        dpi: Optional[int] = None,
        limitsize: bool | None = None,
        verbose: bool = True,
        **kwargs: Any,
    ):
        """
        Save a ggplot object as an image file

        Parameters
        ----------
        filename :
            File name to write the plot to. If not specified, a name
            like “plotnine-save-<hash>.<format>” is used.
        format :
            Image format to use, automatically extract from
            file name extension.
        path :
            Path to save plot to (if you just want to set path and
            not filename).
        width :
            Width (defaults to value set by the theme). If specified
            the `height` must also be given.
        height :
            Height (defaults to value set by the theme). If specified
            the `width` must also be given.
        units :
            Units for width and height when either one is explicitly
            specified (in, cm, or mm).
        dpi :
            DPI to use for raster graphics. If None, defaults to using
            the `dpi` of theme, if none is set then a `dpi` of 100.
        limitsize :
            If `True` (the default), save will not save images
            larger than 25x25 inches, to prevent the common error
            of specifying dimensions in pixels. The default value
            is from the option `plotine.options.limitsize`.
        verbose :
            If `True`, print the saving information.
        kwargs :
            Additional arguments to pass to matplotlib `savefig()`.
        """
        pass

    def layer_data(self, i: int = 0) -> pd.DataFrame:
        """
        Return the data used to draw a specific plot layer

        Parameters
        ----------
        i :
            Index of the layer to retrieve, starting from 0.

        Returns
        -------
        pd.DataFrame
            Data used by the specified layer after all transformations,
            statistics, and position adjustments have been applied.
        """
        pass


ggsave = ggplot.save


def save_as_pdf_pages(
    plots: Iterable[ggplot],
    filename: Optional[str | Path] = None,
    path: str | None = None,
    verbose: bool = True,
    **kwargs: Any,
):
    """
    Save multiple [](`~plotnine.ggplot`) objects to a PDF file, one per page.

    Parameters
    ----------
    plots :
        Plot objects to write to file. `plots` may be either a
        collection such as a [](:class:`list`) or [](:class:`set`)

        ```python
        base_plot = ggplot(…)
        plots = [base_plot + ggtitle('%d of 3' % i) for i in range(1, 3)]
        save_as_pdf_pages(plots)
        ```

        or, a generator that yields [](`~plotnine.ggplot`) objects:

        ```python
        def myplots():
            for i in range(1, 3):
                yield ggplot(…) + ggtitle('%d of 3' % i)
        save_as_pdf_pages(myplots())
        ```
    filename :
        File name to write the plot to. If not specified, a name
        like “plotnine-save-<hash>.pdf” is used.
    path :
        Path to save plot to (if you just want to set path and
        not filename).
    verbose :
        If `True`, print the saving information.
    kwargs :
        Additional arguments to pass to
        [](:meth:`~matplotlib.figure.Figure.savefig`).

    Notes
    -----
    Using pandas [](:meth:`~pandas.DataFrame.groupby`) methods, tidy data
    can be "faceted" across pages:

    ```python
    from plotnine.data import mtcars

    def facet_pages(column)
        base_plot = [
            aes(x="wt", y="mpg", label="name"),
            geom_text(),
        ]
        for label, group_data in mtcars.groupby(column):
            yield ggplot(group_data) + base_plot + ggtitle(label)

    save_as_pdf_pages(facet_pages('cyl'))
    ```

    Unlike [](:meth:`~plotnine.ggplot.save`),
    [](:meth:`~plotnine.save_as_pdf_pages`)
    does not process arguments for `height` or `width`. To set the figure
    size, add [](`~plotnine.themes.themeable.figure_size`) to the theme
    for some or all of the objects in `plots`:

    ```python
    plot = ggplot(…)
    # The following are equivalent
    plot.save('filename.pdf', height=6, width=8)
    save_as_pdf_pages([plot + theme(figure_size=(8, 6))])
    ```
    """
    pass
