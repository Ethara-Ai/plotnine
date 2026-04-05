from __future__ import annotations

import typing
from copy import deepcopy

from matplotlib.animation import ArtistAnimation

from .exceptions import PlotnineError

if typing.TYPE_CHECKING:
    from typing import Iterable

    from matplotlib.artist import Artist
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure

    from plotnine import ggplot
    from plotnine.scales.scale import scale

__all__ = ("PlotnineAnimation",)


class PlotnineAnimation(ArtistAnimation):
    """
    Animation using ggplot objects

    Parameters
    ----------
    plots :
        ggplot objects that make up the the frames of the animation
    interval : int
        Delay between frames in milliseconds. Defaults to 200.
    repeat_delay : int
        If the animation in repeated, adds a delay in milliseconds
        before repeating the animation. Defaults to `None`.
    repeat : bool
        Controls whether the animation should repeat when the sequence
        of frames is completed. Defaults to `True`.
    blit : bool
        Controls whether blitting is used to optimize drawing. Defaults
        to `False`.

    Notes
    -----
    1. The plots should have the same `facet` and
       the facet should not have fixed x and y scales.
    2. The scales of all the plots should have the same limits. It is
       a good idea to create a scale (with limits) for each aesthetic
       and add them to all the plots.
    """

    def __init__(
        self,
        plots: Iterable[ggplot],
        interval: int = 200,
        repeat_delay: int | None = None,
        repeat: bool = True,
        blit: bool = False,
    ):
        figure, artists = self._draw_plots(plots)
        ArtistAnimation.__init__(
            self,
            figure,
            artists,
            interval=interval,
            repeat_delay=repeat_delay,
            repeat=repeat,
            blit=blit,
        )

    def _draw_plots(
        self, plots: Iterable[ggplot]
    ) -> tuple[Figure, list[list[Artist]]]:
        """
        Plot and return the figure and artists

        Parameters
        ----------
        plots : iterable
            ggplot objects that make up the the frames of the animation

        Returns
        -------
        figure
            Matplotlib figure
        artists
            List of [](`Matplotlib.artist.Artist`)
        """
        pass

    def _draw_animation_plot(self, plot: ggplot, first_plot: ggplot) -> ggplot:
        """
        Draw a plot/frame of the animation

        This methods draws plots from the 2nd onwards
        """
        pass
