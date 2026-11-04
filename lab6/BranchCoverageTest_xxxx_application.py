"""Tests focused on exercising both outcomes of application decisions."""

import pytest
from pizza_order import pizza_price, order_discount, delivery_status


def test_pizza_size_valid_and_invalid_branches():
    assert pizza_price("medium", 0, False) == 350
    with pytest.raises(ValueError, match="unknown size"):
        pizza_price("extra-large", 0, False)


def test_topping_count_negative_and_nonnegative_branches():
    with pytest.raises(ValueError, match="invalid toppings"):
        pizza_price("large", -1, False)
    assert pizza_price("large", 0, False) == 500


def test_topping_count_up_to_three_and_above_three_branches():
    assert pizza_price("large", 3, False) == 620
    assert pizza_price("large", 4, False) == 650


def test_cheese_burst_branches():
    assert pizza_price("medium", 0, False) == 350
    assert pizza_price("medium", 0, True) == 450
    with pytest.raises(ValueError, match="cheese burst not available for small"):
        pizza_price("small", 0, True)


def test_order_total_threshold_branches():
    assert order_discount(299, "monday", False) == 0
    assert order_discount(300, "monday", False) == 30


def test_tuesday_weekend_and_other_weekday_branches():
    assert order_discount(500, "tuesday", False) == 250
    assert order_discount(500, "saturday", False) == 0
    assert order_discount(500, "sunday", False) == 0
    assert order_discount(500, "monday", False) == 50


def test_student_and_nonstudent_branches():
    assert order_discount(500, "monday", False) == 50
    assert order_discount(500, "monday", True) == 100


def test_delivery_distance_branches():
    assert delivery_status(20, 10) == "on time"
    assert delivery_status(20, 10.1) == "not deliverable"


def test_delivery_time_branches():
    assert delivery_status(30, 5) == "on time"
    assert delivery_status(31, 5) == "late"
    assert delivery_status(45, 5) == "late"
    assert delivery_status(46, 5) == "free pizza"
