import requests

from ..constants import API_URL
from .api_interfaces import ApiResponse
from .api_utils import handle_api_error


def create_wallet(api_key: str) -> ApiResponse:
    """
    Creates a new wallet using the API.

    :param api_key: The API key for authentication.
    :return: The newly created wallet information.
    :rtype: ApiResponse
    :raises Exception: If the wallet creation fails or the server responds with an error.
    """
    url = f"{API_URL}/wallet"

    response = requests.post(
        url,
        headers={"Content-Type": "application/json", "x-api-key": api_key},
        timeout=15,
    )

    if response.status_code not in (200, 201):
        handle_api_error(response)

    return response.json()


def get_balance(api_key: str, wallet_address: str) -> ApiResponse:
    """
    Fetches the native token balance of a wallet.

    :param api_key: The API key for authentication.
    :param wallet_address: The wallet address to check the balance for (CronosIds with the `.cro` suffix are supported, e.g. `xyz.cro`)
    :return: The native token balance of the wallet.
    :rtype: ApiResponse
    :raises Exception: If the fetch request fails or the server responds with an error message.
    """
    url = f"{API_URL}/wallet/balance?walletAddress={wallet_address}"

    response = requests.get(
        url,
        headers={"Content-Type": "application/json", "x-api-key": api_key},
        timeout=15,
    )

    if response.status_code not in (200, 201):
        handle_api_error(response)

    return response.json()
