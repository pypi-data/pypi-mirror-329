

def build(params: dict) -> str:
    """
    Build an HTTP Query parameters string from dictionary.
    :param params: dictionary with all parameters key-value pairs
    :return: a query string
    """
    return f"{'&'.join([f'{str(key)}={str(params[key])}' for key in params.keys()])}"
