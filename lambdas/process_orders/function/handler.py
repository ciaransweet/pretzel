import logging
import os

from .exceptions import NoOrdersListException, ProcessOrdersStepFunctionArnMissing
from .order_initiator import initiate_orders

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def handler(event, context):
    try:
        process_orders_step_function_arn = os.environ.get(
            "PROCESS_ORDERS_STEP_FUNCTION_ARN", None
        )
        if process_orders_step_function_arn is None:
            raise ProcessOrdersStepFunctionArnMissing("The Arn is missing")

        orders = event.get("orders", None)
        if orders is None:
            raise NoOrdersListException("The 'orders' key was not found")

        return initiate_orders(orders, process_orders_step_function_arn)
    except Exception as e:
        err_message = f"Caught {type(e).__name__} with message: {str(e)}"
        LOGGER.error(err_message)
        return {"exception": err_message}
