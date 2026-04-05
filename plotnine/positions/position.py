from __future__ import annotations

import typing
from abc import ABC
from copy import copy
from warnings import warn

import numpy as np

from .._utils import check_required_aesthetics, groupby_apply
from .._utils.registry import Register
from ..exceptions import PlotnineError, PlotnineWarning
from ..mapping.aes import X_AESTHETICS, Y_AESTHETICS

if typing.TYPE_CHECKING:
    from typing import Any, Optional

    import pandas as pd

    from plotnine.facets.layout import Layout
    from plotnine.iapi import pos_scales
    from plotnine.typing import TransformCol


class position(ABC, metaclass=Register):
    """Base class for all positions"""

    REQUIRED_AES: set[str] = set()
    """
    Aesthetics required for the positioning
    """
    params: dict[str, Any]

    def __init__(self):
        self.params = {}

    def setup_params(self, data: pd.DataFrame) -> dict[str, Any]:
        """
        Verify, modify & return a copy of the params.
        """
        pass

    def setup_data(
        self, data: pd.DataFrame, params: dict[str, Any]
    ) -> pd.DataFrame:
        """
        Verify & return data
        """
        pass

    @classmethod
    def compute_layer(
        cls, data: pd.DataFrame, params: dict[str, Any], layout: Layout
    ):
        """
        Compute position for the layer in all panels

        Positions can override this function instead of
        `compute_panel` if the position computations are
        independent of the panel. i.e when not colliding
        """
        pass

    @classmethod
    def compute_panel(
        cls, data: pd.DataFrame, scales: pos_scales, params: dict[str, Any]
    ) -> pd.DataFrame:
        """
        Positions must override this function

        Notes
        -----
        Make necessary adjustments to the columns in the dataframe.

        Create the position transformation functions and
        use self.transform_position() do the rest.

        See Also
        --------
        plotnine.position_jitter.compute_panel
        """
        pass

    @staticmethod
    def transform_position(
        data,
        trans_x: Optional[TransformCol] = None,
        trans_y: Optional[TransformCol] = None,
    ) -> pd.DataFrame:
        """
        Transform all the variables that map onto the x and y scales.

        Parameters
        ----------
        data : dataframe
            Data to transform
        trans_x : callable
            Transforms x scale mappings
            Takes one argument, either a scalar or an array-type
        trans_y : callable
            Transforms y scale mappings
            Takes one argument, either a scalar or an array-type
        """
        pass

    @staticmethod
    def strategy(data: pd.DataFrame, params: dict[str, Any]) -> pd.DataFrame:
        """
        Calculate boundaries of geometry object
        """
        pass

    @classmethod
    def _collide_setup(cls, data, params):
        pass

    @classmethod
    def collide(cls, data, params):
        """
        Calculate boundaries of geometry object

        Uses Strategy
        """
        pass

    @classmethod
    def collide2(cls, data, params):
        """
        Calculate boundaries of geometry object

        Uses Strategy
        """
        pass


transform_position = position.transform_position
