class KikError(Exception):
    """
    Exception raised by all API errors.
    The exception message is set to the server's response.
    """
    pass
