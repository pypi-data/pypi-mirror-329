"""Custom Exceptions"""


class AuthenticationFailure(Exception):
    """Exception raised for errors in Autentication

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="AuthenticationFailure error"):
        self.message = message
        super().__init__(self.message)


class OptionsError(Exception):
    """Exception raised for errors in Options

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="OptionsError error"):
        self.message = message
        super().__init__(self.message)


class LookupError(Exception):
    """Exception raised for errors looking secrets

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="LookupError error"):
        self.message = message
        super().__init__(self.message)


class CreationError(Exception):
    """Exception raised when object was not created in API

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="CreationError error"):
        self.message = message
        super().__init__(self.message)


class DeletionError(Exception):
    """Exception raised when object was not deleted in API

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="DeletionError error"):
        self.message = message
        super().__init__(self.message)
