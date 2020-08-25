from typing import Dict, List

decoration_descriptions = {
    "caramel_sauce": "a sweet, sticky caramel sauce",
    "chocolate_sauce": "a smooth, creamy chocolate sauce",
    "sprinkles": "a dashing of colourful sugar sprinkles",
    "sesame_seeds": "a sprinkling of crunchy sesame seeds",
    "salt": "a tickle of salt pieces",
    "honey": "a sticky drizzle of honey",
}


def _get_decoration_descriptions(order: Dict[str, str]) -> List[str]:
    """
    For a given order, return the textual description of the decorations
    :param order: Dict[str, str] representing an order
    :returns: List[str] a list containing the textual descriptions of decorations in an
    order, if there are decorations
    """
    if "pretzel_decorations" not in order.keys():
        return []
    decorations = [
        decoration_descriptions[decoration]
        for decoration in order["pretzel_decorations"]
    ]
    return decorations


def collect_decoration_descriptions(order: Dict[str, str]) -> str:
    """
    Collects the textual descriptions of decorations in an order, message differs
    whether the order contains decorations or not
    :param order: Dict[str, str] representing an order
    :returns: str a textual description of all of the decorations in an order, string
    returned depends on whether decorations are present or not
    """
    decorations = _get_decoration_descriptions(order)
    if len(decorations) < 3:
        decoration_description = (
            f"For your pretzels, you've chosen: {' and '.join(decorations)}."
        )
    else:
        decoration_description = (
            "For your pretzels, you've chosen:"
            f" {', '.join(decorations[:-1])}"
            f", and {decorations[-1]}."
        )
    return decoration_description
