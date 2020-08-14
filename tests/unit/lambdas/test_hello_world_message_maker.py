from assertpy import assert_that
from freezegun import freeze_time

import lambdas.hello_world.function.message_maker as message_maker


@freeze_time("2020-01-01 11:39:00")
def test_that_correct_message_returned():
    message = message_maker.make_message("test-name")
    assert_that(message).is_equal_to(
        "Hello test-name, the time is 11:39, how are you today?"
    )
