from __future__ import annotations

import typing
from contextlib import suppress
from copy import copy

from .._utils import jitter, resolution
from ..exceptions import PlotnineError
from ..mapping.aes import SCALED_AESTHETICS
from .position import position
from .position_dodge import position_dodge

if typing.TYPE_CHECKING:
    from typing import Optional

    import numpy as np


# Adjust position by simultaneously dodging and jittering
class position_jitterdodge(position):
    """
    Dodge and jitter to minimise overlap

    Useful when aligning points generated through
    [](`~plotnine.geoms.geom_point`) with dodged a
    [](`~plotnine.geoms.geom_boxplot`).

    Parameters
    ----------
    jitter_width :
        Proportion to jitter in horizontal direction.
        If `None`, `0.4` of the resolution of the data.
    jitter_height :
        Proportion to jitter in vertical direction.
    dodge_width :
        Amount to dodge in horizontal direction.
    random_state :
        Seed or Random number generator to use. If `None`, then
        numpy global generator [](`numpy.random`) is used.
    """

    REQUIRED_AES = {"x", "y"}
    strategy = staticmethod(position_dodge.strategy)

    def __init__(
        self,
        jitter_width: Optional[float] = None,
        jitter_height: float = 0,
        dodge_width: float = 0.75,
        random_state: Optional[int | np.random.RandomState] = None,
    ):
        self.params = {
            "jitter_width": jitter_width,
            "jitter_height": jitter_height,
            "dodge_width": dodge_width,
            "random_state": random_state,
        }

    def setup_params(self, data):
        pass

    @classmethod
    def compute_panel(cls, data, scales, params):
        pass
