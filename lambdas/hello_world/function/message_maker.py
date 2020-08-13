from datetime import datetime


def make_message(name: str) -> str:
    """
    Takes a name and returns a message with the name and the time
    :param name: str Which is the name for the message to refer to
    :returns: str The message containing the name and the time
    """
    time = datetime.now().strftime("%H:%M")
    return f"Hello {name}, the time is {time}, how are you today?"
