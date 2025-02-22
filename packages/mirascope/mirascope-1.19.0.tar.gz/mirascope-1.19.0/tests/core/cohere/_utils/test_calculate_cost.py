"""Tests the `cohere._utils.calculate_cost` function."""

from mirascope.core.cohere._utils._calculate_cost import calculate_cost


def test_calculate_cost() -> None:
    """Tests the `calculate_cost` function."""
    assert calculate_cost(None, None, None, model="command-r-plus") is None
    assert calculate_cost(1, None, 1, model="unknown") is None
    assert calculate_cost(1, None, 1, model="command-r-plus") == 1.8e-05
