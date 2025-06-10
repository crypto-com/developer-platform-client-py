import requests

from ..constants import API_URL
from .api_interfaces import ApiResponse


def get_native_token_balance(api_key: str, address: str) -> ApiResponse:
    """
    Get the native token balance for a given address.

    :param api_key: The API key for authentication.
    :param address: The address to check the balance for (CronosIds with the `.cro` suffix are supported, e.g. `xyz.cro`)
    :return: The native token balance.
    :rtype: ApiResponse
    """
    url = f"{API_URL}/token/native-token-balance?address={address}"

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


def get_erc20_token_balance(
    api_key: str, address: str, contract_address: str, block_height: str
) -> ApiResponse:
    """
    Get the ERC20 token balance for a given address.

    :param api_key: The API key for authentication.
    :param address: The address to check the balance for (CronosIds with the `.cro` suffix are supported, e.g. `xyz.cro`)
    :param contract_address: The address of the ERC20 token contract.
    :param block_height: The block height to check the balance at.
    :return: The ERC20 token balance.
    :rtype: ApiResponse
    """
    url = f"{API_URL}/token/erc20-token-balance?address={address}&contractAddress={contract_address}&blockHeight={block_height}"

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


def transfer_token(api_key: str, payload: dict) -> ApiResponse:
    """
    Transfer a token.

    :param api_key: The API key for authentication.
    :param payload: The payload for the transfer.
    :param provider: The provider for the transfer.
    :return: The transfer response.
    """
    url = f"{API_URL}/token/transfer"

    response = requests.get(
        url,
        json=payload,
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


def wrap_token(api_key: str, payload: dict) -> ApiResponse:
    """
    Wrap a token.

    :param api_key: The API key for authentication.
    :param payload: The payload for the wrap.
    :param provider: The provider for the wrap.
    :return: The wrap response.
    """
    url = f"{API_URL}/token/wrap"

    response = requests.get(
        url,
        json=payload,
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


def swap_token(api_key: str, payload: dict) -> ApiResponse:
    """
    Swap a token.

    :param api_key: The API key for authentication.
    :param payload: The payload for the swap.
    :param provider: The provider for the swap.
    :return: The swap response.
    """
    url = f"{API_URL}/token/swap"

    response = requests.get(
        url,
        json=payload,
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
