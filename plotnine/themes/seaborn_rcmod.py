# type: ignore

"""Functions that alter the matplotlib rc dictionary on the fly."""

import functools

import matplotlib as _mpl

# https://github.com/mwaskom/seaborn/blob/master/seaborn/rcmod.py
# License: BSD-3-Clause License
#
# Modifications
# ---------------
# modified set_theme()
# removed set_palette(), reset_defaults(), reset_orig()
#
# We (plotnine) do not want to modify the rcParams
# on the matplotlib instance, so we create a dummy object
# The set_* function work on the rcParams dict on that
# object and then set() returns it. Then outside this
# file we only need to call the set() function.


class dummy:
    """
    No Op
    """

    __version__ = _mpl.__version__
    rcParams = {}


mpl = dummy()


_style_keys = [
    "axes.facecolor",
    "axes.edgecolor",
    "axes.grid",
    "axes.axisbelow",
    "axes.labelcolor",
    "figure.facecolor",
    "grid.color",
    "grid.linestyle",
    "text.color",
    "xtick.color",
    "ytick.color",
    "xtick.direction",
    "ytick.direction",
    "lines.solid_capstyle",
    "patch.edgecolor",
    "patch.force_edgecolor",
    "image.cmap",
    "font.family",
    "font.sans-serif",
    "xtick.bottom",
    "xtick.top",
    "ytick.left",
    "ytick.right",
    "axes.spines.left",
    "axes.spines.bottom",
    "axes.spines.right",
    "axes.spines.top",
]

_context_keys = [
    "font.size",
    "axes.labelsize",
    "axes.titlesize",
    "xtick.labelsize",
    "ytick.labelsize",
    "legend.fontsize",
    "legend.title_fontsize",
    "axes.linewidth",
    "grid.linewidth",
    "lines.linewidth",
    "lines.markersize",
    "patch.linewidth",
    "xtick.major.width",
    "ytick.major.width",
    "xtick.minor.width",
    "ytick.minor.width",
    "xtick.major.size",
    "ytick.major.size",
    "xtick.minor.size",
    "ytick.minor.size",
]


def set_theme(
    context="notebook",
    style="darkgrid",
    palette="deep",
    font="sans-serif",
    font_scale=1,
    color_codes=False,
    rc=None,
):
    """
    Set aesthetic parameters in one step

    Each set of parameters can be set directly or temporarily, see the
    referenced functions below for more information.

    Parameters
    ----------
    context : string or dict
        Plotting context parameters, see :func:`plotting_context`
    style : string or dict
        Axes style parameters, see :func:`axes_style`
    palette : string or sequence
        Color palette, see :func:`color_palette`
    font : string
        Font family, see matplotlib font manager.
    font_scale : float
        Separate scaling factor to independently scale the size of the
        font elements.
    color_codes : bool
        If `True` and `palette` is a seaborn palette, remap the shorthand
        color codes (e.g. "b", "g", "r", etc.) to the colors from this palette.
    rc : dict or None
        Dictionary of rc parameter mappings to override the above.

    """
    pass


def set(*args, **kwargs):
    """
    Alias for :func:`set_theme`, which is the preferred interface

    This function may be removed in the future.
    """
    pass


def axes_style(style=None, rc=None):
    """
    Return a parameter dict for the aesthetic style of the plots

    This affects things like the color of the axes, whether a grid is
    enabled by default, and other aesthetic elements.

    This function returns an object that can be used in a `with` statement
    to temporarily change the style parameters.

    Parameters
    ----------
    style : "darkgrid" | "whitegrid" | "dark" | "white" | "ticks" | dict | None
        A dictionary of parameters or the name of a preconfigured set.
    rc : dict
        Parameter mappings to override the values in the preset seaborn
        style dictionaries. This only updates parameters that are
        considered part of the style definition.

    Examples
    --------
    >>> st = axes_style("whitegrid")

    >>> set_style("ticks", {"xtick.major.size": 8, "ytick.major.size": 8})

    >>> import matplotlib.pyplot as plt
    >>> with axes_style("white"):
    ...     f, ax = plt.subplots()
    ...     ax.plot(x, y)               # doctest: +SKIP

    See Also
    --------
    set_style : set the matplotlib parameters for a seaborn theme
    plotting_context : return a parameter dict to to scale plot elements
    color_palette : define the color palette for a plot

    """
    pass


def set_style(style=None, rc=None):
    """
    Set the aesthetic style of the plots

    This affects things like the color of the axes, whether a grid is
    enabled by default, and other aesthetic elements.

    Parameters
    ----------
    style : "darkgrid" | "whitegrid" | "dark" | "white" | "ticks" | dict | None
        A dictionary of parameters or the name of a preconfigured set.
    rc : dict
        Parameter mappings to override the values in the preset seaborn
        style dictionaries. This only updates parameters that are
        considered part of the style definition.

    Examples
    --------
    >>> set_style("whitegrid")

    >>> set_style("ticks", {"xtick.major.size": 8, "ytick.major.size": 8})

    See Also
    --------
    axes_style : return a dict of parameters or use in a `with` statement
                 to temporarily set the style.
    set_context : set parameters to scale plot elements
    set_palette : set the default color palette for figures

    """
    pass


def plotting_context(context=None, font_scale=1, rc=None):
    """
    Return a parameter dict to scale elements of the figure

    This affects things like the size of the labels, lines, and other
    elements of the plot, but not the overall style. The base context
    is "notebook", and the other contexts are "paper", "talk", and "poster",
    which are version of the notebook parameters scaled by .8, 1.3, and 1.6,
    respectively.

    This function returns an object that can be used in a `with` statement
    to temporarily change the context parameters.

    Parameters
    ----------
    context : dict, None, or one of {paper, notebook, talk, poster}
        A dictionary of parameters or the name of a preconfigured set.
    font_scale : float, optional
        Separate scaling factor to independently scale the size of the
        font elements.
    rc : dict, optional
        Parameter mappings to override the values in the preset seaborn
        context dictionaries. This only updates parameters that are
        considered part of the context definition.

    Examples
    --------
    >>> c = plotting_context("poster")

    >>> c = plotting_context("notebook", font_scale=1.5)

    >>> c = plotting_context("talk", rc={"lines.linewidth": 2})

    >>> import matplotlib.pyplot as plt
    >>> with plotting_context("paper"):
    ...     f, ax = plt.subplots()
    ...     ax.plot(x, y)                 # doctest: +SKIP

    See Also
    --------
    set_context : set the matplotlib parameters to scale plot elements
    axes_style : return a dict of parameters defining a figure style
    color_palette : define the color palette for a plot
    """
    pass


def set_context(context=None, font_scale=1, rc=None):
    """
    Set the plotting context parameters

    This affects things like the size of the labels, lines, and other
    elements of the plot, but not the overall style. The base context
    is "notebook", and the other contexts are "paper", "talk", and "poster",
    which are version of the notebook parameters scaled by .8, 1.3, and 1.6,
    respectively.

    Parameters
    ----------
    context : dict, None, or one of {paper, notebook, talk, poster}
        A dictionary of parameters or the name of a preconfigured set.
    font_scale : float, optional
        Separate scaling factor to independently scale the size of the
        font elements.
    rc : dict, optional
        Parameter mappings to override the values in the preset seaborn
        context dictionaries. This only updates parameters that are
        considered part of the context definition.

    Examples
    --------
    >>> set_context("paper")

    >>> set_context("talk", font_scale=1.4)

    >>> set_context("talk", rc={"lines.linewidth": 2})

    See Also
    --------
    plotting_context : return a dictionary of rc parameters, or use in
                       a `with` statement to temporarily set the context.
    set_style : set the default parameters for figure style
    set_palette : set the default color palette for figures

    """
    pass


class _RCAesthetics(dict):
    def __enter__(self):
        rc = mpl.rcParams
        self._orig = {k: rc[k] for k in self._keys}
        self._set(self)

    def __exit__(self, exc_type, exc_value, exc_tb):
        self._set(self._orig)

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            pass

        return wrapper


class _AxesStyle(_RCAesthetics):
    """Light wrapper on a dict to set style temporarily."""

    _keys = _style_keys
    _set = staticmethod(set_style)


class _PlottingContext(_RCAesthetics):
    """Light wrapper on a dict to set context temporarily."""

    _keys = _context_keys
    _set = staticmethod(set_context)
