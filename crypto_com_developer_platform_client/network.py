from typing import Optional

from .client import Client
from .integrations.api_interfaces import ApiResponse
from .integrations.network_api import get_chain_id, get_client_version, get_network_info


class Network:
    """
    Network class for accessing blockchain network metadata.
    """

    _client: Optional[Client] = None

    @classmethod
    def init(cls, client: Client) -> None:
        """
        Initialize the Network class with a Client instance.

        :param client: An instance of the Client class.
        """
        cls._client = client

    @classmethod
    def info(cls) -> ApiResponse:
        """
        Get general network info.

        :raises ValueError: If the Network class is not initialized with a Client instance.
        :return: Network metadata.
        """
        if cls._client is None:
            raise ValueError("Network class not initialized with a Client instance.")

        return get_network_info(cls._client.get_api_key())

    @classmethod
    def chain_id(cls) -> ApiResponse:
        """
        Get the current chain ID.

        :raises ValueError: If the Network class is not initialized with a Client instance.
        :return: Chain ID value.
        """
        if cls._client is None:
            raise ValueError("Network class not initialized with a Client instance.")

        return get_chain_id(cls._client.get_api_key())

    @classmethod
    def client_version(cls) -> ApiResponse:
        """
        Get the connected node's client version.

        :raises ValueError: If the Network class is not initialized with a Client instance.
        :return: Client version string.
        """
        if cls._client is None:
            raise ValueError("Network class not initialized with a Client instance.")

        return get_client_version(cls._client.get_api_key())
