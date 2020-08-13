import logging

from .message_maker import make_message


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def handler(event, context):
    LOGGER.info(event)
    try:
        name = event['name']
        return make_message(name)
    except Exception as e:
        LOGGER.error(str(e))
        return {'exception': str(e)}
