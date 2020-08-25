import json
import os

from assertpy import assert_that

from lambdas.collect_decorations.function.decorations_collector import (
    _get_decoration_descriptions,
    collect_decoration_descriptions,
)

EXAMPLE_FULL_ORDER_JSON_PATH = (
    f"{os.path.dirname(os.path.abspath(__file__))}/full_example_order.json"
)
EXAMPLE_PARTIAL_ORDER_JSON_PATH = (
    f"{os.path.dirname(os.path.abspath(__file__))}/partial_example_order.json"
)


def test_that_decorations_descriptions_returned_correctly():
    expected_decorations = [
        "a sweet, sticky caramel sauce",
        "a smooth, creamy chocolate sauce",
        "a dashing of colourful sugar sprinkles",
        "a sprinkling of crunchy sesame seeds",
        "a tickle of salt pieces",
        "a sticky drizzle of honey",
    ]
    with open(EXAMPLE_FULL_ORDER_JSON_PATH, "r") as order_in:
        order_json = json.load(order_in)
    decorations = _get_decoration_descriptions(order_json)
    assert_that(decorations).contains_only(*expected_decorations)


def test_that_no_decorations_returns_empty_list():
    decorations = _get_decoration_descriptions({"pretzel_decorations": []})
    assert_that(decorations).is_empty()
    decorations = _get_decoration_descriptions({})
    assert_that(decorations).is_empty()


def test_that_less_than_three_decorations_returns_correct_description():
    expected_description = (
        "For your pretzels, you've chosen: a sweet, sticky caramel"
        " sauce and a smooth, creamy chocolate sauce."
    )
    with open(EXAMPLE_PARTIAL_ORDER_JSON_PATH, "r") as order_in:
        order_json = json.load(order_in)
    description = collect_decoration_descriptions(order_json)
    assert_that(description).is_equal_to(expected_description)


def test_that_decorations_returns_correct_description():
    expected_description = (
        "For your pretzels, you've chosen: a sweet, sticky caramel sauce, "
        "a smooth, creamy chocolate sauce, "
        "a dashing of colourful sugar sprinkles, "
        "a sprinkling of crunchy sesame seeds, "
        "a tickle of salt pieces, and "
        "a sticky drizzle of honey."
    )
    with open(EXAMPLE_FULL_ORDER_JSON_PATH, "r") as order_in:
        order_json = json.load(order_in)
    description = collect_decoration_descriptions(order_json)
    assert_that(description).is_equal_to(expected_description)
