import requests

from ..constants import API_URL
from .api_interfaces import ApiResponse


def get_transactions_by_address(chain_id: str, address: str, startBlock: int, endBlock: int, session: str, limit: str, api_key: str) -> ApiResponse:
    """
    Get transactions by address.

    :param chain_id: The ID of the blockchain network
    :param address: The address to get transactions for (CronosIds with the `.cro` suffix are supported, e.g. `xyz.cro`)
    :param startBlock: The starting block number to get transactions from. (The maximum number of blocks that can be fetched is 10,000)
    :param endBlock: The ending block number to get transactions to. (The maximum number of blocks that can be fetched is 10,000)
    :param session: The session to get transactions for
    :param limit: The limit of transactions to get
    :param api_key: The API key for authentication
    :return: The transactions for the address
    :rtype: ApiResponse
    """
    url = f"{API_URL}/transaction/{chain_id}/address?address={address}&startBlock={startBlock}&endBlock={endBlock}&session={session}&limit={limit}&apiKey={api_key}"

    response = requests.get(url, headers={'Content-Type': 'application/json'}, timeout=15)

    if response.status_code not in (200, 201):
        error_body = response.json()
        server_error_message = error_body.get('error') or f"""HTTP error! status: {
            response.status_code}"""
        raise Exception(f"""Failed to fetch transactions by address: {
                        server_error_message}""")

    return response.json()


def get_transaction_by_hash(chain_id: str, tx_hash: str, api_key: str) -> ApiResponse:
    """
    Get transaction by hash.

    :param chain_id: The ID of the blockchain network
    :param tx_hash: The hash of the transaction.
    :param api_key: The API key for authentication.
    :return: The transaction details.
    :rtype: ApiResponse
    """
    url = f"{API_URL}/transaction/{chain_id}/tx-hash?txHash={tx_hash}&apiKey={api_key}"

    response = requests.get(url, headers={'Content-Type': 'application/json'}, timeout=15)

    if response.status_code not in (200, 201):
        error_body = response.json()
        server_error_message = error_body.get('error') or f"""HTTP error! status: {
            response.status_code}"""
        raise Exception(f"""Failed to fetch transaction by hash: {
                        server_error_message}""")

    return response.json()


def get_transaction_status(chain_id: str, tx_hash: str, api_key: str) -> ApiResponse:
    """
    Get transaction status.

    :param chain_id: The ID of the blockchain network
    :param tx_hash: The hash of the transaction.
    :param api_key: The API key for authentication.
    :return: The transaction status.
    :rtype: ApiResponse
    """
    url = f"{API_URL}/transaction/{chain_id}/status?txHash={tx_hash}&apiKey={api_key}"

    response = requests.get(url, headers={'Content-Type': 'application/json'}, timeout=15)

    if response.status_code not in (200, 201):
        error_body = response.json()
        server_error_message = error_body.get('error') or f"""HTTP error! status: {
            response.status_code}"""
        raise Exception(f"""Failed to fetch transaction status: {
                        server_error_message}""")

    return response.json()
