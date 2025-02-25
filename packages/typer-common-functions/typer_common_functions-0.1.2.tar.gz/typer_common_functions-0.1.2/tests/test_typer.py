"""Tests for typer module."""

from typing import Tuple

import typer

from typer_common_functions.typer import typer_retuner, typer_unpacker


def test_typer_retuner() -> None:
    """Test typer_retuner function."""
    # Test with non-integer return
    assert typer_retuner("test") == "test"
    assert typer_retuner(None) is None

    # Test with integer return (should not raise typer.Exit since we're not in a CLI context)
    assert typer_retuner(0) == 0
    assert typer_retuner(1) == 1


def test_typer_unpacker() -> None:
    """Test typer_unpacker function."""

    def test_func(
        required: str,
        optional: str = typer.Option("default"),
        flag: bool = typer.Option(False),
    ) -> Tuple[str, str, bool]:
        return required, optional, flag

    wrapped_func = typer_unpacker(test_func)

    # Test with all arguments provided
    result = wrapped_func("value", optional="custom", flag=True)
    assert result == ("value", "custom", True)

    # Test with only required argument
    result = wrapped_func("value")
    assert result == ("value", "default", False)
