from .client import Client
from .integrations.api_interfaces import ApiResponse
from .integrations.token_api import (
    get_erc20_metadata,
    get_erc20_token_balance,
    get_erc721_metadata,
    get_erc721_token_balance,
    get_native_token_balance,
    get_token_owner,
    get_token_uri,
    swap_token,
    transfer_token,
    wrap_token,
)


class Token:
    """
    Token class for managing native token and ERC20 token operations.
    """

    _client: Client

    @classmethod
    def init(cls, client: Client) -> None:
        """
        Initialize the Token class with a Client instance.

        :param client: An instance of the Client class.
        """
        cls._client = client

    @classmethod
    def get_native_balance(cls, address: str) -> ApiResponse:
        """
        Get the native token balance for a given address.

        :param address: The address to get the balance for (CronosIds with the `.cro` suffix are supported, e.g. `xyz.cro`)
        :raises ValueError: If the Token class is not initialized with a Client instance.
        :return: The balance of the native token.
        """
        if cls._client is None:
            raise ValueError("Token class not initialized with a Client instance.")

        return get_native_token_balance(cls._client.get_api_key(), address)

    @classmethod
    def get_erc20_balance(
        cls, wallet_address: str, contract_address: str, block_height: str = "latest"
    ) -> ApiResponse:
        """
        Get the ERC20 token balance for a given address and contract address.

        :param wallet_address: The address to get the balance for (CronosIds with the `.cro` suffix are supported, e.g. `xyz.cro`)
        :param contract_address: The contract address to get the balance for.
        :param block_height: The block height to get the balance for.
        :raises ValueError: If the Token class is not initialized with a Client instance.
        :return: The balance of the ERC20 token.
        """
        if cls._client is None:
            raise ValueError("Token class not initialized with a Client instance.")

        return get_erc20_token_balance(
            cls._client.get_api_key(),
            wallet_address,
            contract_address,
            block_height,
        )

    @classmethod
    def transfer_token(
        cls, to: str, amount: int, contract_address: str = ""
    ) -> ApiResponse:
        """
        Transfer a token to another address.

        :param to: The address to transfer the token to (CronosIds with the `.cro` suffix are supported, e.g. `xyz.cro`)
        :param amount: The amount of the token to transfer.
        :param contract_address: Optional. The contract address of the token to transfer.
        :raises ValueError: If the Token class is not initialized with a Client instance.
        :return: The transaction hash.
        """

        if cls._client is None:
            raise ValueError("Token class not initialized with a Client instance.")

        payload = {
            "to": to,
            "amount": amount,
            "provider": cls._client.get_provider(),
        }
        if contract_address:
            payload["contractAddress"] = contract_address

        return transfer_token(cls._client.get_api_key(), payload)

    @classmethod
    def wrap_token(cls, amount: float) -> ApiResponse:
        """
        Wrap a token to another address.

        :param amount: The amount of the token to wrap.
        :raises ValueError: If the Token class is not initialized with a Client instance.
        :return: The transaction hash.
        """
        if cls._client is None:
            raise ValueError("Token class not initialized with a Client instance.")

        payload = {
            "amount": amount,
            "provider": cls._client.get_provider(),
        }

        return wrap_token(cls._client.get_api_key(), payload)

    @classmethod
    def swap_token(
        cls, from_contract_address: str, to_contract_address: str, amount: int
    ) -> ApiResponse:
        """
        Swap a token for another token.

        :param from_contract_address: The token to swap from.
        :param to_contract_address: The token to swap to.
        :param amount: The amount of the token to swap.
        :raises ValueError: If the Token class is not initialized with a Client instance.
        :return: The transaction hash.
        """
        if cls._client is None:
            raise ValueError("Token class not initialized with a Client instance.")

        payload = {
            "fromContractAddress": from_contract_address,
            "toContractAddress": to_contract_address,
            "amount": amount,
            "provider": cls._client.get_provider(),
        }

        return swap_token(cls._client.get_api_key(), payload)

    @classmethod
    def get_erc721_balance(
        cls, wallet_address: str, contract_address: str
    ) -> ApiResponse:
        """
        Get the ERC721 token balance for a given address.

        :param wallet_address: The address to get the balance for.
        :param contract_address: The ERC721 contract address.
        :raises ValueError: If the Token class is not initialized with a Client instance.
        :return: The ERC721 token balance.
        """
        if cls._client is None:
            raise ValueError("Token class not initialized with a Client instance.")

        return get_erc721_token_balance(
            cls._client.get_api_key(), wallet_address, contract_address
        )

    @classmethod
    def get_token_owner(cls, contract_address: str, token_id: str) -> ApiResponse:
        """
        Get the owner of a specific ERC721 token.

        :param contract_address: The ERC721 contract address.
        :param token_id: The token ID.
        :raises ValueError: If the Token class is not initialized with a Client instance.
        :return: The owner of the token.
        """
        if cls._client is None:
            raise ValueError("Token class not initialized with a Client instance.")

        return get_token_owner(cls._client.get_api_key(), contract_address, token_id)

    @classmethod
    def get_token_uri(cls, contract_address: str, token_id: str) -> ApiResponse:
        """
        Get the URI of a specific ERC721 token.

        :param contract_address: The ERC721 contract address.
        :param token_id: The token ID.
        :raises ValueError: If the Token class is not initialized with a Client instance.
        :return: The token URI.
        """
        if cls._client is None:
            raise ValueError("Token class not initialized with a Client instance.")

        return get_token_uri(cls._client.get_api_key(), contract_address, token_id)

    @classmethod
    def get_erc721_metadata(cls, contract_address: str) -> ApiResponse:
        """
        Get the metadata of an ERC721 token contract.

        :param contract_address: The ERC721 contract address.
        :raises ValueError: If the Token class is not initialized with a Client instance.
        :return: The contract metadata.
        """
        if cls._client is None:
            raise ValueError("Token class not initialized with a Client instance.")

        return get_erc721_metadata(cls._client.get_api_key(), contract_address)

    @classmethod
    def get_erc20_metadata(cls, contract_address: str) -> ApiResponse:
        """
        Get the metadata of an ERC20 token contract.

        :param contract_address: The ERC20 contract address.
        :raises ValueError: If the Token class is not initialized with a Client instance.
        :return: The contract metadata.
        """
        if cls._client is None:
            raise ValueError("Token class not initialized with a Client instance.")

        return get_erc20_metadata(cls._client.get_api_key(), contract_address)
