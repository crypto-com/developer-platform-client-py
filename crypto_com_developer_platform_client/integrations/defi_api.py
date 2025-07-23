import requests

from ..constants import API_URL
from .api_interfaces import ApiResponse
from .api_utils import handle_api_error


def get_whitelisted_tokens(project: str, api_key: str) -> ApiResponse:
    """
    Get whitelisted tokens for a specific DeFi project.

    :param project: The DeFi project name
    :param api_key: The API key for authentication
    :return: List of whitelisted tokens
    :raises Exception: If the request fails or server responds with an error
    """
    url = f"{API_URL}/defi/whitelisted-tokens/{project}?apiKey={api_key}"

    response = requests.get(
        url,
        headers={"Content-Type": "application/json", "x-api-key": api_key},
        timeout=15,
    )

    if response.status_code not in (200, 201):
        handle_api_error(response)

    return response.json()


def get_all_farms(project: str, api_key: str) -> ApiResponse:
    """
    Get all farms for a specific DeFi project.

    :param project: The DeFi project name
    :param api_key: The API key for authentication
    :return: List of all farms
    :raises Exception: If the request fails or server responds with an error
    """
    url = f"{API_URL}/defi/farms/{project}?apiKey={api_key}"

    response = requests.get(
        url,
        headers={"Content-Type": "application/json", "x-api-key": api_key},
        timeout=15,
    )

    if response.status_code not in (200, 201):
        handle_api_error(response)

    return response.json()


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

    response = requests.get(
        url,
        headers={"Content-Type": "application/json", "x-api-key": api_key},
        timeout=15,
    )

    if response.status_code not in (200, 201):
        handle_api_error(response)

    return response.json()
