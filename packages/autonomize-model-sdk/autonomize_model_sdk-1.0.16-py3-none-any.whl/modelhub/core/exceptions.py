""" This module contains the ModelHubException class. """


class ModelHubException(Exception):
    """Exception raised for errors in the ModelHub client.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
