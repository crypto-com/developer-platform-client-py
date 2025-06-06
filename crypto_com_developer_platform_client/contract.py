from typing import Optional

from .client import Client
from .integrations.api_interfaces import ApiResponse
from .integrations.contract_api import get_contract_abi, get_contract_code


class Contract:
    """
    Contract class for fetching smart contract ABIs.
    """

    _client: Optional[Client] = None

    @classmethod
    def init(cls, client: Client) -> None:
        """
        Initialize the Contract class with a Client instance.

        :param client: An instance of the Client class.
        """
        cls._client = client

    @classmethod
    def get_contract_abi(cls, contract_address: str, explorerKey: str) -> ApiResponse:
        """
        Get the ABI for a smart contract.

        :param contract_address: The address of the smart contract.
        """
        if cls._client is None:
            raise ValueError("Network class not initialized with a Client instance.")

        return get_contract_abi(
            cls._client.get_api_key(), contract_address, explorerKey
        )

    @classmethod
    def get_contract_code(cls, contract_address: str) -> ApiResponse:
        """
        Get the bytecode of a smart contract.

        :param contract_address: The address of the smart contract.
        :return: The bytecode of the smart contract.
        """
        if cls._client is None:
            raise ValueError("Network class not initialized with a Client instance.")

        return get_contract_code(cls._client.get_api_key(), contract_address)
