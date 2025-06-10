from typing import Optional

from .client import Client
from .integrations.api_interfaces import ApiResponse
from .integrations.event_api import get_logs


class Event:
    """
    Contract class for fetching event logs.
    """

    _client: Optional[Client] = None

    @classmethod
    def init(cls, client: Client) -> None:
        """
        Initialize the Event class with a Client instance.

        :param client: An instance of the Client class.
        """
        cls._client = client

    @classmethod
    def get_logs(cls, address: str) -> ApiResponse:
        """
        Get the emitted events of a smart contract.

        :param address: The address of the smart contract.
        :return: A list of decoded contract events.
        """
        if cls._client is None:
            raise ValueError("Event class not initialized with a Client instance.")

        return get_logs(cls._client.get_api_key(), address)
