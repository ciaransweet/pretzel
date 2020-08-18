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


def execution_exists(execution_arn):
    sfn_c = boto3.client("stepfunctions")
    try:
        sfn_c.describe_execution(executionArn=execution_arn)
        return True
    except (sfn_c.exceptions.ExecutionDoesNotExist, sfn_c.exceptions.InvalidArn):
        return False


def test_that_process_orders_returns_execution_arns_and_they_exist():
    function_arn = get_function_arn()
    lambda_c = boto3.client("lambda")
    with open(EXAMPLE_ORDERS_JSON_PATH, "r") as orders_in:
        orders = json.load(orders_in)
    execution_arns = json.loads(
        lambda_c.invoke(
            FunctionName=function_arn,
            InvocationType="RequestResponse",
            Payload=json.dumps(orders),
        )["Payload"]
        .read()
        .decode("UTF-8")
    )
    assert_that(len(execution_arns)).is_equal_to(3)
    for execution_arn in execution_arns:
        assert_that(execution_arn).matches(
            r"arn:aws:states:.*?:\d+?:execution:ProcessOrder.*:.*"
        )
        assert_that(execution_exists(execution_arn)).is_true()
