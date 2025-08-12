from typing import Optional

from .client import Client
from .integrations.api_interfaces import ApiResponse
from .integrations.transaction_api import (
    estimate_gas,
    get_fee_data,
    get_gas_price,
    get_transaction_by_hash,
    get_transaction_count,
    get_transaction_status,
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
