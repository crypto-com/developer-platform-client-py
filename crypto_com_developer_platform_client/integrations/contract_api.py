import requests

from ..constants import API_URL
from .api_interfaces import ApiResponse
from .api_utils import handle_api_error


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
        handle_api_error(response)

    return response.json()


