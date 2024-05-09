class CustomException(Exception):
    """Base checked exception."""
    pass


class CustomException1(CustomException):
    """Example checked exception."""
    pass


class CustomException2(CustomException):
    """Another example checked exception."""
    pass


class CustomException3(CustomException):
    """Yet another example checked exception."""
    pass


class CustomException4(CustomException):
    """Checked exception again."""
    pass


class CustomException5(CustomException):
    """Last example checked exception."""
    pass


class UncheckedException(Exception):
    """Example unchecked exception."""
    pass
