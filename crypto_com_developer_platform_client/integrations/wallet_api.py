import requests

from ..constants import API_URL
from .api_interfaces import ApiResponse


def create_wallet() -> ApiResponse:
    """
    Creates a new wallet using the API.

    :return: The newly created wallet information.
    :rtype: ApiResponse
    :raises Exception: If the wallet creation fails or the server responds with an error.
    """
    url = f"{API_URL}/wallet"

    try:
        response = requests.post(
            url, headers={'Content-Type': 'application/json'}, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        error_message = str(e)
        if response.status_code not in (200, 201):
            error_body = response.json()
            error_message = error_body.get('error') or f"""HTTP error! status: {
                response.status_code}"""
        raise Exception(f"""Failed to create wallet: {error_message}""")


def get_balance(chain_id: str, address: str, api_key: str) -> ApiResponse:
    """
    Fetches the native token balance of a wallet.

    :param chain_id: The ID of the blockchain network
    :param address: The wallet address to check the balance for (CronosIds with the `.cro` suffix are supported, e.g. `xyz.cro`)
    :return: The native token balance of the wallet.
    :rtype: ApiResponse
    :raises Exception: If the fetch request fails or the server responds with an error message.
    """
    url = f"{API_URL}/wallet/{chain_id}/balance?address={address}&apiKey={api_key}"

    try:
        response = requests.get(
            url, headers={'Content-Type': 'application/json'}, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        error_message = str(e)
        if response.status_code not in (200, 201):
            error_body = response.json()
            error_message = error_body.get('error') or f"""HTTP error! status: {
                response.status_code}"""
        raise Exception(f"""Failed to fetch wallet balance: {error_message}""")
