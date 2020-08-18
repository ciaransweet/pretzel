import json
from typing import Dict, List

import boto3


def initiate_orders(
    orders: List[Dict], process_order_step_function_arn: str
) -> List[str]:
    """
    Takes a list of orders and invokes a Step Function to create each order within
    the 'orders' field
    :param orders: List[Dict] object representing one or more orders for Pretzels
    :param process_order_step_function_arn: str representing the ARN for the
        process_order Step Function
    :returns: List[str] list of the executions that have been initiated
    """
    sfn_c = boto3.client("stepfunctions")
    executions = []
    for order in orders:
        execution_arn = sfn_c.start_execution(
            stateMachineArn=process_order_step_function_arn, input=json.dumps(order)
        )["executionArn"]
        executions.append(execution_arn)
    return executions
