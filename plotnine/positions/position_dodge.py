from __future__ import annotations

import typing
from contextlib import suppress
from copy import copy

import numpy as np
import pandas as pd

from .._utils import groupby_apply, match
from ..exceptions import PlotnineError
from .position import position

if typing.TYPE_CHECKING:
    from typing import Literal, Optional


class position_dodge(position):
    """
    Dodge overlaps and place objects side-by-side

    Parameters
    ----------
    width :
        Dodging width, when different to the width of the
        individual elements. This is useful when you want
        to align narrow geoms with wider geoms
    preserve :
        Should dodging preserve the total width of all elements
        at a position, or the width of a single element?
    """

    REQUIRED_AES = {"x"}

    def __init__(
        self,
        width: Optional[float] = None,
        preserve: Literal["total", "single"] = "total",
    ):
        self.params = {
            "width": width,
            "preserve": preserve,
        }

    def setup_data(self, data, params):
        # # e.g. geom_segment should be dodgeable
        pass

    def setup_params(self, data):
        pass

    @classmethod
    def compute_panel(cls, data, scales, params):
        pass

    @staticmethod
    def strategy(data, params):
        """
        Dodge overlapping interval

        Assumes that each set has the same horizontal position.
        """
        pass
