from .client import Client
from .integrations.api_interfaces import ApiResponse
from .integrations.defi_api import (
    get_all_farms,
    get_farm_by_symbol,
    get_whitelisted_tokens,
)
from .interfaces.defi_interfaces import DefiProtocol


class Defi:
    """
    Defi class for managing DeFi-related operations like getting whitelisted tokens and farm information.
    """

    _client: Client

    @classmethod
    def init(cls, client: Client) -> None:
        """
        Initialize the Defi class with a Client instance.

        :param client: An instance of the Client class.
        """
        cls._client = client

    @classmethod
    def get_whitelisted_tokens(cls, protocol: DefiProtocol) -> ApiResponse:
        """
        Get whitelisted tokens for a specific DeFi project.

        :param protocol: The DeFi protocol (e.g., DefiProtocol.H2FINANCE, DefiProtocol.VVSFINANCE)
        :return: List of whitelisted tokens for the project
        """
        api_key = cls._client.get_api_key()
        return get_whitelisted_tokens(protocol.value, api_key)

    @classmethod
    def get_all_farms(cls, protocol: DefiProtocol) -> ApiResponse:
        """
        Get all farms for a specific DeFi project.

        :param protocol: The DeFi protocol (e.g., DefiProtocol.H2FINANCE, DefiProtocol.VVSFINANCE)
        :return: List of all farms for the project
        """
        api_key = cls._client.get_api_key()
        return get_all_farms(protocol.value, api_key)

    @classmethod
    def get_farm_by_symbol(cls, protocol: DefiProtocol, symbol: str) -> ApiResponse:
        """
        Get specific farm information by symbol for a DeFi project.

        :param protocol: The DeFi protocol (e.g., DefiProtocol.H2FINANCE, DefiProtocol.VVSFINANCE)
        :param symbol: The farm symbol (e.g., 'zkCRO-MOON', 'CRO-GOLD')
        :return: Information about the specific farm
        """
        api_key = cls._client.get_api_key()
        return get_farm_by_symbol(protocol.value, symbol, api_key)
