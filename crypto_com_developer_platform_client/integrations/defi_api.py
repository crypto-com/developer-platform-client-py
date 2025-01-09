import requests

from ..constants import API_URL
from .api_interfaces import ApiResponse


def get_whitelisted_tokens(project: str, api_key: str) -> ApiResponse:
    """
    Get whitelisted tokens for a specific DeFi project.

    :param project: The DeFi project name
    :param api_key: The API key for authentication
    :return: List of whitelisted tokens
    :raises Exception: If the request fails or server responds with an error
    """
    url = f"{API_URL}/defi/whitelisted-tokens/{project}?apiKey={api_key}"

    try:
        response = requests.get(
            url, headers={'Content-Type': 'application/json'}, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        error_message = str(e)
        if hasattr(e, 'response') and e.response is not None:
            if e.response.status_code not in (200, 201):
                error_body = e.response.json()
                error_message = error_body.get('error') or f"HTTP error! status: {
                    e.response.status_code}"
        raise Exception(f"Failed to get whitelisted tokens: {error_message}")


def get_all_farms(project: str, api_key: str) -> ApiResponse:
    """
    Get all farms for a specific DeFi project.

    :param project: The DeFi project name
    :param api_key: The API key for authentication
    :return: List of all farms
    :raises Exception: If the request fails or server responds with an error
    """
    url = f"{API_URL}/defi/farms/{project}?apiKey={api_key}"

    try:
        response = requests.get(
            url, headers={'Content-Type': 'application/json'}, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        error_message = str(e)
        if hasattr(e, 'response') and e.response is not None:
            if e.response.status_code not in (200, 201):
                error_body = e.response.json()
                error_message = error_body.get('error') or f"HTTP error! status: {
                    e.response.status_code}"
        raise Exception(f"Failed to get farms: {error_message}")


def get_farm_by_symbol(project: str, symbol: str, api_key: str) -> ApiResponse:
    """
    Get specific farm information by symbol for a DeFi project.

    :param project: The DeFi project name
    :param symbol: The farm symbol
    :param api_key: The API key for authentication
    :return: Information about the specific farm
    :raises Exception: If the request fails or server responds with an error
    """
    url = f"{API_URL}/defi/farms/{project}/{symbol}?apiKey={api_key}"

    try:
        response = requests.get(
            url, headers={'Content-Type': 'application/json'}, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        error_message = str(e)
        if hasattr(e, 'response') and e.response is not None:
            if e.response.status_code not in (200, 201):
                error_body = e.response.json()
                error_message = error_body.get('error') or f"HTTP error! status: {
                    e.response.status_code}"
        raise Exception(f"Failed to get farm by symbol: {error_message}")
