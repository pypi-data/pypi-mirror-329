 # Global variable to hold the configuration
_config = None

def set_config(config):
    """
    Set the configuration.

    Args:
        config (dict): The configuration dictionary to set.
    """
    global _config
    _config = config

def get_config():
    """
    Get the configuration.

    Returns:
        dict: The configuration dictionary.
    """
    global _config
    return _config