from __future__ import annotations

import typing
from copy import copy

import numpy as np
import pandas as pd

from .._utils import groupby_apply, pivot_apply
from ..exceptions import PlotnineError
from .position_dodge import position_dodge

if typing.TYPE_CHECKING:
    from typing import Literal, Optional

    from plotnine.typing import IntArray


class position_dodge2(position_dodge):
    """
    Dodge overlaps and place objects side-by-side

    This is an enhanced version of
    [](`~plotnine.positions.position_dodge`) that can deal
    with rectangular overlaps that do not share a lower x border.

    Parameters
    ----------
    width :
        Dodging width, when different to the width of the
        individual elements. This is useful when you want
        to align narrow geoms with wider geoms
    preserve :
        Should dodging preserve the total width of all elements
        at a position, or the width of a single element?
    padding :
        Padding between elements at the same position.
        Elements are shrunk by this proportion to allow space
        between them.
    reverse :
        Reverse the default ordering of the groups. This is
        useful if you're rotating both the plot and legend.
    """

    REQUIRED_AES = {"x"}

    def __init__(
        self,
        width: Optional[float] = None,
        preserve: Literal["total", "single"] = "total",
        padding: float = 0.1,
        reverse: bool = False,
    ):
        self.params = {
            "width": width,
            "preserve": preserve,
            "padding": padding,
            "reverse": reverse,
        }

    def setup_params(self, data):
        pass

    @classmethod
    def compute_panel(cls, data, scales, params):
        pass

    @staticmethod
    def strategy(data, params):
        pass


def find_x_overlaps(df: pd.DataFrame) -> IntArray:
    """
    Find overlapping regions along the x axis
    """
    pass
