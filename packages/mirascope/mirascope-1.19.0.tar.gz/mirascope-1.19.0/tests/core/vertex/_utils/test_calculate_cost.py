"""Tests the `vertex._utils.calculate_cost` function."""

import pytest

from mirascope.core.vertex._utils._calculate_cost import calculate_cost


def test_calculate_cost() -> None:
    """Tests the `calculate_cost` function for Vertex AI Gemini models."""
    # Test None inputs
    assert calculate_cost(None, None, None, model="gemini-1.5-pro") is None

    # Test unknown model
    assert calculate_cost(1, None, 1, model="unknown") is None

    # Test normal cases with short context
    assert calculate_cost(
        1000, None, 1000, model="gemini-1.5-flash", context_length=100000
    ) == pytest.approx(0.00009375)
    assert calculate_cost(
        1000, None, 1000, model="gemini-1.5-pro", context_length=100000
    ) == pytest.approx(0.005)
    assert calculate_cost(
        1000, None, 1000, model="gemini-1.0-pro", context_length=100000
    ) == pytest.approx(0.0005)

    # Test long context cases
    assert calculate_cost(
        1000, None, 1000, model="gemini-1.5-flash", context_length=150000
    ) == pytest.approx(0.0001875)
    assert calculate_cost(
        1000, None, 1000, model="gemini-1.5-pro", context_length=150000
    ) == pytest.approx(0.01)

    # Test Gemini 1.0 Pro with long context (should return None)
    assert (
        calculate_cost(1000, None, 1000, model="gemini-1.0-pro", context_length=150000)
        is None
    )

    # Test zero input
    assert calculate_cost(0, None, 0, model="gemini-1.5-pro") == 0

    # Test very large input
    large_input = 1_000_000  # 1 million characters
    assert calculate_cost(
        large_input, None, large_input, model="gemini-1.5-pro"
    ) == pytest.approx(5)

    # Test fractional input
    assert calculate_cost(500.5, None, 500.5, model="gemini-1.5-pro") == pytest.approx(
        0.0025025
    )


def test_calculate_cost_edge_cases() -> None:
    """Tests edge cases for the `calculate_cost` function."""

    # Test exactly 128K context boundary
    assert calculate_cost(
        1000, None, 1000, model="gemini-1.5-pro", context_length=128000
    ) == pytest.approx(0.005)
    assert calculate_cost(
        1000, None, 1000, model="gemini-1.5-pro", context_length=128001
    ) == pytest.approx(0.01)
