def fill_missing_attributes(inputs, defaults):
    """Fill missing attributes with their default values."""
    return {key: inputs.get(key, defaults[key]) for key in defaults.keys()}
