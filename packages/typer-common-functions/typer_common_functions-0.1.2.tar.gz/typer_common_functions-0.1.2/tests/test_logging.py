"""Tests for logging module."""

import logging

import pytest

from typer_common_functions.logging import set_logging


@pytest.fixture(autouse=True)
def reset_logging() -> None:
    """Reset root logger before each test."""
    root = logging.getLogger()
    root.handlers.clear()
    root.manager.loggerDict.clear()
    logging.basicConfig(level=logging.WARNING)  # Reset to default


def test_set_logging() -> None:
    """Test set_logging function."""
    # Test with default values (non-verbose)
    set_logging(verbose=False)
    assert logging.getLogger().level == logging.INFO

    # Test with verbose mode
    set_logging(verbose=True)
    assert logging.getLogger().level == logging.DEBUG
