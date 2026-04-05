from __future__ import annotations

from warnings import warn

import numpy as np
import pandas as pd

from .._utils import remove_missing
from ..exceptions import PlotnineWarning
from .position import position


class position_stack(position):
    """
    Stack plotted objects on top of each other

    The objects to stack are those that have
    an overlapping x range.

    Parameters
    ----------
    vjust :
        By what fraction to avoid overlapping the lower object,
        where `0` gives a complete overlap and `1` gives no overlap.
    reverse :
        Reverse the order of the stacked groups if true.
    """

    fill = False

    def __init__(self, vjust: float = 1, reverse: bool = False):
        self.params = {"vjust": vjust, "reverse": reverse}

    def setup_params(self, data):
        """
        Verify, modify & return a copy of the params.
        """
        pass

    def setup_data(self, data, params):
        pass

    @classmethod
    def compute_panel(cls, data, scales, params):
        pass

    @staticmethod
    def strategy(data, params):
        """
        Stack overlapping intervals.

        Assumes that each set has the same horizontal position
        """
        pass
