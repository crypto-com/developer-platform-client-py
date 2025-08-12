from typing import Optional
from urllib.parse import urlencode

import requests

from ..constants import API_URL
from .api_interfaces import ApiResponse
from .api_utils import handle_api_error



def get_transaction_by_hash(api_key: str, tx_hash: str) -> ApiResponse:
    """
    Get transaction by hash.

    :param chain_id: The ID of the blockchain network
    :param tx_hash: The hash of the transaction.
    :param api_key: The API key for authentication.
    :return: The transaction details.
    :rtype: ApiResponse
    """
    url = f"{API_URL}/transaction/tx-hash?txHash={tx_hash}"

    response = requests.get(
        url,
        headers={"Content-Type": "application/json", "x-api-key": api_key},
        timeout=15,
    )

    if response.status_code not in (200, 201):
        handle_api_error(response)

    return response.json()


def get_transaction_status(api_key: str, tx_hash: str) -> ApiResponse:
    """
    Get transaction status.

    :param chain_id: The ID of the blockchain network
    :param tx_hash: The hash of the transaction.
    :param api_key: The API key for authentication.
    :return: The transaction status.
    :rtype: ApiResponse
    """
    url = f"{API_URL}/transaction/status?txHash={tx_hash}"

    response = requests.get(
        url,
        headers={"Content-Type": "application/json", "x-api-key": api_key},
        timeout=15,
    )

    if response.status_code not in (200, 201):
        handle_api_error(response)

    return response.json()


def get_transaction_count(api_key: str, wallet_address: str) -> ApiResponse:
    """
    Get transaction count by wallet address.

    :param wallet_address: The address to get the transaction count for.
    :param api_key: The API key for authentication.
    :return: The transaction count for the wallet address.
    :rtype: ApiResponse
    """
    url = f"{API_URL}/transaction/tx-count?walletAddress={wallet_address}"

    response = requests.get(
        url,
        headers={"Content-Type": "application/json", "x-api-key": api_key},
        timeout=15,
    )

    if response.status_code not in (200, 201):
        handle_api_error(response)

    return response.json()


def get_gas_price(api_key: str) -> ApiResponse:
    """
    Get current gas price.

    :param api_key: The API key for authentication.
    :return: The current gas price.
    :rtype: ApiResponse
    """
    url = f"{API_URL}/transaction/gas-price"

    response = requests.get(
        url,
        headers={"Content-Type": "application/json", "x-api-key": api_key},
        timeout=15,
    )

    if response.status_code not in (200, 201):
        handle_api_error(response)

    return response.json()


def get_fee_data(api_key: str) -> ApiResponse:
    """
    Get current fee data.

    :param api_key: The API key for authentication.
    :return: The current fee data.
    :rtype: ApiResponse
    """
    url = f"{API_URL}/transaction/fee-data"

    response = requests.get(
        url,
        headers={"Content-Type": "application/json", "x-api-key": api_key},
        timeout=15,
    )

    if response.status_code not in (200, 201):
        handle_api_error(response)

    return response.json()


def estimate_gas(api_key: str, payload: dict) -> ApiResponse:
    """
    Estimate gas for a transaction.

    :param payload: The payload for gas estimation, including fields like `from`, `to`, `value`, `gasLimit`, `gasPrice`, `data`.
    :param api_key: The API key for authentication.
    :return: The estimated gas information.
    :rtype: ApiResponse
    """
    url = f"{API_URL}/transaction/estimate-gas"

    response = requests.post(
        url,
        headers={"Content-Type": "application/json", "x-api-key": api_key},
        json=payload,
        timeout=15,
    )

    if response.status_code not in (200, 201):
        handle_api_error(response)

    return response.json()
