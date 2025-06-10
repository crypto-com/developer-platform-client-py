from .client import Client
from .integrations.api_interfaces import ApiResponse
from .integrations.wallet_api import create_wallet, get_balance


class Wallet:
    """
    Wallet class for managing wallet-related operations like creation and balance retrieval.
    """

    _client: Client

    @classmethod
    def init(cls, client: Client) -> None:
        """
        Initialize the Wallet class with a Client instance.

        :param client: An instance of the Client class.
        """
        cls._client = client

    @classmethod
    def create_wallet(cls) -> ApiResponse:
        """
        Create a new wallet.

        :raises ValueError: If the Wallet class is not initialized with a Client instance.
        :return: The address of the new wallet.
        """
        if cls._client is None:
            raise ValueError("Wallet class not initialized with a Client instance.")

        return create_wallet(cls._client.get_api_key())

    @classmethod
    def get_balance(cls, wallet_address: str) -> ApiResponse:
        """
        Get the balance of a wallet.

        :param wallet_address: The address to get the balance for (CronosIds with the `.cro` suffix are supported, e.g. `xyz.cro`)
        :raises ValueError: If the Wallet class is not initialized with a Client instance.
        :return: The balance of the wallet.
        """
        if cls._client is None:
            raise ValueError("Wallet class not initialized with a Client instance.")

        return get_balance(cls._client.get_api_key(), wallet_address)
