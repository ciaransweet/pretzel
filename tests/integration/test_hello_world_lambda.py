import json
import os

import boto3
from assertpy import assert_that


def get_function_arn():
    env = os.environ.get("ENV", "dev")
    ssm_c = boto3.client("ssm")
    return ssm_c.get_parameter(
        Name=f"/integration_tests/pretzel-{env}/hello_world_lambda_arn"
    )["Parameter"]["Value"]


def test_that_hello_world_returns_message():
    function_arn = get_function_arn()
    lambda_c = boto3.client("lambda")
    resp = (
        lambda_c.invoke(
            FunctionName=function_arn,
            InvocationType="RequestResponse",
            Payload=json.dumps({"name": "integration-testy"}),
        )["Payload"]
        .read()
        .decode("UTF-8")
    )
    assert_that(resp).contains("Hello", "integration-testy")


def test_that_hello_world_returns_exception_when_no_name():
    function_arn = get_function_arn()
    lambda_c = boto3.client("lambda")
    resp = json.loads(
        (
            lambda_c.invoke(
                FunctionName=function_arn,
                InvocationType="RequestResponse",
                Payload=json.dumps({}),
            )["Payload"]
            .read()
            .decode("UTF-8")
        )
    )
    assert_that(resp).is_equal_to({"exception": "Caught KeyError with message: 'name'"})
