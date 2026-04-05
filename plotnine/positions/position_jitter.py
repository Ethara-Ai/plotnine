from __future__ import annotations

import typing
from copy import deepcopy

import numpy as np

from .._utils import jitter, resolution
from .position import position

if typing.TYPE_CHECKING:
    from typing import Optional

    from plotnine.typing import FloatArray, FloatArrayLike


class position_jitter(position):
    """
    Jitter points to avoid overplotting

    Parameters
    ----------
    width :
        Proportion to jitter in horizontal direction.
        If `None`, `0.4` of the resolution of the data.
    height :
        Proportion to jitter in vertical direction.
        If `None`, `0.4` of the resolution of the data.
    random_state :
        Seed or Random number generator to use. If `None`, then
        numpy global generator [](`numpy.random`) is used.
    """

    REQUIRED_AES = {"x", "y"}

    def __init__(
        self,
        width: Optional[float] = None,
        height: Optional[float] = None,
        random_state: Optional[int | np.random.RandomState] = None,
    ):
        self.params = {
            "width": width,
            "height": height,
            "random_state": random_state,
        }

    def setup_params(self, data):
        pass

    @classmethod
    def compute_layer(cls, data, params, layout):
        pass
