from hypothesis import given, strategies as st
from pizza_order import toppings_price, pizza_inches, split_bill


@given(st.text() | st.none())
def test_toppings_price_no_crash(s):
    try:
        toppings_price(s)
    except Exception as e:
        assert False, f"toppings_price crashed with: {e}"


@given(st.text() | st.none())
def test_pizza_inches_no_crash(s):
    try:
        pizza_inches(s)
    except Exception as e:
        assert False, f"pizza_inches crashed with: {e}"


@given(st.text() | st.none())
def test_split_bill_no_crash(s):
    try:
        split_bill(s)
    except Exception as e:
        assert False, f"split_bill crashed with: {e}"