from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from IPython.core.interactiveshell import InteractiveShell

    from ..typing import DisplayMetadata, FigureFormat, MimeBundle


def get_ipython() -> "None | InteractiveShell":
    """
    Return running IPython instance or None
    """
    pass


def is_inline_backend() -> bool:
    """
    Return True if the inline_backend is on

    This can only be True if also running in an jupyter/ipython session.
    """
    pass


def get_mimebundle(
    b: bytes, format: FigureFormat, figure_size_px: tuple[int, int]
) -> MimeBundle:
    """
    Return a the display MIME bundle from image data

    Parameters
    ----------
    format :
        The figure format
    figure_size_px :
        The figure size in pixels (width, height)
    """
    pass
