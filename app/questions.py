REQUIRED_ATTRIBUTES = [
    "gill_color",
    "spore_print_color",
    "mushroom_population",
    "gill_size",
    "mushroom_odor",
    "mushroom_habitat",
    "bruising_present",
]

def get_next_question(provided_data):
    """Return the next question based on missing attributes."""
    for attr in REQUIRED_ATTRIBUTES:
        if attr not in provided_data or provided_data[attr] is None:
            return f"What is the {attr.replace('_', ' ')} of the mushroom?"
    return None
