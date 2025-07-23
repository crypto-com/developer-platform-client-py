class Client:
    """
    Client class for managing API key, chain ID and provider.
    """

    _api_key: str
    _provider: str

    @classmethod
    def init(cls, api_key: str, provider: str = "") -> None:
        """
        Initialize the client with API key and chain ID. Provider is optional.

        :param api_key: The API key for authentication.
        :param chain_id: The blockchain network ID.
        """

        cls._api_key = api_key
        cls._provider = provider

        from .block import Block
        from .contract import Contract
        from .cronosid import CronosId
        from .defi import Defi
        from .event import Event
        from .exchange import Exchange
        from .network import Network
        from .token import Token
        from .transaction import Transaction
        from .wallet import Wallet

        Contract.init(cls())
        Event.init(cls())
        Network.init(cls())
        Wallet.init(cls())
        Block.init(cls())
        Transaction.init(cls())
        Token.init(cls())
        Exchange.init(cls())
        Defi.init(cls())
        CronosId.init(cls())

    @classmethod
    def get_api_key(cls) -> str:
        """
        Get the API key.

        :return: The API key.
        :raises ValueError: If the API key is not set.
        """
        if not hasattr(cls, "_api_key") or cls._api_key is None:
            raise ValueError("API key is not set. Please set the API key.")

        return cls._api_key

    @classmethod
    def get_provider(cls) -> str:
        """
        Get the provider.

        :return: The provider.
        """
        if not hasattr(cls, "_provider") or cls._provider is None:
            raise ValueError("Provider is not set. Please set the provider.")

        return cls._provider
