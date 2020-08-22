from typing import Dict, List

decoration_descriptions = {
    "caramel_sauce": "a sweet, sticky caramel sauce",
    "chocolate_sauce": "a smooth, creamy chocolate sauce",
    "sprinkles": "a dashing of colourful sugar sprinkles",
    "sesame_seeds": "a sprinkling of crunchy sesame seeds",
    "salt": "a tickle of salt pieces",
    "honey": "a sticky drizzle of honey",
}


def collect_decorations(order: Dict[str, str]) -> List[str]:
    if "pretzel_decorations" not in order.keys():
        return []
    decorations = [
        decoration_descriptions[decoration]
        for decoration in order["pretzel_decorations"]
    ]
    return decorations
