from .message_maker import make_message


def handler(event, context):
    try:
        name = event['name']
        return make_message(name)
    except Exception as e:
        return {'exception': str(e)}
