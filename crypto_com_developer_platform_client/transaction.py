from typing import Optional
from .client import Client
from .integrations.api_interfaces import ApiResponse
from .integrations.transaction_api import (
    get_transaction_by_hash,
    get_transaction_status,
    get_transactions_by_address,
    get_transaction_count,
    get_gas_price,
    get_fee_data,
    estimate_gas,
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
    def get_transactions_by_address(
        cls,
        address: str,
        explorer_key: str,
        session: str = "",
        limit: str = "20",
        startBlock: Optional[int] = None,
        endBlock: Optional[int] = None,
    ) -> ApiResponse:
        """
        Get transactions by address.

        :param address: The address to get transactions for (CronosIds with the `.cro` suffix are supported, e.g. `xyz.cro`)
        :param startBlock: The starting block number to get transactions from. (The maximum number of blocks that can be fetched is 10,000)
        :param endBlock: The ending block number to get transactions to. (The maximum number of blocks that can be fetched is 10,000)
        :param session: The session to get transactions for
        :param limit: The limit of transactions to get
        :param contract_address: Optional. The contract address of the token to transfer.
        :raises ValueError: If the Transaction class is not initialized with a Client instance.
        :return: The transactions for the address.
        """
        if cls._client is None:
            raise ValueError(
                "Transaction class not initialized with a Client instance."
            )

        return get_transactions_by_address(
            cls._client.get_api_key(),
            address,
            explorer_key,
            startBlock,
            endBlock,
            session,
            limit,
        )

    @classmethod
    def get_transaction_by_hash(cls, hash: str) -> ApiResponse:
        """
        Get transaction by hash.

        :param hash: The hash of the transaction.
        :raises ValueError: If the Transaction class is not initialized with a Client instance.
        :return: The transaction details.
        """
        if cls._client is None:
            raise ValueError(
                "Transaction class not initialized with a Client instance."
            )

        return get_transaction_by_hash(cls._client.get_api_key(), hash)

    @classmethod
    def get_transaction_status(cls, hash: str) -> ApiResponse:
        """
        Get transaction status.

        :param hash: The hash of the transaction.
        :raises ValueError: If the Transaction class is not initialized with a Client instance.
        :return: The transaction status.
        """
        if cls._client is None:
            raise ValueError(
                "Transaction class not initialized with a Client instance."
            )

        return get_transaction_status(cls._client.get_api_key(), hash)

    @classmethod
    def get_transaction_count(cls, wallet_address: str) -> ApiResponse:
        """
        Get transaction count by wallet address.

        :param wallet_address: The address to get the transaction count for.
        :raises ValueError: If the Transaction class is not initialized with a Client instance.
        :return: The transaction count for the wallet address.
        """
        if cls._client is None:
            raise ValueError(
                "Transaction class not initialized with a Client instance."
            )

        return get_transaction_count(cls._client.get_api_key(), wallet_address)

    @classmethod
    def get_gas_price(cls) -> ApiResponse:
        """
        Get current gas price.

        :raises ValueError: If the Transaction class is not initialized with a Client instance.
        :return: The current gas price.
        """
        if cls._client is None:
            raise ValueError(
                "Transaction class not initialized with a Client instance."
            )

        return get_gas_price(cls._client.get_api_key())

    @classmethod
    def get_fee_data(cls) -> ApiResponse:
        """
        Get current fee data.

        :raises ValueError: If the Transaction class is not initialized with a Client instance.
        :return: The current fee data.
        """
        if cls._client is None:
            raise ValueError(
                "Transaction class not initialized with a Client instance."
            )

        return get_fee_data(cls._client.get_api_key())

    @classmethod
    def estimate_gas(cls, payload: dict) -> ApiResponse:
        """
        Estimate gas for a transaction.

        :param payload: The payload for gas estimation, including fields like `from`, `to`, `value`, `gasLimit`, `gasPrice`, `data`.
        :raises ValueError: If the Transaction class is not initialized with a Client instance.
        :return: The estimated gas information.
        """
        if cls._client is None:
            raise ValueError(
                "Transaction class not initialized with a Client instance."
            )

        return estimate_gas(cls._client.get_api_key(), payload)
