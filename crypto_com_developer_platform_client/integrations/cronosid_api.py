import requests

from ..constants import API_URL
from .api_interfaces import ApiResponse
from .api_utils import handle_api_error


def resolve_cronos_id(api_key: str, name: str) -> ApiResponse:
    """
    Resolve a Cronos ID name (e.g., 'test.cro') to its associated address.

    :param api_key: The API key for authentication.
    :param name: The Cronos ID name.
    :return: The associated address and resolution metadata.
    :rtype: ApiResponse
    :raises Exception: If the resolution fails or the server returns an error.
    """
    url = f"{API_URL}/cronosid/resolve/{name}"

    response = requests.get(
        url,
        headers={"Content-Type": "application/json", "x-api-key": api_key},
        timeout=15,
    )

    if response.status_code not in (200, 201):
        handle_api_error(response)

    return response.json()


def lookup_cronos_id(api_key: str, address: str) -> ApiResponse:
    """
    Lookup a Cronos ID by wallet address.

    :param api_key: The API key for authentication.
    :param address: The wallet address.
    :return: The Cronos ID associated with the address.
    :rtype: ApiResponse
    :raises Exception: If the lookup fails or the server returns an error.
    """
    url = f"{API_URL}/cronosid/lookup/{address}"

    response = requests.get(
        url,
        headers={"Content-Type": "application/json", "x-api-key": api_key},
        timeout=15,
    )

    if response.status_code not in (200, 201):
        handle_api_error(response)

    return response.json()
