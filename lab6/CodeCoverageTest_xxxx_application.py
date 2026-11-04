"""Tests focused on executing application statements (line coverage)."""

import pytest
from pizza_order import pizza_price, order_discount, delivery_status


def test_pizza_price_normal_and_extra_toppings():
    assert pizza_price("small", 0, False) == 200
    assert pizza_price("medium", 2, False) == 430
    assert pizza_price("large", 5, False) == 680


def test_pizza_price_cheese_burst_and_errors():
    assert pizza_price("medium", 1, True) == 490
    with pytest.raises(ValueError, match="unknown size"):
        pizza_price("extra-large", 1, False)
    with pytest.raises(ValueError, match="invalid toppings"):
        pizza_price("large", -1, False)
    with pytest.raises(ValueError, match="cheese burst not available for small"):
        pizza_price("small", 0, True)


def test_order_discount_scenarios():
    assert order_discount(299, "monday", False) == 0
    assert order_discount(500, "tuesday", True) == 300
    assert order_discount(500, "saturday", False) == 0
    assert order_discount(500, "monday", False) == 50


def test_delivery_status_scenarios():
    assert delivery_status(20, 11) == "not deliverable"
    assert delivery_status(30, 5) == "on time"
    assert delivery_status(40, 5) == "late"
    assert delivery_status(50, 5) == "free pizza"
