"""Unit tests for the business logic (no HTTP)."""

import pytest

from app.logic import calculate_gross


def test_calculate_gross_standard_rate():
    assert calculate_gross(100, 23) == 123.0


def test_calculate_gross_zero_rate():
    assert calculate_gross(50, 0) == 50.0


def test_calculate_gross_rounds_to_cents():
    # 99.99 * 1.23 = 122.9877 -> 122.99
    assert calculate_gross(99.99, 23) == 122.99


def test_calculate_gross_negative_net_raises():
    with pytest.raises(ValueError):
        calculate_gross(-1, 23)
