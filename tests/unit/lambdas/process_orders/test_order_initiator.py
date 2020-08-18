import json
import os

import boto3
from assertpy import assert_that
from moto import mock_stepfunctions

import lambdas.process_orders.function.order_initiator as order_initiator

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


@mock_stepfunctions
def test_that_order_initator_initiates_orders_correctly():
    sfn_c = boto3.client("stepfunctions", region_name="us-east-1")
    step_function_arn = create_step_function(sfn_c)
    with open(EXAMPLE_ORDERS_JSON_PATH, "r") as orders_in:
        orders = json.load(orders_in)["orders"]
    execution_arns = order_initiator.initiate_orders(orders, step_function_arn)
    number_of_step_function_invocations = len(
        sfn_c.list_executions(stateMachineArn=step_function_arn)["executions"]
    )
    assert_that(number_of_step_function_invocations).is_equal_to(3)
    assert_that(len(execution_arns)).is_equal_to(3)
    for execution in execution_arns:
        assert_that(execution).contains(
            "arn:aws:states:us-east-1:123456789012:execution:TestStepFunction:"
        )
