"""
Tests for network_api integration module
"""

from unittest.mock import Mock, patch

import pytest
import requests
import responses

from crypto_com_developer_platform_client.constants import API_URL
from crypto_com_developer_platform_client.integrations.network_api import (
    get_chain_id,
    get_client_version,
    get_network_info,
)


class TestNetworkApi:
    """Test cases for network API functions."""

    @pytest.mark.unit
    @responses.activate
    def test_get_network_info_success(self, mock_api_key):
        """Test successful network info retrieval."""
        expected_response = {
            "success": True,
            "data": {"name": "Cronos", "chainId": 25, "isTestnet": False},
        }

        responses.add(
            responses.GET, f"{API_URL}/network/info", json=expected_response, status=200
        )

        result = get_network_info(mock_api_key)

        assert result == expected_response

    @pytest.mark.unit
    @responses.activate
    def test_get_chain_id_success(self, mock_api_key):
        """Test successful chain ID retrieval."""
        expected_response = {"success": True, "data": {"chainId": 25}}

        responses.add(
            responses.GET,
            f"{API_URL}/network/chain-id",
            json=expected_response,
            status=200,
        )

        result = get_chain_id(mock_api_key)

        assert result == expected_response

    @pytest.mark.unit
    @responses.activate
    def test_get_client_version_success(self, mock_api_key):
        """Test successful client version retrieval."""
        expected_response = {"success": True, "data": {"version": "v1.2.3"}}

        responses.add(
            responses.GET,
            f"{API_URL}/network/client-version",
            json=expected_response,
            status=200,
        )

        result = get_client_version(mock_api_key)

        assert result == expected_response

    @pytest.mark.unit
    @responses.activate
    def test_get_network_info_api_error(self, mock_api_key):
        """Test network info API error handling."""
        responses.add(
            responses.GET,
            f"{API_URL}/network/info",
            json={"error": "Invalid API key"},
            status=401,
        )

        with pytest.raises(Exception, match="Invalid API key"):
            get_network_info(mock_api_key)

    @pytest.mark.unit
    @responses.activate
    def test_get_chain_id_http_error_without_json(self, mock_api_key):
        """Test chain ID with HTTP error and no JSON response."""
        responses.add(
            responses.GET,
            f"{API_URL}/network/chain-id",
            body="Unauthorized",
            status=401,
        )

        with pytest.raises(Exception, match="HTTP error! status: 401"):
            get_chain_id(mock_api_key)

    @pytest.mark.unit
    @responses.activate
    def test_get_client_version_timeout_handling(self, mock_api_key):
        """Test client version timeout error handling."""
        responses.add(
            responses.GET,
            f"{API_URL}/network/client-version",
            json={"error": "Request timeout"},
            status=408,
        )

        with pytest.raises(Exception, match="Request timeout"):
            get_client_version(mock_api_key)

    @pytest.mark.unit
    @responses.activate
    def test_all_endpoints_use_correct_headers(self, mock_api_key):
        """Test that all network endpoints use correct headers."""
        expected_headers = {
            "Content-Type": "application/json",
            "x-api-key": mock_api_key,
        }

        # Mock each endpoint
        for endpoint in [
            "/network/info",
            "/network/chain-id",
            "/network/client-version",
        ]:
            responses.add(
                responses.GET,
                f"{API_URL}{endpoint}",
                json={"success": True},
                status=200,
            )

        # Call each function
        get_network_info(mock_api_key)
        get_chain_id(mock_api_key)
        get_client_version(mock_api_key)

        # Verify headers for each call
        for call in responses.calls:
            for key, value in expected_headers.items():
                assert call.request.headers[key] == value

    @pytest.mark.unit
    @responses.activate
    def test_network_api_error_status_codes(self, mock_api_key):
        """Test various HTTP error status codes."""
        error_codes = [400, 401, 403, 404, 500, 502, 503]

        for status_code in error_codes:
            responses.reset()
            responses.add(
                responses.GET,
                f"{API_URL}/network/info",
                json={"error": f"HTTP {status_code} error"},
                status=status_code,
            )

            with pytest.raises(Exception, match=f"HTTP {status_code} error"):
                get_network_info(mock_api_key)

    @pytest.mark.unit
    @responses.activate
    def test_success_status_codes(self, mock_api_key):
        """Test that both 200 and 201 are treated as success."""
        success_codes = [200, 201]
        expected_response = {"success": True, "data": {}}

        for status_code in success_codes:
            responses.reset()
            responses.add(
                responses.GET,
                f"{API_URL}/network/info",
                json=expected_response,
                status=status_code,
            )

            result = get_network_info(mock_api_key)
            assert result == expected_response

    @pytest.mark.unit
    @patch("crypto_com_developer_platform_client.integrations.network_api.requests.get")
    def test_requests_timeout_configuration(self, mock_get, mock_api_key):
        """Test that requests are configured with proper timeout."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "test"}
        mock_get.return_value = mock_response

        get_network_info(mock_api_key)

        # Verify timeout is set to 15 seconds
        mock_get.assert_called_with(
            f"{API_URL}/network/info",
            headers={"Content-Type": "application/json", "x-api-key": mock_api_key},
            timeout=15,
        )

    @pytest.mark.unit
    def test_api_key_parameter_validation(self):
        """Test behavior with different API key types."""
        with patch(
            "crypto_com_developer_platform_client.integrations.network_api.requests.get"
        ) as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"data": "test"}
            mock_get.return_value = mock_response

            # Test with regular string API key
            get_network_info("regular-api-key")
            mock_get.assert_called_with(
                f"{API_URL}/network/info",
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": "regular-api-key",
                },
                timeout=15,
            )
