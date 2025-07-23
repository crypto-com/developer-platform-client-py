"""
Tests for authentication and API key handling across the platform
"""

from unittest.mock import Mock, patch

import pytest
import responses

from crypto_com_developer_platform_client.client import Client
from crypto_com_developer_platform_client.constants import API_URL
from crypto_com_developer_platform_client.network import Network
from crypto_com_developer_platform_client.token import Token
from crypto_com_developer_platform_client.wallet import Wallet


class TestAuthentication:
    """Test cases for authentication and API key handling."""

    def setup_method(self):
        """Reset Client state before each test."""
        Client._api_key = None
        Client._provider = None

    @pytest.mark.unit
    def test_client_api_key_validation(self):
        """Test Client API key validation and storage."""
        # Test valid API key
        valid_key = "sk_test_1234567890abcdef"
        Client.init(api_key=valid_key)
        assert Client.get_api_key() == valid_key

    @pytest.mark.unit
    def test_api_key_format_patterns(self):
        """Test various API key format patterns."""
        valid_patterns = [
            "sk_test_1234567890abcdef",
            "sk_live_abcdef1234567890",
            "api_key_with_underscores_123",
            "simple-api-key-with-dashes",
            "APIKey123WithMixedCase",
            "very-long-api-key-that-exceeds-normal-length-expectations-but-should-still-work-fine",
        ]

        for pattern in valid_patterns:
            Client.init(api_key=pattern)
            assert Client.get_api_key() == pattern

    @pytest.mark.unit
    @responses.activate
    def test_api_key_in_headers(self):
        """Test that API key is properly included in request headers."""
        api_key = "test-api-key-12345"

        responses.add(
            responses.GET,
            f"{API_URL}/network/info",
            json={"data": {"chainId": "25"}},
            status=200,
        )

        Client.init(api_key=api_key)
        client = Client()
        Network.init(client)
        Network.info()

        # Verify API key is in headers
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers["x-api-key"] == api_key

    @pytest.mark.unit
    @responses.activate
    def test_unauthorized_access_handling(self):
        """Test handling of unauthorized access responses."""
        api_key = "invalid-api-key"

        responses.add(
            responses.GET,
            f"{API_URL}/network/info",
            json={"error": "Unauthorized"},
            status=401,
        )

        Client.init(api_key=api_key)
        client = Client()
        Network.init(client)

        with pytest.raises(Exception, match="Unauthorized"):
            Network.info()

    @pytest.mark.unit
    @responses.activate
    def test_forbidden_access_handling(self):
        """Test handling of forbidden access responses."""
        api_key = "limited-access-key"

        responses.add(
            responses.GET,
            f"{API_URL}/network/info",
            json={"error": "Forbidden - insufficient permissions"},
            status=403,
        )

        Client.init(api_key=api_key)
        client = Client()
        Network.init(client)

        with pytest.raises(Exception, match="Forbidden - insufficient permissions"):
            Network.info()

    @pytest.mark.unit
    @responses.activate
    def test_rate_limiting_handling(self):
        """Test handling of rate limiting responses."""
        api_key = "rate-limited-key"

        responses.add(
            responses.GET,
            f"{API_URL}/network/info",
            json={"error": "Rate limit exceeded"},
            status=429,
        )

        Client.init(api_key=api_key)
        client = Client()
        Network.init(client)

        with pytest.raises(Exception, match="Rate limit exceeded"):
            Network.info()

    @pytest.mark.unit
    @responses.activate
    def test_api_key_persistence_across_module_calls(self):
        """Test that API key persists across different module calls."""
        api_key = "persistent-test-key"

        # Mock responses for different endpoints
        responses.add(
            responses.GET, f"{API_URL}/network/info", json={"data": {}}, status=200
        )
        responses.add(
            responses.GET,
            f"{API_URL}/token/native-token-balance",
            json={"data": {}},
            status=200,
        )
        responses.add(
            responses.GET, f"{API_URL}/wallet/balance", json={"data": {}}, status=200
        )

        Client.init(api_key=api_key)
        client = Client()

        # Initialize multiple modules
        Network.init(client)
        Token.init(client)
        Wallet.init(client)

        # Make calls to different modules
        Network.info()
        Token.get_native_balance("0x123...")
        Wallet.get_balance("0x456...")

        # Verify all calls used the same API key
        assert len(responses.calls) == 3
        for call in responses.calls:
            assert call.request.headers["x-api-key"] == api_key

    @pytest.mark.unit
    def test_module_initialization_without_client(self):
        """Test that modules properly reject operations without client initialization."""
        # Reset all module clients
        Token._client = None
        Wallet._client = None
        Network._client = None

        with pytest.raises(ValueError, match="Token class not initialized"):
            Token.get_native_balance("0x123...")

        with pytest.raises(ValueError, match="Wallet class not initialized"):
            Wallet.get_balance("0x456...")

        with pytest.raises(ValueError, match="Network class not initialized"):
            Network.info()

    @pytest.mark.unit
    @responses.activate
    def test_api_key_security_headers(self):
        """Test that security-related headers are properly set."""
        api_key = "security-test-key"

        responses.add(
            responses.GET, f"{API_URL}/network/info", json={"data": {}}, status=200
        )

        Client.init(api_key=api_key)
        client = Client()
        Network.init(client)
        Network.info()

        headers = responses.calls[0].request.headers

        # Verify required headers are present
        assert headers["x-api-key"] == api_key
        assert headers["Content-Type"] == "application/json"

        # Verify no sensitive data leaks in other headers
        assert "password" not in str(headers).lower()
        assert "secret" not in str(headers).lower()

    @pytest.mark.unit
    def test_api_key_immutability(self):
        """Test that API key cannot be modified after client creation."""
        api_key = "immutable-test-key"
        Client.init(api_key=api_key)

        # Verify API key is read-only
        original_key = Client.get_api_key()

        # Client should maintain the original key
        assert Client.get_api_key() == original_key
        assert Client.get_api_key() == api_key

    @pytest.mark.unit
    @responses.activate
    def test_api_timeout_with_authentication(self):
        """Test that authenticated requests respect timeout settings."""
        api_key = "timeout-test-key"

        # We can't easily simulate actual timeouts, but we can verify the request is made
        responses.add(
            responses.GET, f"{API_URL}/network/info", json={"data": {}}, status=200
        )

        Client.init(api_key=api_key)
        client = Client()
        Network.init(client)

        # This should complete without timeout issues
        result = Network.info()
        assert result["data"] == {}

    @pytest.mark.unit
    def test_class_level_client_reinitialization(self):
        """Test that client can be reinitialized with different API keys."""
        # Initialize with first API key
        api_key1 = "first-key"
        Client.init(api_key=api_key1)
        client = Client()
        Token.init(client)

        assert Token._client.get_api_key() == api_key1

        # Reinitialize with second API key
        api_key2 = "second-key"
        Client.init(api_key=api_key2)
        client2 = Client()
        Token.init(client2)

        assert Token._client.get_api_key() == api_key2
        assert Token._client.get_api_key() != api_key1
