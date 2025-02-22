""" This module contains utility functions for the modelhub package. """

import requests

from ..utils import setup_logger

logger = setup_logger(__name__)


def handle_response(response):
    """
    Handles the response from an HTTP request.

    Args:
        response (requests.Response): The response object from the HTTP request.

    Returns:
        dict: The JSON response from the HTTP request.

    Raises:
        requests.exceptions.HTTPError: If the HTTP response status code is an error.
        requests.exceptions.RequestException: If there is an error with the request.
        ValueError: If the response is not a valid JSON.

    """
    try:
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error("HTTP error: %s", e.response.text)
        raise
    except requests.exceptions.RequestException as e:
        logger.error("Request error: %s", str(e))
        raise
    except ValueError as e:
        logger.error("Invalid JSON response: %s", str(e))
        raise
