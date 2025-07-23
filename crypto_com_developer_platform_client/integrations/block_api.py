import requests

from ..constants import API_URL
from .api_interfaces import ApiResponse
from .api_utils import handle_api_error


def get_current_block(api_key: str) -> ApiResponse:
    """
    Get the latest block data from the blockchain.

    :param api_key: The API key used for authentication.
    :return: The current block data returned by the API.
    :rtype: ApiResponse
    :raises Exception: If the block retrieval fails or the server responds with an error.
    """
    url = f"{API_URL}/block/current-block"

    response = requests.get(
        url,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
        },
        timeout=15,
    )

    if response.status_code not in (200, 201):
        handle_api_error(response)

    return response.json()


def get_block_by_tag(api_key: str, block_tag: str, tx_detail: str) -> ApiResponse:
    """
    Get block by tag.

    :param chain_id: The ID of the blockchain network (e.g., Ethereum, Cronos).
    :param api_key: The API key for authentication.
    :param block_tag: The tag of the block to retrieve (e.g., "latest", "pending", "finalized").
    :param tx_detail: The detail level of transactions in the block (e.g., "full", "medium", "light").
    :return: The block data.
    :rtype: ApiResponse
    :raises Exception: If the block retrieval fails or the server responds with an error.
    """
    url = f"{API_URL}/block/block-tag?blockTag={block_tag}&txDetail={tx_detail}"

    response = requests.get(
        url,
        headers={"Content-Type": "application/json", "x-api-key": api_key},
        timeout=15,
    )

    if response.status_code not in (200, 201):
        handle_api_error(response)

    return response.json()
