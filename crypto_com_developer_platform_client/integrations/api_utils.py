import requests


def handle_api_error(response: requests.Response) -> None:
    """
    Handles API error responses by extracting error messages and raising exceptions.

    :param response: The HTTP response object from requests
    :raises Exception: Always raises an exception with the appropriate error message
    """
    try:
        error_body = response.json()
        server_error_message = (
            error_body.get("error") or f"HTTP error! status: {response.status_code}"
        )
    except ValueError:
        # Handle non-JSON error responses
        server_error_message = f"HTTP error! status: {response.status_code}"

    raise Exception(server_error_message)
