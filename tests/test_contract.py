from unittest.mock import patch

import pytest
import responses

from crypto_com_developer_platform_client.client import Client
from crypto_com_developer_platform_client.constants import API_URL
from crypto_com_developer_platform_client.contract import Contract


class TestContract:
    """Test cases for the Contract class."""

    @pytest.mark.unit
    def test_init_with_client(self, mock_client):
        """Test Contract initialization with a Client instance."""
        Contract.init(mock_client)
        assert Contract._client == mock_client

    @pytest.mark.unit
    def test_get_contract_abi_without_client(self):
        """Test get_contract_abi without client initialization."""
        Contract._client = None

        with pytest.raises(
            ValueError, match="Contract class not initialized with a Client instance"
        ):
            Contract.get_contract_abi("0x123...", "explorer_key")

    @pytest.mark.unit
    def test_get_contract_code_without_client(self):
        """Test get_contract_code without client initialization."""
        Contract._client = None

        with pytest.raises(
            ValueError, match="Contract class not initialized with a Client instance"
        ):
            Contract.get_contract_code("0x123...")

    @pytest.mark.unit
    def test_contract_api_integration_with_integrations_module(self, mock_client):
        """Test that Contract class properly uses integrations.contract_api functions."""
        Contract.init(mock_client)

        with patch(
            "crypto_com_developer_platform_client.contract.get_contract_abi"
        ) as mock_abi:
            mock_abi.return_value = {"abi": []}
            result = Contract.get_contract_abi("0x123...", "explorer_key")

            mock_abi.assert_called_once_with(
                mock_client.get_api_key(), "0x123...", "explorer_key"
            )
            assert result == {"abi": []}

        with patch(
            "crypto_com_developer_platform_client.contract.get_contract_code"
        ) as mock_code:
            mock_code.return_value = {"bytecode": "0x123"}
            result = Contract.get_contract_code("0x123...")

            mock_code.assert_called_once_with(mock_client.get_api_key(), "0x123...")
            assert result == {"bytecode": "0x123"}

    @pytest.mark.unit
    def test_multiple_operations_same_client(self, mock_client):
        """Test multiple contract operations with the same client."""
        Contract.init(mock_client)

        with (
            patch(
                "crypto_com_developer_platform_client.contract.get_contract_abi"
            ) as mock_abi,
            patch(
                "crypto_com_developer_platform_client.contract.get_contract_code"
            ) as mock_code,
        ):

            mock_abi.return_value = {"abi": []}
            mock_code.return_value = {"bytecode": "0x123"}

            # Multiple operations
            Contract.get_contract_abi("0x123...", "explorer_key")
            Contract.get_contract_code("0x123...")
            Contract.get_contract_abi("0x456...", "explorer_key2")

            # Verify all use the same client
            assert mock_abi.call_count == 2
            assert mock_code.call_count == 1

            # Check API key consistency
            for call in mock_abi.call_args_list:
                assert call[0][0] == mock_client.get_api_key()

            mock_code.assert_called_with(mock_client.get_api_key(), "0x123...")
