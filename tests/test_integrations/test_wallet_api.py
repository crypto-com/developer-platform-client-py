"""
Tests for wallet_api integration module
"""

from unittest.mock import Mock, patch

import pytest
import responses

from crypto_com_developer_platform_client.constants import API_URL
from crypto_com_developer_platform_client.integrations.wallet_api import (
    create_wallet,
    get_balance,
)


class TestWalletApi:
    """Test cases for wallet_api integration functions."""

    @pytest.mark.unit
    @responses.activate
    def test_create_wallet_success(self, mock_api_key):
        """Test successful wallet creation."""
        expected_response = {
            "success": True,
            "data": {
                "address": "0x123abc000000000000000000000000000000000",
                "privateKey": "0x123abc000000000000000000000000000000000000000000000000000000",
                "publicKey": "0x456def000000000000000000000000000000000000000000000000000000",
            },
        }

        responses.add(
            responses.POST, f"{API_URL}/wallet", json=expected_response, status=201
        )

        result = create_wallet(mock_api_key)

        assert result == expected_response
        assert len(responses.calls) == 1

        request = responses.calls[0].request
        assert request.headers["x-api-key"] == mock_api_key
        assert request.headers["Content-Type"] == "application/json"

    @pytest.mark.unit
    @responses.activate
    def test_get_balance_success(self, mock_api_key, mock_wallet_address):
        """Test successful balance retrieval."""
        expected_response = {
            "success": True,
            "data": {
                "balance": "1000000000000000000",  # 1 CRO in wei
                "balanceInEth": "1.0",
                "address": mock_wallet_address,
            },
        }

        responses.add(
            responses.GET,
            f"{API_URL}/wallet/balance",
            json=expected_response,
            status=200,
        )

        result = get_balance(mock_api_key, mock_wallet_address)

        assert result == expected_response
        assert len(responses.calls) == 1

        request = responses.calls[0].request
        assert request.headers["x-api-key"] == mock_api_key
        assert f"walletAddress={mock_wallet_address}" in request.url

    @pytest.mark.unit
    @responses.activate
    def test_get_balance_with_cronos_id(self, mock_api_key):
        """Test balance retrieval with Cronos ID."""
        cronos_id = "alice.cro"
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

        result = get_balance(mock_api_key, cronos_id)

        assert result == expected_response
        assert f"walletAddress={cronos_id}" in responses.calls[0].request.url

    @pytest.mark.unit
    @responses.activate
    def test_create_wallet_api_error(self, mock_api_key):
        """Test wallet creation with API error response."""
        error_response = {"error": "Service temporarily unavailable"}

        responses.add(
            responses.POST, f"{API_URL}/wallet", json=error_response, status=503
        )

        with pytest.raises(Exception, match="Service temporarily unavailable"):
            create_wallet(mock_api_key)

    @pytest.mark.unit
    @responses.activate
    def test_get_balance_api_error(self, mock_api_key, mock_wallet_address):
        """Test balance retrieval with API error response."""
        error_response = {"error": "Invalid wallet address format"}

        responses.add(
            responses.GET, f"{API_URL}/wallet/balance", json=error_response, status=400
        )

        with pytest.raises(Exception, match="Invalid wallet address format"):
            get_balance(mock_api_key, mock_wallet_address)

    @pytest.mark.unit
    @responses.activate
    def test_create_wallet_http_error_without_json(self, mock_api_key):
        """Test wallet creation with HTTP error and no JSON response."""
        responses.add(
            responses.POST,
            f"{API_URL}/wallet",
            body="Internal Server Error",
            status=500,
        )

        with pytest.raises(Exception, match="HTTP error! status: 500"):
            create_wallet(mock_api_key)

    @pytest.mark.unit
    @responses.activate
    def test_get_balance_http_error_without_json(
        self, mock_api_key, mock_wallet_address
    ):
        """Test balance retrieval with HTTP error and no JSON response."""
        responses.add(
            responses.GET, f"{API_URL}/wallet/balance", body="Not Found", status=404
        )

        with pytest.raises(Exception, match="HTTP error! status: 404"):
            get_balance(mock_api_key, mock_wallet_address)

    @pytest.mark.unit
    @responses.activate
    def test_success_status_codes(self, mock_api_key, mock_wallet_address):
        """Test that both 200 and 201 status codes are treated as success."""
        success_response = {"success": True, "data": "test"}

        # Test create_wallet with status 201
        responses.add(
            responses.POST, f"{API_URL}/wallet", json=success_response, status=201
        )
        result = create_wallet(mock_api_key)
        assert result == success_response

        # Test get_balance with status 200
        responses.add(
            responses.GET,
            f"{API_URL}/wallet/balance",
            json=success_response,
            status=200,
        )
        result = get_balance(mock_api_key, mock_wallet_address)
        assert result == success_response

    @pytest.mark.unit
    @patch("crypto_com_developer_platform_client.integrations.wallet_api.requests.post")
    @patch("crypto_com_developer_platform_client.integrations.wallet_api.requests.get")
    def test_timeout_configuration(
        self, mock_get, mock_post, mock_api_key, mock_wallet_address
    ):
        """Test that requests are configured with proper timeout."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "test"}
        mock_get.return_value = mock_response
        mock_post.return_value = mock_response

        create_wallet(mock_api_key)
        get_balance(mock_api_key, mock_wallet_address)

        # Verify timeout is set to 15 seconds for both calls
        mock_post.assert_called_with(
            f"{API_URL}/wallet",
            headers={"Content-Type": "application/json", "x-api-key": mock_api_key},
            timeout=15,
        )
        mock_get.assert_called_with(
            f"{API_URL}/wallet/balance?walletAddress={mock_wallet_address}",
            headers={"Content-Type": "application/json", "x-api-key": mock_api_key},
            timeout=15,
        )

    @pytest.mark.unit
    @responses.activate
    def test_wallet_api_error_status_codes(self, mock_api_key, mock_wallet_address):
        """Test various HTTP error status codes handling."""
        test_cases = [
            (400, "Bad Request"),
            (401, "Unauthorized"),
            (403, "Forbidden"),
            (404, "Not Found"),
            (422, "Unprocessable Entity"),
            (429, "Too Many Requests"),
            (500, "Internal Server Error"),
        ]

        for status_code, error_message in test_cases:
            # Test create_wallet error handling
            responses.reset()
            responses.add(
                responses.POST,
                f"{API_URL}/wallet",
                json={"error": error_message},
                status=status_code,
            )

            with pytest.raises(Exception, match=error_message):
                create_wallet(mock_api_key)

            # Test get_balance error handling
            responses.reset()
            responses.add(
                responses.GET,
                f"{API_URL}/wallet/balance",
                json={"error": error_message},
                status=status_code,
            )

            with pytest.raises(Exception, match=error_message):
                get_balance(mock_api_key, mock_wallet_address)

    @pytest.mark.unit
    @responses.activate
    def test_wallet_address_encoding_in_url(self, mock_api_key):
        """Test proper URL encoding of wallet addresses."""
        # Test with regular address
        address1 = "0x123abc000000000000000000000000000000000"
        responses.add(
            responses.GET,
            f"{API_URL}/wallet/balance",
            json={"success": True},
            status=200,
        )
        get_balance(mock_api_key, address1)
        assert address1 in responses.calls[0].request.url

        responses.reset()

        # Test with Cronos ID containing special characters
        address2 = "test.user.cro"
        responses.add(
            responses.GET,
            f"{API_URL}/wallet/balance",
            json={"success": True},
            status=200,
        )
        get_balance(mock_api_key, address2)
        assert address2 in responses.calls[0].request.url

    @pytest.mark.unit
    def test_api_key_header_validation(self, mock_wallet_address):
        """Test API key header validation with different key formats."""
        with (
            patch(
                "crypto_com_developer_platform_client.integrations.wallet_api.requests.post"
            ) as mock_post,
            patch(
                "crypto_com_developer_platform_client.integrations.wallet_api.requests.get"
            ) as mock_get,
        ):

            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"data": "test"}
            mock_post.return_value = mock_response
            mock_get.return_value = mock_response

            # Test different API key formats
            test_keys = [
                "simple-key",
                "key_with_underscores",
                "key-with-hyphens",
                "UPPERCASE_KEY",
                "mixed_Case_Key-123",
            ]

            for test_key in test_keys:
                create_wallet(test_key)
                args, kwargs = mock_post.call_args
                assert kwargs["headers"]["x-api-key"] == test_key

                get_balance(test_key, mock_wallet_address)
                args, kwargs = mock_get.call_args
                assert kwargs["headers"]["x-api-key"] == test_key
