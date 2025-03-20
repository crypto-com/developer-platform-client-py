from .client import Client
from .integrations.api_interfaces import ApiResponse
from .integrations.transaction_api import (
    get_transaction_by_hash,
    get_transaction_status,
    get_transactions_by_address,
)


class Transaction:
    """
    Transaction class for handling blockchain transactions and related queries.
    """

    _client: Client

    @classmethod
    def init(cls, client: Client) -> None:
        """
        Initialize the Transaction class with a Client instance.

        :param client: An instance of the Client class.
        """
        cls._client = client

    @classmethod
    def get_transactions_by_address(cls, address: str, startBlock: int, endBlock: int, session: str = "", limit: str = "20") -> ApiResponse:
        """
        Get transactions by address.

        :param address: The address to get transactions for (CronosIds with the `.cro` suffix are supported, e.g. `xyz.cro`)
        :param startBlock: The starting block number to get transactions from. (The maximum number of blocks that can be fetched is 10,000)
        :param endBlock: The ending block number to get transactions to. (The maximum number of blocks that can be fetched is 10,000)
        :param session: The session to get transactions for
        :param limit: The limit of transactions to get
        :return: The transactions for the address.
        """
        chain_id = cls._client.get_chain_id()
        api_key = cls._client.get_api_key()
        return get_transactions_by_address(chain_id, address, startBlock, endBlock, session, limit, api_key)

    @classmethod
    def get_transaction_by_hash(cls, hash: str) -> ApiResponse:
        """
        Get transaction by hash.

        :param hash: The hash of the transaction.
        :return: The transaction details.
        """
        chain_id = cls._client.get_chain_id()
        api_key = cls._client.get_api_key()
        return get_transaction_by_hash(chain_id, hash, api_key)

    @classmethod
    def get_transaction_status(cls, hash: str) -> ApiResponse:
        """
        Get transaction status.

        :param hash: The hash of the transaction.
        :return: The transaction status.
        """
        chain_id = cls._client.get_chain_id()
        api_key = cls._client.get_api_key()
        return get_transaction_status(chain_id, hash, api_key)
