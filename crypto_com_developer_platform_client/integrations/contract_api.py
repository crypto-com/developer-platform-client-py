import requests
from ..constants import API_URL
from .api_interfaces import ApiResponse


def get_contract_code(api_key: str, contract_address: str) -> ApiResponse:
    """
    Get the bytecode of a smart contract.

    :param api_key: The API key for authentication.
    :param contract_address: The address of the smart contract.
    :return: The bytecode of the smart contract.
    :rtype: ApiResponse
    :raises Exception: If the contract code retrieval fails or the server responds with an error.
    """
    url = f"{API_URL}/contract/contract-code?contractAddress={contract_address}"

    response = requests.get(
        url,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
        },
        timeout=15,
    )

    if response.status_code not in (200, 201):
        error_body = response.json()
        server_error_message = (
            error_body.get("error") or f"HTTP error! status: {response.status_code}"
        )
        raise Exception(server_error_message)

    return response.json()


def get_contract_abi(
    api_key: str, contract_address: str, explorerKey: str
) -> ApiResponse:
    """
    Get the ABI for a smart contract.

    :param chain_id: The ID of the blockchain network
    :param api_key: The API key for authentication.
    :param contract_address: The address of the smart contract.
    :return: The ABI of the smart contract.
    :rtype: ApiResponse
    :raises Exception: If the contract ABI retrieval fails or the server responds with an error.
    """

    url = f"{API_URL}/contract/contract-abi?contractAddress={contract_address}&explorerKey={explorerKey}"

    response = requests.get(
        url,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
        },
        timeout=15,
    )

    if response.status_code not in (200, 201):
        error_body = response.json()
        server_error_message = (
            error_body.get("error") or f"""HTTP error! status: {response.status_code}"""
        )
        raise Exception(server_error_message)

    return response.json()
