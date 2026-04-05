from __future__ import annotations

import typing
from copy import deepcopy
from warnings import warn

import pandas as pd

from .._utils import (
    check_required_aesthetics,
    data_mapping_as_kwargs,
    groupby_apply,
    remove_missing,
    uniquecols,
)
from .._utils.registry import Register
from ..layer import layer
from ..mapping import aes

if typing.TYPE_CHECKING:
    from typing import Any

    from plotnine import ggplot
    from plotnine.facets.layout import Layout
    from plotnine.iapi import pos_scales
    from plotnine.mapping import Environment
    from plotnine.typing import DataLike

from abc import ABC

_BASE_PARAMS = {
    "geom": "blank",
    "position": "identity",
    "na_rm": False,
}

DROPPED_TPL = """
The following aesthetics were dropped during processing: {dropped}.
plotnine could not infer the correct grouping.
Did you forget to specify a `group` aesthetic or to convert a numerical \
variable into a categorial?
"""


class stat(ABC, metaclass=Register):
    """Base class of all stats"""

    DEFAULT_AES: dict[str, Any] = {}
    """Default aesthetics for the stat"""

    REQUIRED_AES: set[str] = set()
    """Required aesthetics for the stat"""

    NON_MISSING_AES: set[str] = set()
    """Required aesthetics for the stat"""

    DEFAULT_PARAMS: dict[str, Any] = {}
    """Required parameters for the stat"""

    CREATES: set[str] = set()
    """
    Stats may modify existing columns or create extra
    columns.

    Any extra columns that may be created by the stat
    should be specified in this set
    see: stat_bin

    Documentation for the aesthetics. It ie added under the
    documentation for mapping parameter. Use {aesthetics_table}
    placeholder to insert a table for all the aesthetics and
    their default values.
    """

    _aesthetics_doc = "{aesthetics_table}"

    # Plot namespace, it gets its value when the plot is being
    # built.
    environment: Environment

    def __init__(
        self,
        mapping: aes | None = None,
        data: DataLike | None = None,
        **kwargs: Any,
    ):
        possible_params = _BASE_PARAMS | self.DEFAULT_PARAMS
        possible_params_set = set(possible_params)
        kwargs = data_mapping_as_kwargs((data, mapping), kwargs)
        self._raw_kwargs = kwargs  # Will be used to create the geom
        self.params = possible_params | {
            k: v for k, v in kwargs.items() if k in possible_params_set
        }
        self.DEFAULT_AES = aes(**self.DEFAULT_AES)
        self.aes_params = {
            ae: kwargs[ae] for ae in self.aesthetics() & set(kwargs)
        }

    def __deepcopy__(self, memo: dict[Any, Any]) -> stat:
        """
        Deep copy without copying the self.data dataframe

        stats should not override this method.
        """
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        old = self.__dict__
        new = result.__dict__

        # don't make a _raw_kwargs
        shallow = {"_raw_kwargs"}
        for key, item in old.items():
            if key in shallow:
                new[key] = item  # pyright: ignore[reportIndexIssue]
                memo[id(new[key])] = new[key]
            else:
                new[key] = deepcopy(item, memo)  # pyright: ignore[reportIndexIssue]

        return result

    @classmethod
    def aesthetics(cls) -> set[str]:
        """
        Return a set of all non-computed aesthetics for this stat.

        stats should not override this method.
        """
        pass

    def use_defaults(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Combine data with defaults and set aesthetics from parameters

        stats should not override this method.

        Parameters
        ----------
        data :
            Data used for drawing the geom.

        Returns
        -------
        out :
            Data used for drawing the geom.
        """
        pass

    def setup_params(self, data: pd.DataFrame):
        """
        Override this to verify and/or adjust parameters

        Parameters
        ----------
        data :
            Data

        Returns
        -------
        out :
            Parameters used by the stats.
        """

    def setup_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Override to modify data before compute_layer is called

        Parameters
        ----------
        data :
            Data

        Returns
        -------
        out :
            Data
        """
        pass

    def finish_layer(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Modify data after the aesthetics have been mapped

        This can be used by stats that require access to the mapped
        values of the computed aesthetics, part 3 as shown below.

            1. stat computes and creates variables
            2. variables mapped to aesthetics
            3. stat sees and modifies data according to the
               aesthetic values

        The default to is to do nothing.

        Parameters
        ----------
        data :
            Data for the layer
        params :
            Parameters

        Returns
        -------
        data :
            Modified data
        """
        pass

    def compute_layer(
        self, data: pd.DataFrame, layout: Layout
    ) -> pd.DataFrame:
        """
        Calculate statistics for this layers

        This is the top-most computation method for the
        stat. It does not do any computations, but it
        knows how to verify the data, partition it call the
        next computation method and merge results.

        stats should not override this method.

        Parameters
        ----------
        data :
            Data points for all objects in a layer.
        layout :
            Panel layout information
        """
        pass

    def compute_panel(self, data: pd.DataFrame, scales: pos_scales):
        """
        Calculate the statistics for all the groups

        Return the results in a single dataframe.

        This is a default function that can be overridden
        by individual stats

        Parameters
        ----------
        data :
            data for the computing
        scales :
            x (``scales.x``) and y (``scales.y``) scale objects.
            The most likely reason to use scale information is
            to find out the physical size of a scale. e.g.

            ```python
            range_x = scales.x.dimension()
            ```
        params :
            The parameters for the stat. It includes default
            values if user did not set a particular parameter.
        """
        pass

    def compute_group(
        self, data: pd.DataFrame, scales: pos_scales
    ) -> pd.DataFrame:
        """
        Calculate statistics for the group

        All stats should implement this method

        Parameters
        ----------
        data :
            Data for a group
        scales :
            x (``scales.x``) and y (``scales.y``) scale objects.
            The most likely reason to use scale information is
            to find out the physical size of a scale. e.g.

            ```python
            range_x = scales.x.dimension()
            ```
        params :
            Parameters
        """
        pass

    def __radd__(self, other: ggplot) -> ggplot:
        """
        Add layer representing stat object on the right

        Parameters
        ----------
        gg :
            ggplot object

        Returns
        -------
        out :
            ggplot object with added layer
        """
        other += layer(stat=self)
        return other
