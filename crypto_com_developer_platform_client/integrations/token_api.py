import requests

from ..constants import API_URL
from .api_interfaces import ApiResponse
from .api_utils import handle_api_error


def get_native_token_balance(api_key: str, wallet_address: str) -> ApiResponse:
    """
    Get the native token balance for a given address.

    :param api_key: The API key for authentication.
    :param wallet_address: The address to check the balance for (CronosIds with the `.cro` suffix are supported, e.g. `xyz.cro`)
    :return: The native token balance.
    :rtype: ApiResponse
    """
    url = f"{API_URL}/token/native-token-balance?walletAddress={wallet_address}"

    response = requests.get(
        url,
        headers={"Content-Type": "application/json", "x-api-key": api_key},
        timeout=15,
    )

    if response.status_code not in (200, 201):
        handle_api_error(response)

    return response.json()


def get_erc20_token_balance(
    api_key: str, wallet_address: str, contract_address: str, block_height: str
) -> ApiResponse:
    """
    Get the ERC20 token balance for a given address.

    :param api_key: The API key for authentication.
    :param wallet_address: The address to check the balance for (CronosIds with the `.cro` suffix are supported, e.g. `xyz.cro`)
    :param contract_address: The address of the ERC20 token contract.
    :param block_height: The block height to check the balance at.
    :return: The ERC20 token balance.
    :rtype: ApiResponse
    """
    url = f"{API_URL}/token/erc20-token-balance?walletAddress={wallet_address}&contractAddress={contract_address}&blockHeight={block_height}"

    response = requests.get(
        url,
        headers={"Content-Type": "application/json", "x-api-key": api_key},
        timeout=15,
    )

    if response.status_code not in (200, 201):
        handle_api_error(response)

    return response.json()


def transfer_token(api_key: str, payload: dict) -> ApiResponse:
    """
    Transfer a token.

    :param api_key: The API key for authentication.
    :param payload: The payload for the transfer.
    :param provider: The provider for the transfer.
    :return: The transfer response.
    """
    url = f"{API_URL}/token/transfer"

    response = requests.post(
        url,
        json=payload,
        headers={"Content-Type": "application/json", "x-api-key": api_key},
        timeout=15,
    )

    if response.status_code not in (200, 201):
        handle_api_error(response)

    return response.json()


def wrap_token(api_key: str, payload: dict) -> ApiResponse:
    """
    Wrap a token.

    :param api_key: The API key for authentication.
    :param payload: The payload for the wrap.
    :param provider: The provider for the wrap.
    :return: The wrap response.
    """
    url = f"{API_URL}/token/wrap"

    response = requests.post(
        url,
        json=payload,
        headers={"Content-Type": "application/json", "x-api-key": api_key},
        timeout=15,
    )

    if response.status_code not in (200, 201):
        handle_api_error(response)

    return response.json()


def swap_token(api_key: str, payload: dict) -> ApiResponse:
    """
    Swap a token.

    :param api_key: The API key for authentication.
    :param payload: The payload for the swap.
    :param provider: The provider for the swap.
    :return: The swap response.
    """
    url = f"{API_URL}/token/swap"

    response = requests.post(
        url,
        json=payload,
        headers={"Content-Type": "application/json", "x-api-key": api_key},
        timeout=15,
    )

    if response.status_code not in (200, 201):
        handle_api_error(response)

    return response.json()


def get_erc721_token_balance(
    api_key: str, wallet_address: str, contract_address: str
) -> ApiResponse:
    """
    Get the ERC721 token balance for a given address and contract address.

    :param api_key: The API key for authentication.
    :param wallet_address: The address to get the balance for.
    :param contract_address: The ERC721 contract address.
    :return: The balance of the ERC721 token.
    :rtype: ApiResponse
    """
    url = f"{API_URL}/token/erc721-token-balance?walletAddress={wallet_address}&contractAddress={contract_address}"

    response = requests.get(
        url,
        headers={"Content-Type": "application/json", "x-api-key": api_key},
        timeout=15,
    )

    if response.status_code not in (200, 201):
        handle_api_error(response)

    return response.json()


def get_token_owner(api_key: str, contract_address: str, token_id: str) -> ApiResponse:
    """
    Get the owner of a specific ERC721 token.

    :param api_key: The API key for authentication.
    :param contract_address: The ERC721 contract address.
    :param token_id: The token ID.
    :return: The owner address of the token.
    :rtype: ApiResponse
    """
    url = f"{API_URL}/token/erc721-token-owner?contractAddress={contract_address}&tokenId={token_id}"

    response = requests.get(
        url,
        headers={"Content-Type": "application/json", "x-api-key": api_key},
        timeout=15,
    )

    if response.status_code not in (200, 201):
        handle_api_error(response)

    return response.json()


def get_token_uri(api_key: str, contract_address: str, token_id: str) -> ApiResponse:
    """
    Get the URI of a specific ERC721 token.

    :param api_key: The API key for authentication.
    :param contract_address: The ERC721 contract address.
    :param token_id: The token ID.
    :return: The token URI.
    :rtype: ApiResponse
    """
    url = f"{API_URL}/token/erc721-token-uri?contractAddress={contract_address}&tokenId={token_id}"

    response = requests.get(
        url,
        headers={"Content-Type": "application/json", "x-api-key": api_key},
        timeout=15,
    )

    if response.status_code not in (200, 201):
        handle_api_error(response)

    return response.json()


def get_erc721_metadata(api_key: str, contract_address: str) -> ApiResponse:
    """
    Get the metadata of an ERC721 token contract.

    :param api_key: The API key for authentication.
    :param contract_address: The ERC721 contract address.
    :return: The metadata of the ERC721 contract.
    :rtype: ApiResponse
    """
    url = f"{API_URL}/token/erc721-token-metadata?contractAddress={contract_address}"

    response = requests.get(
        url,
        headers={"Content-Type": "application/json", "x-api-key": api_key},
        timeout=15,
    )

    if response.status_code not in (200, 201):
        handle_api_error(response)

    return response.json()


def get_erc20_metadata(api_key: str, contract_address: str) -> ApiResponse:
    """
    Get the metadata of an ERC20 token contract.

    :param api_key: The API key for authentication.
    :param contract_address: The ERC20 contract address.
    :return: The metadata of the ERC20 contract.
    :rtype: ApiResponse
    """
    url = f"{API_URL}/token/erc20-token-metadata?contractAddress={contract_address}"

    response = requests.get(
        url,
        headers={"Content-Type": "application/json", "x-api-key": api_key},
        timeout=15,
    )

    if response.status_code not in (200, 201):
        handle_api_error(response)

    return response.json()
