import json
import os

import boto3
import polling2
from assertpy import assert_that


def get_step_function_arn():
    env = os.environ.get("ENV", "dev")
    ssm_c = boto3.client("ssm")
    return ssm_c.get_parameter(
        Name=f"/integration_tests/pretzel-{env}/hello_world_step_function_arn"
    )["Parameter"]["Value"]


def has_terminated(step_c, execution_arn):
    status = step_c.describe_execution(executionArn=execution_arn)["status"]
    return True if status != "RUNNING" else False


def test_that_hello_world_returns_message():
    step_function_arn = get_step_function_arn()
    step_c = boto3.client("stepfunctions")

    execution_arn = step_c.start_execution(
        stateMachineArn=step_function_arn,
        input=json.dumps({"name": "integration-testy-step"}),
    )["executionArn"]
    polling2.poll(lambda: has_terminated(step_c, execution_arn), step=2, timeout=10)

    last_event = step_c.get_execution_history(
        executionArn=execution_arn, reverseOrder=True
    )["events"][0]

    assert_that(last_event["type"]).is_equal_to("ExecutionSucceeded")
    assert_that(
        json.loads(last_event["executionSucceededEventDetails"]["output"])[
            "hello_message"
        ]["Payload"]
    ).contains("Hello", "integration-testy-step")


def test_that_hello_world_returns_error_when_no_name_given():
    step_function_arn = get_step_function_arn()
    step_c = boto3.client("stepfunctions")

    execution_arn = step_c.start_execution(
        stateMachineArn=step_function_arn, input=json.dumps({}),
    )["executionArn"]
    polling2.poll(lambda: has_terminated(step_c, execution_arn), step=2, timeout=10)

    last_event = step_c.get_execution_history(
        executionArn=execution_arn, reverseOrder=True
    )["events"][0]

    assert_that(last_event["type"]).is_equal_to("ExecutionSucceeded")
    payload = json.loads(last_event["executionSucceededEventDetails"]["output"])[
        "hello_message"
    ]["Payload"]
    assert_that(payload).is_equal_to(
        {"exception": "Caught KeyError with message: 'name'"}
    )
