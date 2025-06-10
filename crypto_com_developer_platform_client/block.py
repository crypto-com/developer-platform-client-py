from .client import Client
from .integrations.api_interfaces import ApiResponse
from .integrations.block_api import get_block_by_tag, get_current_block


class Block:
    """
    Block class for fetching block data.
    """

    _client: Client

    @classmethod
    def init(cls, client: Client) -> None:
        """
        Initialize the Block class with a Client instance.

        :param client: An instance of the Client class.
        """
        cls._client = client

    @classmethod
    def get_by_tag(cls, tag: str = "latest", tx_detail: str = "false") -> ApiResponse:
        """
        Get block data by tag.

        :param tag: Integer of a block number in hex, or the string "earliest", "latest" or "pending", as in https://ethereum.org/en/developers/docs/apis/json-rpc/#default-block
        :param tx_detail: If true it returns the full transaction objects, if false only the hashes of the transactions.
        :raises ValueError: If the Block class is not initialized with a Client instance.
        :return: The block data.
        """
        if cls._client is None:
            raise ValueError("Block class not initialized with a Client instance.")

        return get_block_by_tag(cls._client.get_api_key(), tag, tx_detail)

    @classmethod
    def get_current(cls) -> ApiResponse:
        """
        Get the current block (latest).

        :raises ValueError: If the Block class is not initialized with a Client instance.
        :return: The latest block data.
        """
        if cls._client is None:
            raise ValueError("Block class not initialized with a Client instance.")

        return get_current_block(cls._client.get_api_key())
