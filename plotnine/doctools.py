from __future__ import annotations

import itertools
import os
import re
from functools import lru_cache
from textwrap import dedent, indent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Sequence, Type, TypeVar

    from plotnine.geoms.geom import geom
    from plotnine.stats.stat import stat

    T = TypeVar("T")

# Markup that is robust for documentation needs grid tables
# using tabulate and it is only required when
# building documentation.
try:
    from tabulate import tabulate as table_function
except ImportError:
    from ._utils import simple_table as table_function


# Parameter arguments that are listed first in the geom and
# stat class signatures

common_geom_params = [
    "mapping",
    "data",
    "stat",
    "position",
    "na_rm",
    "inherit_aes",
    "show_legend",
    "raster",
]
common_geom_param_values = {
    "mapping": None,
    "data": None,
    "inherit_aes": True,
    "show_legend": None,
    "raster": False,
}

common_stat_params = ["mapping", "data", "geom", "position", "na_rm"]
common_stat_param_values = common_geom_param_values

# Templates for docstrings

GEOM_SIGNATURE_TPL = """
**Usage**

{signature}

""".strip()

AESTHETICS_TABLE_TPL = """
{table}

The **bold** aesthetics are required."""

STAT_SIGNATURE_TPL = """
**Usage**

{signature}

""".strip()

common_params_doc = {
    "mapping": """\
Aesthetic mappings created with [aes](:class:`plotnine.mapping.aes.aes`). If \
specified and `inherit_aes=True`{.py}, it is combined with the default \
mapping for the plot. You must supply mapping if there is no plot mapping.""",
    "data": """\
The data to be displayed in this layer. If `None`{.py}, the data from \
from the `ggplot()`{.py} call is used. If specified, it overrides the \
data from the `ggplot()`{.py} call.""",
    "stat": """\
The statistical transformation to use on the data for this layer. \
If it is a string, it must be the registered and known to Plotnine.""",
    "position": """\
Position adjustment. If it is a string, it must be registered and \
known to Plotnine.""",
    "na_rm": """\
If `False`{.py}, removes missing values with a warning. If `True`{.py} \
silently removes missing values.""",
    "inherit_aes": """\
If `False`{.py}, overrides the default aesthetics.""",
    "show_legend": """\
Whether this layer should be included in the legends. `None`{.py} the \
default, includes any aesthetics that are mapped. If a [](:class:`bool`), \
`False`{.py} never includes and `True`{.py} always includes. A \
[](:class:`dict`) can be used to *exclude* specific aesthetis of the layer \
from showing in the legend. e.g `show_legend={'color': False}`{.py}, \
any other aesthetic are included by default.""",
    "raster": """\
If `True`, draw onto this layer a raster (bitmap) object even if\
the final image is in vector format.""",
}


GEOM_PARAMS_TPL = """
mapping : ~plotnine.mapping.aes.aes, default=None
    {mapping}
    {_aesthetics_doc}
data : ~pandas.DataFrame, default=None
    {data}
stat : str | ~plotnine.stats.stat.stat, default="{default_stat}"
    {stat}
position : str | ~plotnine.positions.position.position, \
default="{default_position}"
    {position}
na_rm : bool, default={default_na_rm}
    {na_rm}
inherit_aes : bool, default={default_inherit_aes}
    {inherit_aes}
show_legend : bool | dict, default=None
    {show_legend}
raster : bool, default={default_raster}
    {raster}
"""

STAT_PARAMS_TPL = """
mapping : ~plotnine.mapping.aes.aes, default=None
    {mapping}
    {_aesthetics_doc}
data : ~pandas.DataFrame, default=None
    {data}
geom : str | ~plotnine.geoms.geom.geom, default="{default_geom}"
    {stat}
position : str | ~plotnine.positions.position.position, \
default="{default_position}"
    {position}
na_rm : bool, default={default_na_rm}
    {na_rm}
"""

geom_kwargs = """\
**kwargs: Any
    Aesthetics or parameters used by the `stat`.
"""

stat_kwargs = """\
**kwargs: Any
    Aesthetics or parameters used by the `geom`.
"""

DOCSTRING_SECTIONS = {
    "parameters",
    "see also",
    "note",
    "notes",
    "example",
    "examples",
}

PARAM_PATTERN = re.compile(r"\s*" r"([_A-Za-z]\w*)" r"\s:\s")
SECTIONS_PATTERN = re.compile(
    r"\n(?P<section>(?:\w+|(\w+\s\w+)+))\s*"  # section name
    r"\n-{3,}\n",  # underline
)
GENERATING_QUARTODOC = os.environ.get("GENERATING_QUARTODOC")


def dict_to_table(header: tuple[str, str], contents: dict[str, str]) -> str:
    """
    Convert dict to an (n x 2) table

    Parameters
    ----------
    header : tuple
        Table header. Should have a length of 2.
    contents : dict
        The key becomes column 1 of table and the
        value becomes column 2 of table.

    Examples
    --------
    >>> d = {"alpha": 1, "color": "blue", "fill": None}
    >>> print(dict_to_table(("Aesthetic", "Default Value"), d))
    Aesthetic  Default Value
    ---------  -------------
    alpha      `1`
    color      `'blue'`
    fill       `None`
    """
    pass


def make_signature(
    name: str,
    params: dict[str, Any],
    common_params: Sequence[str],
    common_param_values: dict[str, Any],
) -> str:
    """
    Create a signature for a geom or stat

    Gets the DEFAULT_PARAMS (params) and creates are comma
    separated list of the `name=value` pairs. The common_params
    come first in the list, and they get take their values from
    either the params-dict or the common_geom_param_values-dict.
    """
    pass


@lru_cache(maxsize=256)
def docstring_section_lines(docstring: str, section_name: str) -> str:
    """
    Return a section of a numpydoc string

    Parameters
    ----------
    docstring :
        Docstring
    section_name :
        Name of section to return

    Returns
    -------
    :
        Section minus the header
    """
    pass


def append_to_section(s: str, docstring: str, section: str) -> str:
    """
    Append string s to a section in the docstring
    """
    pass


def docstring_parameters_section(obj: Any) -> str:
    """
    Return the parameters section of a docstring
    """
    pass


def param_spec(line: str) -> str | None:
    """
    Identify and return parameter

    Parameters
    ----------
    line : str
        A line in the parameter section.

    Returns
    -------
    name : str | None
        Name of the parameter if the line for the parameter
        type specification and None otherwise.

    Examples
    --------
    >>> param_spec('line : str')
    breaks
    >>> param_spec("    A line in the parameter section.")
    """
    pass


def parameters_str_to_dict(param_section: str) -> dict[str, str]:
    """
    Convert a param section to a dict

    Parameters
    ----------
    param_section : str
        Text in the parameter section

    Returns
    -------
    d : dict
        Dictionary of the parameters in the order that they
        are described in the parameters section. The dict
        is of the form `{param: all_parameter_text}`.
        You can reconstruct the `param_section` from the
        keys of the dictionary.

    See Also
    --------
    plotnine.doctools.parameters_dict_to_str
    """
    pass


def parameters_dict_to_str(d: dict[str, str]) -> str:
    """
    Convert a dict of param section to a string

    Parameters
    ----------
    d : dict
        Parameters and their descriptions in a docstring

    Returns
    -------
    param_section : str
        Text in the parameter section

    See Also
    --------
    plotnine.doctools.parameters_str_to_dict
    """
    pass


def default_class_name(s: str | type | object) -> str:
    """
    Return the qualified name of s

    Only if s does not start with the prefix

    Examples
    --------
    >>> qualified_name('stat_bin')
    'stat_bin'
    >>> qualified_name(stat_bin)
    'stat_bin'
    >>> qualified_name(stat_bin())
    'stat_bin'
    """
    pass


def document_geom(geom: type[geom]) -> type[geom]:
    """
    Create a structured documentation for the geom

    It replaces `{usage}`, `{common_parameters}` and
    `{aesthetics}` with generated documentation.
    """
    pass


def document_stat(stat: type[stat]) -> type[stat]:
    """
    Create a structured documentation for the stat

    It replaces `{usage}`, `{common_parameters}` and
    `{aesthetics}` with generated documentation.
    """
    pass


DOC_FUNCTIONS = {
    "geom": document_geom,
    "stat": document_stat,
}


def document(cls: Type[T]) -> Type[T]:
    """
    Document a plotnine class

    To be used as a decorator
    """
    return cls
