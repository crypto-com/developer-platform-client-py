from typing import Optional
from urllib.parse import urlencode
import requests

from ..constants import API_URL
from .api_interfaces import ApiResponse


def get_transactions_by_address(
    api_key: str,
    address: str,
    explorer_key: str,
    session: str,
    limit: str,
    start_block: Optional[int],
    end_block: Optional[int],
) -> ApiResponse:
    """
    Get transactions by address.

    :param chain_id: The ID of the blockchain network
    :param address: The address to get transactions for (CronosIds with the `.cro` suffix are supported, e.g. `xyz.cro`)
    :param start_block: The starting block number to get transactions from. (The maximum number of blocks that can be fetched is 10,000)
    :param end_block: The ending block number to get transactions to. (The maximum number of blocks that can be fetched is 10,000)
    :param session: The session to get transactions for
    :param limit: The limit of transactions to get
    :param api_key: The API key for authentication
    :return: The transactions for the address
    :rtype: ApiResponse
    """
    params = {
        "address": address,
        "limit": limit,
        "explorerKey": explorer_key,
    }

    if start_block is not None:
        params["startBlock"] = start_block

    if end_block is not None:
        params["endBlock"] = end_block

    if session:
        params["session"] = session

    query_string = urlencode(params)
    url = f"{API_URL}/transaction/address?{query_string}"

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
        error_body = response.json()
        server_error_message = (
            error_body.get("error") or f"HTTP error! status: {response.status_code}"
        )
        raise Exception(server_error_message)

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
        error_body = response.json()
        server_error_message = (
            error_body.get("error") or f"HTTP error! status: {response.status_code}"
        )
        raise Exception(server_error_message)

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
        error_body = response.json()
        server_error_message = (
            error_body.get("error") or f"HTTP error! status: {response.status_code}"
        )
        raise Exception(server_error_message)

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
        error_body = response.json()
        server_error_message = (
            error_body.get("error") or f"HTTP error! status: {response.status_code}"
        )
        raise Exception(server_error_message)

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
        error_body = response.json()
        server_error_message = (
            error_body.get("error") or f"HTTP error! status: {response.status_code}"
        )
        raise Exception(server_error_message)

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
        error_body = response.json()
        server_error_message = (
            error_body.get("error") or f"HTTP error! status: {response.status_code}"
        )
        raise Exception(server_error_message)

    return response.json()
