from .client import Client
from .integrations.api_interfaces import ApiResponse
from .integrations.cronosid_api import lookup_address, resolve_name


class CronosId:
    """
    CronosId utility class for resolving CronosId names and looking up addresses.
    """

    _client: Client

    @classmethod
    def init(cls, client: Client) -> None:
        """
        Initialize the CronosId class with a Client instance.

        :param client: An instance of the Client class.
        """
        cls._client = client

    @classmethod
    def resolve_name(cls, name: str) -> ApiResponse:
        """
        Resolves a CronosId to its corresponding blockchain address.

        :param name: The CronosId name to resolve (CronosIds with the `.cro` suffix are supported, e.g. `xyz.cro`)
        :return: Response containing the resolved blockchain address
        """
        chain_id = cls._client.get_chain_id()
        return resolve_name(chain_id, name)

    @classmethod
    def lookup_address(cls, address: str) -> ApiResponse:
        """
        Looks up an address to find its associated CronosId.

        :param address: The blockchain address to lookup
        :return: Response containing the CronosId name
        """
        chain_id = cls._client.get_chain_id()
        return lookup_address(chain_id, address)
