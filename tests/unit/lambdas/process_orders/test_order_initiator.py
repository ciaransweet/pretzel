import json
import os

EXAMPLE_ORDERS_JSON_PATH = \
    f"{os.path.dirname(os.path.abspath(__file__))}/example_orders.json"


def test_that_order_initator_initiates_orders_correctly():
    with open(EXAMPLE_ORDERS_JSON_PATH, 'r') as orders_in:
        orders = json.load(orders_in)
    print(orders)
