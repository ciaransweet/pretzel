import json
import os

import boto3
from assertpy import assert_that

EXAMPLE_ORDERS_JSON_PATH = (
    f"{os.path.dirname(os.path.abspath(__file__))}/example_orders.json"
)


def get_function_arn():
    env = os.environ.get("ENV", "dev")
    ssm_c = boto3.client("ssm")
    return ssm_c.get_parameter(
        Name=f"/integration_tests/pretzel-{env}/process_orders_lambda_arn"
    )["Parameter"]["Value"]


def test_that_process_orders_returns_execution_arns():
    function_arn = get_function_arn()
    lambda_c = boto3.client("lambda")
    with open(EXAMPLE_ORDERS_JSON_PATH, "r") as orders_in:
        orders = json.load(orders_in)
    resp = json.loads(
        lambda_c.invoke(
            FunctionName=function_arn,
            InvocationType="RequestResponse",
            Payload=json.dumps(orders),
        )["Payload"]
        .read()
        .decode("UTF-8")
    )
    assert_that(len(resp)).is_equal_to(3)
