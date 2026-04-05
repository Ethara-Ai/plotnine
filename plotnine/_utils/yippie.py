"""
Functions/class to quickly create plots for development and testing
"""

import pandas as pd

from plotnine import (
    aes,
    element_blank,
    element_rect,
    element_text,
    geom_col,
    geom_point,
    ggplot,
    labs,
    theme,
)

__all__ = ("geom", "legend", "plot", "rotate", "tag")


class _Plot:
    """
    Create a plot
    """

    def __getattr__(self, color: str):
        """
        Create a blank plot with given background color
        """
        return (
            ggplot()
            + labs(
                x="x-axis",
                y="y-axis",
                title=color.title(),
            )
            + theme(
                figure_size=(8, 6),
                text=element_text(color="black", size=11),
                panel_background=element_rect(fill=color, size=1),
                plot_background=element_rect(fill=color, alpha=0.2),
                panel_border=element_rect(color="black"),
                strip_background=element_rect(color="black"),
                panel_grid=element_blank(),
                legend_key_size=12,
            )
        )


class _Geom:
    """
    Create some simple geoms
    """

    data = pd.DataFrame(
        {
            "cat": ["a", "b", "c", "d"],
            "cat2": ["r", "r", "s", "s"],
            "value": [1, 2, 3, 4],
        }
    )

    @property
    def points(self):
        pass

    @property
    def cols(self):
        pass


class _Legend:
    """
    Position Legends
    """

    @property
    def left(self):
        pass

    @property
    def bottom(self):
        pass

    @property
    def right(self):
        pass

    @property
    def top(self):
        pass


class _Rotate:
    """
    Rotate a text themeable
    """

    def __getattr__(self, name):
        angle = 0 if name[-2:] == "_y" else 90
        return theme(**{name: element_text(angle=angle)})  # pyright: ignore[reportArgumentType]


def tag(s, position="topleft"):
    """
    Create a tag at a position
    """
    pass


plot = _Plot()
geom = _Geom()
legend = _Legend()
rotate = _Rotate()
