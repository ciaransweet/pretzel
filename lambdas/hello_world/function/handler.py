import logging

from .message_maker import make_message

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def handler(event, context):
    LOGGER.info(event)
    try:
        name = event["name"]
        return make_message(name)
    except Exception as e:
        err_message = f"Caught {type(e).__name__} with message: {str(e)}"
        LOGGER.error(err_message)
        return {"exception": err_message}
