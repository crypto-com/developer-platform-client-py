import requests

from ..constants import API_URL
from .api_interfaces import ApiResponse
from .api_utils import handle_api_error


def get_all_tickers(api_key: str) -> ApiResponse:
    """
    Get all tickers from the Crypto.com Exchange (Chain agnostic).

    :param api_key: The API key for authentication.
    :return: A list of all available tickers and their information.
    :raises Exception: If the ticker retrieval fails or the server responds with an error.
    """
    url = f"{API_URL}/exchange/tickers"

    response = requests.get(
        url,
        headers={"Content-Type": "application/json", "x-api-key": api_key},
        timeout=15,
    )

    if response.status_code not in (200, 201):
        handle_api_error(response)

    return response.json()


def get_ticker_by_instrument(api_key: str, instrument_name: str) -> ApiResponse:
    """
    Get ticker information for a specific instrument from the Crypto.com Exchange (Chain agnostic).

    :param api_key: The API key for authentication.
    :param instrument_name: The name of the instrument to get ticker information for.
    :return: Ticker information for the specified instrument.
    :raises Exception: If the ticker retrieval fails, does not exist or the server responds with an error.
    """
    url = f"{API_URL}/exchange/tickers/{instrument_name}"

    response = requests.get(
        url,
        headers={"Content-Type": "application/json", "x-api-key": api_key},
        timeout=15,
    )

    if response.status_code not in (200, 201):
        handle_api_error(response)

    return response.json()
