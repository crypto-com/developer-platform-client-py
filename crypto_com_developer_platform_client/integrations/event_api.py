import requests
from ..constants import API_URL
from .api_interfaces import ApiResponse


def get_logs(api_key: str, address: str) -> ApiResponse:
    """
    Get the emitted events of a smart contract.

    :param api_key: The API key for authentication.
    :param address: The address of the smart contract.
    :return: A list of decoded contract events.
    :rtype: ApiResponse
    :raises Exception: If the event retrieval fails or the server responds with an error.
    """
    url = f"{API_URL}/events?address={address}"

    response = requests.get(
        url,
        headers={"Content-Type": "application/json", "x-api-key": api_key},
        timeout=15,
    )

    if response.status_code not in (200, 201):
        error_body = response.json()
        server_error_message = (
            error_body.get("error") or f"HTTP error! status: {response.status_code}"
        )
        raise Exception(server_error_message)

    return response.json()
