"""
Tests for the Token class
"""

from unittest.mock import patch

import pytest
import responses

from crypto_com_developer_platform_client.client import Client
from crypto_com_developer_platform_client.constants import API_URL
from crypto_com_developer_platform_client.token import Token


class TestToken:
    """Test cases for Token class."""

    def setup_method(self):
        """Reset state before each test."""
        Token._client = None

    @pytest.mark.unit
    def test_init_with_client(self, mock_client):
        """Test Token initialization with Client instance."""
        client_instance = Client()
        Token.init(client_instance)

        assert Token._client == client_instance

    @pytest.mark.unit
    def test_get_native_balance_without_client(self, mock_wallet_address):
        """Test Token.get_native_balance() raises ValueError when not initialized."""
        with pytest.raises(ValueError, match="Token class not initialized"):
            Token.get_native_balance(mock_wallet_address)

    @pytest.mark.unit
    @responses.activate
    def test_get_native_balance_success(self, mock_client, mock_wallet_address):
        """Test successful native token balance retrieval."""
        expected_response = {
            "success": True,
            "data": {
                "balance": "1500000000000000000",  # 1.5 CRO
                "balanceInEth": "1.5",
                "symbol": "CRO",
                "decimals": 18,
            },
        }

        responses.add(
            responses.GET,
            f"{API_URL}/token/native-token-balance",
            json=expected_response,
            status=200,
        )

        Token.init(Client())
        result = Token.get_native_balance(mock_wallet_address)

        assert result == expected_response
        assert len(responses.calls) == 1
        assert (
            responses.calls[0].request.headers["x-api-key"] == mock_client.get_api_key()
        )
        assert f"walletAddress={mock_wallet_address}" in responses.calls[0].request.url

    @pytest.mark.unit
    @responses.activate
    def test_get_erc20_balance_success(
        self, mock_client, mock_wallet_address, mock_contract_address
    ):
        """Test successful ERC20 token balance retrieval."""
        expected_response = {
            "success": True,
            "data": {
                "balance": "1000000000",  # 1000 USDC (6 decimals)
                "decimals": 6,
                "symbol": "USDC",
                "name": "USD Coin",
            },
        }

        responses.add(
            responses.GET,
            f"{API_URL}/token/erc20-token-balance",
            json=expected_response,
            status=200,
        )

        Token.init(Client())
        result = Token.get_erc20_balance(mock_wallet_address, mock_contract_address)

        assert result == expected_response
        assert len(responses.calls) == 1
        assert f"walletAddress={mock_wallet_address}" in responses.calls[0].request.url
        assert (
            f"contractAddress={mock_contract_address}" in responses.calls[0].request.url
        )

    @pytest.mark.unit
    @responses.activate
    def test_get_native_balance_with_cronos_id(self, mock_client):
        """Test native balance retrieval with Cronos ID."""
        cronos_id = "alice.cro"
        expected_response = {
            "success": True,
            "data": {
                "balance": "2000000000000000000",  # 2 CRO
                "balanceInEth": "2.0",
                "symbol": "CRO",
            },
        }

        responses.add(
            responses.GET,
            f"{API_URL}/token/native-token-balance",
            json=expected_response,
            status=200,
        )

        Token.init(Client())
        result = Token.get_native_balance(cronos_id)

        assert result == expected_response
        assert f"walletAddress={cronos_id}" in responses.calls[0].request.url

    @pytest.mark.unit
    @responses.activate
    def test_transfer_token_success(self, mock_client):
        """Test successful token transfer."""
        recipient = "0x123abc000000000000000000000000000000000"
        amount = 100
        expected_response = {
            "success": True,
            "data": {"transactionHash": "0xabcd1234...", "status": "pending"},
        }

        responses.add(
            responses.POST,
            f"{API_URL}/token/transfer",
            json=expected_response,
            status=200,
        )

        Token.init(Client())
        result = Token.transfer_token(recipient, amount)

        assert result == expected_response
        assert len(responses.calls) == 1

    @pytest.mark.unit
    @responses.activate
    def test_wrap_token_success(self, mock_client):
        """Test successful token wrapping."""
        from_contract = "0x456def000000000000000000000000000000000"
        to_contract = "0x123abc000000000000000000000000000000000"
        receiver = "0x789012000000000000000000000000000000000"
        amount = 50

        expected_response = {
            "success": True,
            "data": {"transactionHash": "0xwrap1234...", "status": "pending"},
        }

        responses.add(
            responses.POST, f"{API_URL}/token/wrap", json=expected_response, status=200
        )

        Token.init(Client())
        result = Token.wrap_token(amount)

        assert result == expected_response
        assert len(responses.calls) == 1

    @pytest.mark.unit
    @responses.activate
    def test_swap_token_success(self, mock_client):
        """Test successful token swap."""
        from_token = "0x456def000000000000000000000000000000000"
        to_token = "0x123abc000000000000000000000000000000000"
        receiver = "0x789012000000000000000000000000000000000"
        amount = 25

        expected_response = {
            "success": True,
            "data": {
                "transactionHash": "0xswap1234...",
                "status": "pending",
                "estimatedOutput": "24.5",
            },
        }

        responses.add(
            responses.POST, f"{API_URL}/token/swap", json=expected_response, status=200
        )

        Token.init(Client())
        result = Token.swap_token(from_token, to_token, amount)

        assert result == expected_response
        assert len(responses.calls) == 1

    @pytest.mark.unit
    @responses.activate
    def test_get_native_balance_api_error(self, mock_client, mock_wallet_address):
        """Test native balance with API error response."""
        error_response = {"error": "Invalid wallet address"}

        responses.add(
            responses.GET,
            f"{API_URL}/token/native-token-balance",
            json=error_response,
            status=400,
        )

        Token.init(Client())

        with pytest.raises(Exception, match="Invalid wallet address"):
            Token.get_native_balance(mock_wallet_address)

    @pytest.mark.unit
    @responses.activate
    def test_get_erc20_balance_api_error(
        self, mock_client, mock_wallet_address, mock_contract_address
    ):
        """Test ERC20 balance with API error response."""
        error_response = {"error": "Contract not found"}

        responses.add(
            responses.GET,
            f"{API_URL}/token/erc20-token-balance",
            json=error_response,
            status=404,
        )

        Token.init(Client())

        with pytest.raises(Exception, match="Contract not found"):
            Token.get_erc20_balance(mock_wallet_address, mock_contract_address)

    @pytest.mark.unit
    @responses.activate
    def test_transfer_token_api_error(self, mock_client):
        """Test token transfer with API error response."""
        error_response = {"error": "Insufficient balance"}

        responses.add(
            responses.POST, f"{API_URL}/token/transfer", json=error_response, status=422
        )

        Token.init(Client())

        with pytest.raises(Exception, match="Insufficient balance"):
            Token.transfer_token("0x123...", 100)

    @pytest.mark.unit
    def test_token_api_integration_with_integrations_module(
        self, mock_client, mock_wallet_address, mock_contract_address
    ):
        """Test that Token class properly uses integrations.token_api functions."""
        Token.init(Client())

        with patch(
            "crypto_com_developer_platform_client.token.get_native_token_balance"
        ) as mock_native:
            mock_native.return_value = {"balance": "1000000000000000000"}
            result = Token.get_native_balance(mock_wallet_address)

            mock_native.assert_called_once_with(
                mock_client.get_api_key(), mock_wallet_address
            )
            assert result == {"balance": "1000000000000000000"}

        with patch(
            "crypto_com_developer_platform_client.token.get_erc20_token_balance"
        ) as mock_erc20:
            mock_erc20.return_value = {"balance": "500000000"}
            result = Token.get_erc20_balance(mock_wallet_address, mock_contract_address)

            mock_erc20.assert_called_once_with(
                mock_client.get_api_key(),
                mock_wallet_address,
                mock_contract_address,
                "latest",
            )
            assert result == {"balance": "500000000"}

    @pytest.mark.unit
    @responses.activate
    def test_multiple_token_operations(
        self, mock_client, mock_wallet_address, mock_contract_address
    ):
        """Test multiple token operations with the same client instance."""
        native_response = {"balance": "1000000000000000000", "symbol": "CRO"}
        erc20_response = {"balance": "500000000", "symbol": "USDC"}

        responses.add(
            responses.GET,
            f"{API_URL}/token/native-token-balance",
            json=native_response,
            status=200,
        )
        responses.add(
            responses.GET,
            f"{API_URL}/token/erc20-token-balance",
            json=erc20_response,
            status=200,
        )

        Token.init(Client())

        native_result = Token.get_native_balance(mock_wallet_address)
        erc20_result = Token.get_erc20_balance(
            mock_wallet_address, mock_contract_address
        )

        assert native_result == native_response
        assert erc20_result == erc20_response
        assert len(responses.calls) == 2

    @pytest.mark.unit
    @responses.activate
    def test_erc721_token_balance_success(
        self, mock_client, mock_wallet_address, mock_contract_address
    ):
        """Test successful ERC721 token balance retrieval."""
        expected_response = {
            "success": True,
            "data": {"balance": 5, "tokens": ["1", "2", "3", "4", "5"]},  # 5 NFTs
        }

        responses.add(
            responses.GET,
            f"{API_URL}/token/erc721-token-balance",
            json=expected_response,
            status=200,
        )

        Token.init(Client())
        result = Token.get_erc721_balance(mock_wallet_address, mock_contract_address)

        assert result == expected_response
        assert len(responses.calls) == 1
        assert f"walletAddress={mock_wallet_address}" in responses.calls[0].request.url
        assert (
            f"contractAddress={mock_contract_address}" in responses.calls[0].request.url
        )

    @pytest.mark.unit
    @responses.activate
    def test_token_metadata_retrieval(self, mock_client, mock_contract_address):
        """Test token metadata retrieval for ERC20 and ERC721 tokens."""
        erc20_metadata = {
            "success": True,
            "data": {
                "name": "USD Coin",
                "symbol": "USDC",
                "decimals": 6,
                "totalSupply": "1000000000000000",
            },
        }

        responses.add(
            responses.GET,
            f"{API_URL}/token/erc20-token-metadata",
            json=erc20_metadata,
            status=200,
        )

        Token.init(Client())
        result = Token.get_erc20_metadata(mock_contract_address)

        assert result == erc20_metadata
        assert (
            f"contractAddress={mock_contract_address}" in responses.calls[0].request.url
        )
