"""Logging Related Functions."""

import logging

import click
from rich.logging import RichHandler
from rich.traceback import install as install_rich_traceback

from . import typer as typer_helpers

LOGGER = logging.getLogger(__name__)


def set_logging(verbose: bool = False) -> None:
    """Set the Logging Config according to passed arguments.

    parameters
    ----------
    verbose : bool
        wether to Log debug Messages
    """
    root = logging.getLogger()
    for handler in root.handlers[:]:
        root.removeHandler(handler)

    if verbose:
        install_rich_traceback(suppress=[click, typer_helpers])
        root.setLevel(logging.DEBUG)
        handler = RichHandler(
            level=logging.DEBUG,
            show_path=True,
            rich_tracebacks=True,
            tracebacks_show_locals=True,
        )
    else:
        root.setLevel(logging.INFO)
        handler = RichHandler(
            level=logging.INFO,
            show_path=False,
            rich_tracebacks=False,
        )

    handler.setFormatter(
        logging.Formatter(
            fmt="{name}: {message}" if verbose else "{message}",
            style="{",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    root.addHandler(handler)
