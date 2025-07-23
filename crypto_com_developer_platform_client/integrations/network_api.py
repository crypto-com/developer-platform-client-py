import requests

from ..constants import API_URL
from .api_interfaces import ApiResponse
from .api_utils import handle_api_error


def get_network_info(api_key: str) -> ApiResponse:
    """
    Fetch general network information.

    :param api_key: The API key for authentication.
    :return: The network information.
    :rtype: ApiResponse
    :raises Exception: If the request fails or the server returns an error.
    """
    url = f"{API_URL}/network/info"

    response = requests.get(
        url,
        headers={"Content-Type": "application/json", "x-api-key": api_key},
        timeout=15,
    )

    if response.status_code not in (200, 201):
        handle_api_error(response)

    return response.json()


def get_chain_id(api_key: str) -> ApiResponse:
    """
    Fetch the network's chain ID.

    :param api_key: The API key for authentication.
    :return: The chain ID of the network.
    :rtype: ApiResponse
    :raises Exception: If the request fails or the server returns an error.
    """
    url = f"{API_URL}/network/chain-id"

    response = requests.get(
        url,
        headers={"Content-Type": "application/json", "x-api-key": api_key},
        timeout=15,
    )

    if response.status_code not in (200, 201):
        handle_api_error(response)

    return response.json()


def get_client_version(api_key: str) -> ApiResponse:
    """
    Fetch the client version of the connected node.

    :param api_key: The API key for authentication.
    :return: The client version string.
    :rtype: ApiResponse
    :raises Exception: If the request fails or the server returns an error.
    """
    url = f"{API_URL}/network/client-version"
    response = requests.get(
        url,
        headers={"Content-Type": "application/json", "x-api-key": api_key},
        timeout=15,
    )

    if response.status_code not in (200, 201):
        handle_api_error(response)

    return response.json()
