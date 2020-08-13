from unittest.mock import patch

from assertpy import assert_that
from freezegun import freeze_time

import lambdas.hello_world.function.handler as handler


@freeze_time("2020-01-01 12:00:00")
def test_that_message_returned_correctly():
    message = handler.handler({'name': 'test-name-from-handler'}, None)
    assert_that(message).is_equal_to(
        "Hello test-name-from-handler, the time is 12:00, how are you today?"
    )


@patch('lambdas.hello_world.function.handler.make_message')
def test_that_error_handled_correctly(mock_make_message):
    mock_make_message.side_effect = Exception('Im an exception')
    message = handler.handler({'name': 'test-name-from-handler'}, None)
    assert_that(message).is_equal_to({
        'exception': 'Im an exception'
    })
