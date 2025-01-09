import requests

from ..constants import API_URL
from .api_interfaces import ApiResponse


def resolve_name(chain_id: str, name: str) -> ApiResponse:
    """
    Resolves a CronosId to its corresponding blockchain address.

    :param chain_id: The ID of the blockchain network
    :param name: The CronosId to resolve
    :return: Response containing the resolved blockchain address
    :raises Exception: If the API request fails or returns an error
    """
    url = f"{API_URL}/cronosid/resolve/{name}?chainId={chain_id}"

    try:
        response = requests.get(
            url, headers={"Content-Type": "application/json"}, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        error_message = str(e)
        if hasattr(e, 'response') and e.response is not None:
            if e.response.status_code not in (200, 201):
                error_body = e.response.json()
                error_message = error_body.get('error') or f"HTTP error! status: {
                    e.response.status_code}"
        raise Exception(f"Failed to resolve name: {error_message}")


def lookup_address(chain_id: str, address: str) -> ApiResponse:
    """
    Looks up an address to find its associated CronosId.

    :param chain_id: The ID of the blockchain network
    :param address: The blockchain address to lookup
    :return: Response containing the CronosId name
    :raises Exception: If the API request fails or returns an error
    """
    url = f"{API_URL}/cronosid/lookup/{address}?chainId={chain_id}"

    try:
        response = requests.get(
            url, headers={"Content-Type": "application/json"}, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        error_message = str(e)
        if hasattr(e, 'response') and e.response is not None:
            if e.response.status_code not in (200, 201):
                error_body = e.response.json()
                error_message = error_body.get('error') or f"HTTP error! status: {
                    e.response.status_code}"
        raise Exception(f"Failed to lookup address: {error_message}")
