import json
import os

from assertpy import assert_that

from lambdas.collect_decorations.function.decorations_collector import (
    collect_decorations,
)

EXAMPLE_ORDER_JSON_PATH = (
    f"{os.path.dirname(os.path.abspath(__file__))}/example_order.json"
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
    with open(EXAMPLE_ORDER_JSON_PATH, "r") as order_in:
        order_json = json.load(order_in)
    decorations = collect_decorations(order_json)
    assert_that(decorations).contains_only(*expected_decorations)


def test_that_no_decorations_returns_empty_list():
    decorations = collect_decorations({"pretzel_decorations": []})
    assert_that(decorations).is_empty()
    decorations = collect_decorations({})
    assert_that(decorations).is_empty()
