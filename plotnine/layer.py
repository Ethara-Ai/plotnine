from __future__ import annotations

import typing
from copy import copy, deepcopy
from typing import Iterable, List, cast, overload

import pandas as pd

from ._utils import array_kind, check_required_aesthetics, ninteraction
from ._utils.registry import Registry
from .exceptions import PlotnineError
from .mapping.aes import NO_GROUP, SCALED_AESTHETICS, aes, make_labels
from .mapping.evaluation import evaluate, stage

if typing.TYPE_CHECKING:
    from typing import Any, Sequence, SupportsIndex

    from plotnine import ggplot
    from plotnine.coords.coord import coord
    from plotnine.facets.layout import Layout
    from plotnine.geoms.geom import geom
    from plotnine.layer import layer
    from plotnine.mapping import Environment
    from plotnine.positions.position import position
    from plotnine.scales.scales import Scales
    from plotnine.stats.stat import stat
    from plotnine.typing import (
        DataFrameConvertible,
        DataLike,
        LayerDataLike,
    )


class layer:
    """
    Layer

    When a `geom` or `stat` is added to a
    [](`~plotnine.ggplot`) object, it creates a single layer.
    This class is a representation of that layer.

    Parameters
    ----------
    geom :
        Geom used to draw this layer. Accepts an instance,
        a class, or a string name (e.g. ``"point"``).
    stat :
        Stat used for the statistical transformation of data
        in this layer. Accepts an instance, a class, or a
        string name. If ``None``, the geom's default stat is
        used.
    mapping :
        Aesthetic mappings.
    data :
        Data plotted in this layer. If `None`, the data from
        the [](`~plotnine.ggplot`) object will be used.
    position :
        Position adjustment for geometries in this layer.
        Accepts an instance, a class, or a string name. If
        ``None``, the geom's default position is used.
    inherit_aes :
        If `True` inherit from the aesthetic mappings of
        the [](`~plotnine.ggplot`) object.
    show_legend :
        Whether to make up and show a legend for the mappings
        of this layer. If `None` then an automatic/good choice
        is made.
    raster :
        If `True`, draw onto this layer a raster (bitmap)
        object even if the final image format is vector.
    **kwargs :
        Keyword arguments passed to the geom constructor when
        *geom* is a class or string.
    """

    # Data for this layer
    data: pd.DataFrame

    def __init__(
        self,
        geom: geom | type[geom] | str | None = None,
        stat: stat | type[stat] | str | None = None,
        *,
        mapping: aes | None = None,
        data: LayerDataLike | None = None,
        position: position | type[position] | str | None = None,
        inherit_aes: bool = True,
        show_legend: bool | dict[str, bool] | None = None,
        raster: bool = False,
        **kwargs: Any,
    ):
        # Stat-first: derive geom from stat's default
        if geom is None:
            if stat is not None:
                stat_ref = _lookup_stat(stat)
                if isinstance(stat_ref, type):
                    geom = stat_ref.DEFAULT_PARAMS["geom"]
                else:
                    geom = stat_ref.params["geom"]
                    # Forward stat instance's kwargs to the geom
                    if mapping is None and data is None and not kwargs:
                        mapping = stat_ref._raw_kwargs.get("mapping")
                        data = stat_ref._raw_kwargs.get("data")
                        kwargs = {
                            k: v
                            for k, v in stat_ref._raw_kwargs.items()
                            if k not in ("mapping", "data", "geom")
                        }
            else:
                # i.e. layer()
                geom = "blank"

        geom = cast("geom | type[geom] | str", geom)
        _geom = _resolve_geom(geom, mapping, data, kwargs)
        _stat = _resolve_stat(stat, _geom)
        _pos = _resolve_position(position, _geom)
        self._verify_arguments(_geom, _stat)

        # Layer params: prefer explicit kwargs, fall back to
        # geom._raw_kwargs, then geom.DEFAULT_PARAMS
        raw = _geom._raw_kwargs
        self.inherit_aes = raw.get(
            "inherit_aes",
            _geom.DEFAULT_PARAMS.get("inherit_aes", inherit_aes),
        )
        self.show_legend = raw.get(
            "show_legend",
            _geom.DEFAULT_PARAMS.get("show_legend", show_legend),
        )
        self.raster = raw.get(
            "raster",
            _geom.DEFAULT_PARAMS.get("raster", raster),
        )

        self.geom = _geom
        self.stat = _stat
        self._data = _geom.data
        self.mapping = _geom.mapping
        self.position = _pos
        self.zorder = 0

    @staticmethod
    def _verify_arguments(geom: geom, stat: stat) -> None:
        """
        Verify arguments for the geom, stat and layer
        """
        pass

    def __radd__(self, other: ggplot) -> ggplot:
        """
        Add layer to ggplot object
        """
        try:
            other.layers.append(self)
        except AttributeError as e:
            msg = f"Cannot add layer to object of type {type(other)!r}"
            raise PlotnineError(msg) from e
        return other

    def __deepcopy__(self, memo: dict[Any, Any]) -> layer:
        """
        Deep copy without copying the self.data dataframe
        """
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        old = self.__dict__
        new = result.__dict__

        for key, item in old.items():
            if key == "data":
                new[key] = item
            else:
                new[key] = deepcopy(item, memo)

        return result

    def setup(self, plot: ggplot):
        """
        Prepare layer for the plot building

        Give the layer access to the data, mapping and environment
        """
        pass

    def _make_layer_data(self, plot_data: DataLike | None):
        """
        Generate data to be used by this layer

        Parameters
        ----------
        plot_data :
            ggplot object data
        """
        pass

    def _make_layer_mapping(self, plot_mapping: aes):
        """
        Create the aesthetic mappings to be used by this layer

        Parameters
        ----------
        plot_mapping :
            ggplot object mapping
        """
        pass

    def _make_layer_environments(self, plot_environment: Environment):
        """
        Create the aesthetic mappings to be used by this layer

        Parameters
        ----------
        plot_environment :
            Namespace in which to execute aesthetic expressions.
        """
        pass

    def _share_layer_params(self):
        """
        Pass necessary layer parameters to the geom
        """
        pass

    def compute_aesthetics(self, plot: ggplot):
        """
        Return a dataframe where the columns match the aesthetic mappings

        Transformations like 'factor(cyl)' and other
        expression evaluation are  made in here
        """
        pass

    def compute_statistic(self, layout: Layout):
        """
        Compute & return statistics for this layer
        """
        pass

    def map_statistic(self, plot: ggplot):
        """
        Mapping aesthetics to computed statistics
        """
        pass

    def setup_data(self):
        """
        Prepare/modify data for plotting
        """
        pass

    def compute_position(self, layout: Layout):
        """
        Compute the position of each geometric object

        This is in concert with the other objects in the panel depending
        on the position class of the geom
        """
        pass

    def draw(self, layout: Layout, coord: coord):
        """
        Draw geom

        Parameters
        ----------
        layout : Layout
            Layout object created when the plot is getting
            built
        coord : coord
            Type of coordinate axes
        """
        pass

    def use_defaults(
        self,
        data: pd.DataFrame,
        aes_modifiers: dict[str, Any],
        scales: Scales | None = None,
    ) -> pd.DataFrame:
        """
        Prepare/modify data for plotting

        Parameters
        ----------
        data :
            Data
        aes_modifiers :
            Expression to evaluate and replace aesthetics in
            the data.
        """
        pass

    def finish_statistics(self):
        """
        Prepare/modify data for plotting
        """
        pass

    def update_labels(self, plot: ggplot):
        """
        Update label data for the ggplot from the mappings in this layer
        """
        pass


class Layers(List[layer]):
    """
    List of layers

    During the plot building pipeline, many operations are
    applied at all layers in the plot. This class makes those
    tasks easier.
    """

    @overload
    def __radd__(self, other: Iterable[layer]) -> Layers: ...

    @overload
    def __radd__(self, other: ggplot) -> ggplot: ...

    def __radd__(self, other: Iterable[layer] | ggplot) -> Layers | ggplot:
        """
        Add layers to ggplot object
        """
        # Add layers to ggplot object
        from .ggplot import ggplot

        if isinstance(other, ggplot):
            for obj in self:
                other += obj
        else:
            raise PlotnineError(
                f"Cannot add Layers to object of type {type(other)}"
            )
        return other

    @overload
    def __getitem__(self, key: SupportsIndex) -> layer: ...

    @overload
    def __getitem__(self, key: slice) -> Layers: ...

    def __getitem__(self, key: SupportsIndex | slice) -> layer | Layers:
        result = super().__getitem__(key)
        if isinstance(result, Iterable):
            result = Layers(result)
        return result

    @property
    def data(self) -> list[pd.DataFrame]:
        pass

    def setup(self, plot: ggplot):
        # If zorder is 0, it is left to MPL
        pass

    def setup_data(self):
        pass

    def draw(self, layout: Layout, coord: coord):
        pass

    def compute_aesthetics(self, plot: ggplot):
        pass

    def compute_statistic(self, layout: Layout):
        pass

    def map_statistic(self, plot: ggplot):
        pass

    def compute_position(self, layout: Layout):
        pass

    def use_defaults_after_scale(self, scales: Scales):
        pass

    def transform(self, scales: Scales):
        pass

    def train(self, scales: Scales):
        pass

    def map(self, scales: Scales):
        pass

    def finish_statistics(self):
        pass

    def update_labels(self, plot: ggplot):
        pass


def add_group(data: pd.DataFrame) -> pd.DataFrame:
    """
    Add group to the dataframe

    The group depends on the interaction of the discrete
    aesthetic columns in the dataframe.
    """
    pass


def discrete_columns(
    df: pd.DataFrame, ignore: Sequence[str] | pd.Index
) -> Sequence[str]:
    """
    Return a list of the discrete columns in the dataframe

    Parameters
    ----------
    df :
        Data
    ignore :
        A list|set|tuple with the names of the columns to skip.
    """
    pass


def _resolve_geom(
    geom_spec: geom | type[geom] | str,
    mapping: aes | None,
    data: LayerDataLike | None,
    kwargs: dict[str, Any],
) -> geom:
    """
    Resolve a geom specification to an instantiated geom

    Parameters
    ----------
    geom_spec :
        A geom instance, class, or string name.
    mapping :
        Aesthetic mappings.
    data :
        Layer data.
    kwargs :
        Additional keyword arguments forwarded to the geom
        constructor.
    """
    pass


def _lookup_stat(
    stat_spec: stat | type[stat] | str,
) -> stat | type[stat]:
    """
    Look up a stat specification without instantiation

    Parameters
    ----------
    stat_spec :
        A stat instance, class, or string name.

    Returns
    -------
    :
        The stat instance or class.
    """
    pass


def _resolve_stat(
    stat_spec: stat | type[stat] | str | None,
    geom_obj: geom,
) -> stat:
    """
    Resolve a stat specification to an instantiated stat

    Parameters
    ----------
    stat_spec :
        A stat instance, class, string name, or None to use
        the geom's default.
    geom_obj :
        The resolved geom (used to derive defaults).
    """
    pass


def _resolve_position(
    position_spec: position | type[position] | str | None,
    geom_obj: geom,
) -> position:
    """
    Resolve a position specification to an instantiated position

    Parameters
    ----------
    position_spec :
        A position instance, class, string name, or None to use
        the geom's default.
    geom_obj :
        The resolved geom (used to derive defaults).
    """
    pass
