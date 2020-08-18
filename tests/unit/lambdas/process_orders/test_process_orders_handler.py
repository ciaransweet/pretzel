import json
import os
from unittest.mock import patch

import boto3
from assertpy import assert_that
from moto import mock_stepfunctions

import lambdas.process_orders.function.handler as handler

EXAMPLE_ORDERS_JSON_PATH = (
    f"{os.path.dirname(os.path.abspath(__file__))}/example_orders.json"
)


def create_step_function(sfn_c):
    step_function = sfn_c.create_state_machine(
        name="TestStepFunction",
        roleArn="arn:aws:iam::123456789012:role/TestRole",
        definition=json.dumps(
            {
                "StartAt": "Pass",
                "States": {"Pass": {"Type": "Pass", "Result": "World", "End": True}},
            }
        ),
    )
    return step_function["stateMachineArn"]


def test_that_no_orders_list_handled_correctly():
    with patch.dict(os.environ, {"PROCESS_ORDERS_STEP_FUNCTION_ARN": "blah"}):
        execution_arns = handler.handler({}, None)
        assert_that(execution_arns["exception"]).is_equal_to(
            "Caught NoOrdersListException with message: The 'orders' key was not found"
        )


def test_that_no_process_orders_function_arn_handled_correctly():
    execution_arns = handler.handler({}, None)
    assert_that(execution_arns["exception"]).is_equal_to(
        "Caught ProcessOrdersStepFunctionArnMissing with message: The Arn is missing"
    )


@mock_stepfunctions
def test_that_three_orders_returns_correct_execution_arns():
    sfn_c = boto3.client("stepfunctions", region_name="us-east-1")
    step_function_arn = create_step_function(sfn_c)
    with patch.dict(
        os.environ, {"PROCESS_ORDERS_STEP_FUNCTION_ARN": step_function_arn}
    ):
        with open(EXAMPLE_ORDERS_JSON_PATH, "r") as orders_in:
            orders = json.load(orders_in)
        execution_arns = handler.handler(orders, None)
        assert_that(len(execution_arns)).is_equal_to(3)
        for execution in execution_arns:
            assert_that(execution).contains(
                "arn:aws:states:us-east-1:123456789012:execution:TestStepFunction:"
            )


@mock_stepfunctions
def test_that_no_orders_in_list_returns_correct_execution_arns():
    sfn_c = boto3.client("stepfunctions", region_name="us-east-1")
    step_function_arn = create_step_function(sfn_c)
    with patch.dict(
        os.environ, {"PROCESS_ORDERS_STEP_FUNCTION_ARN": step_function_arn}
    ):
        execution_arns = handler.handler({"orders": []}, None)
        assert_that(len(execution_arns)).is_equal_to(0)
