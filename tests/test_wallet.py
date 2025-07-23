"""
Tests for the Wallet class
"""

from unittest.mock import patch

import pytest
import responses

from crypto_com_developer_platform_client.client import Client
from crypto_com_developer_platform_client.constants import API_URL
from crypto_com_developer_platform_client.wallet import Wallet


class TestWallet:
    """Test cases for Wallet class."""

    def setup_method(self):
        """Reset state before each test."""
        Wallet._client = None

    @pytest.mark.unit
    def test_init_with_client(self, mock_client):
        """Test Wallet initialization with Client instance."""
        client_instance = Client()
        Wallet.init(client_instance)

        assert Wallet._client == client_instance

    @pytest.mark.unit
    def test_create_wallet_without_client(self):
        """Test Wallet.create_wallet() raises ValueError when not initialized."""
        with pytest.raises(ValueError, match="Wallet class not initialized"):
            Wallet.create_wallet()

    @pytest.mark.unit
    def test_get_balance_without_client(self, mock_wallet_address):
        """Test Wallet.get_balance() raises ValueError when not initialized."""
        with pytest.raises(ValueError, match="Wallet class not initialized"):
            Wallet.get_balance(mock_wallet_address)

    @pytest.mark.unit
    @responses.activate
    def test_create_wallet_success(self, mock_client):
        """Test successful wallet creation."""
        expected_response = {
            "success": True,
            "data": {
                "address": "0x123abc000000000000000000000000000000000",
                "privateKey": "0x1234567890abcdef...",
                "publicKey": "0xabcdef1234567890...",
            },
        }

        responses.add(
            responses.POST, f"{API_URL}/wallet", json=expected_response, status=201
        )

        Wallet.init(Client())
        result = Wallet.create_wallet()

        assert result == expected_response
        assert len(responses.calls) == 1
        assert (
            responses.calls[0].request.headers["x-api-key"] == mock_client.get_api_key()
        )
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"

    @pytest.mark.unit
    @responses.activate
    def test_get_balance_success(
        self, mock_client, mock_wallet_address, mock_wallet_balance
    ):
        """Test successful wallet balance retrieval."""
        responses.add(
            responses.GET,
            f"{API_URL}/wallet/balance",
            json=mock_wallet_balance,
            status=200,
        )

        Wallet.init(Client())
        result = Wallet.get_balance(mock_wallet_address)

        assert result == mock_wallet_balance
        assert len(responses.calls) == 1
        assert (
            responses.calls[0].request.headers["x-api-key"] == mock_client.get_api_key()
        )
        # Check that wallet address is included in the request
        assert mock_wallet_address in responses.calls[0].request.url

    @pytest.mark.unit
    @responses.activate
    def test_get_balance_with_cronos_id(self, mock_client):
        """Test wallet balance retrieval with Cronos ID (.cro suffix)."""
        cronos_id = "testuser.cro"
        expected_response = {
            "success": True,
            "data": {
                "balance": "2000000000000000000",  # 2 CRO
                "balanceInEth": "2.0",
                "address": cronos_id,
            },
        }

        responses.add(
            responses.GET,
            f"{API_URL}/wallet/balance",
            json=expected_response,
            status=200,
        )

        Wallet.init(Client())
        result = Wallet.get_balance(cronos_id)

        assert result == expected_response
        assert cronos_id in responses.calls[0].request.url

    @pytest.mark.unit
    @responses.activate
    def test_create_wallet_api_error(self, mock_client):
        """Test wallet creation with API error response."""
        error_response = {"error": "Quota exceeded", "code": "QUOTA_ERROR"}

        responses.add(
            responses.POST, f"{API_URL}/wallet", json=error_response, status=429
        )

        Wallet.init(Client())

        with pytest.raises(Exception, match="Quota exceeded"):
            Wallet.create_wallet()

    @pytest.mark.unit
    @responses.activate
    def test_get_balance_api_error(self, mock_client, mock_wallet_address):
        """Test wallet balance with API error response."""
        error_response = {"error": "Invalid address format"}

        responses.add(
            responses.GET, f"{API_URL}/wallet/balance", json=error_response, status=400
        )

        Wallet.init(Client())

        with pytest.raises(Exception, match="Invalid address format"):
            Wallet.get_balance(mock_wallet_address)

    @pytest.mark.unit
    @responses.activate
    def test_create_wallet_http_error_without_json(self, mock_client):
        """Test wallet creation with HTTP error and no JSON response."""
        responses.add(
            responses.POST, f"{API_URL}/wallet", body="Service Unavailable", status=503
        )

        Wallet.init(Client())

        with pytest.raises(Exception, match="HTTP error! status: 503"):
            Wallet.create_wallet()

    @pytest.mark.unit
    def test_wallet_api_integration_with_integrations_module(
        self, mock_client, mock_wallet_address
    ):
        """Test that Wallet class properly uses integrations.wallet_api functions."""
        Wallet.init(Client())

        with patch(
            "crypto_com_developer_platform_client.wallet.create_wallet"
        ) as mock_create:
            mock_create.return_value = {"address": "0x123..."}
            result = Wallet.create_wallet()

            mock_create.assert_called_once_with(mock_client.get_api_key())
            assert result == {"address": "0x123..."}

        with patch(
            "crypto_com_developer_platform_client.wallet.get_balance"
        ) as mock_get_balance:
            mock_get_balance.return_value = {"balance": "1000000000000000000"}
            result = Wallet.get_balance(mock_wallet_address)

            mock_get_balance.assert_called_once_with(
                mock_client.get_api_key(), mock_wallet_address
            )
            assert result == {"balance": "1000000000000000000"}

    @pytest.mark.unit
    @responses.activate
    def test_multiple_operations_same_client(self, mock_client, mock_wallet_address):
        """Test multiple wallet operations with the same client instance."""
        create_response = {
            "success": True,
            "data": {"address": "0x123...", "privateKey": "0xabc..."},
        }
        balance_response = {
            "success": True,
            "data": {"balance": "1000000000000000000", "balanceInEth": "1.0"},
        }

        responses.add(
            responses.POST, f"{API_URL}/wallet", json=create_response, status=201
        )
        responses.add(
            responses.GET,
            f"{API_URL}/wallet/balance",
            json=balance_response,
            status=200,
        )

        Wallet.init(Client())

        create_result = Wallet.create_wallet()
        balance_result = Wallet.get_balance(mock_wallet_address)

        assert create_result == create_response
        assert balance_result == balance_response
        assert len(responses.calls) == 2

    @pytest.mark.unit
    def test_wallet_address_parameter_handling(self, mock_client):
        """Test proper handling of different wallet address formats."""
        Wallet.init(Client())

        with patch(
            "crypto_com_developer_platform_client.wallet.get_balance"
        ) as mock_get_balance:
            # Test with regular Ethereum address
            eth_address = "0x123abc000000000000000000000000000000000"
            Wallet.get_balance(eth_address)
            mock_get_balance.assert_called_with(mock_client.get_api_key(), eth_address)

            # Test with Cronos ID
            cronos_id = "alice.cro"
            Wallet.get_balance(cronos_id)
            mock_get_balance.assert_called_with(mock_client.get_api_key(), cronos_id)

            # Test with mixed case address
            mixed_case = "0x123abc000000000000000000000000000000000"
            Wallet.get_balance(mixed_case)
            mock_get_balance.assert_called_with(mock_client.get_api_key(), mixed_case)
