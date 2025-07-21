"""
Tests for the Network class
"""

from unittest.mock import Mock, patch

import pytest
import responses

from crypto_com_developer_platform_client.client import Client
from crypto_com_developer_platform_client.constants import API_URL
from crypto_com_developer_platform_client.network import Network


class TestNetwork:
    """Test cases for Network class."""

    def setup_method(self):
        """Reset state before each test."""
        Network._client = None

    @pytest.mark.unit
    def test_init_with_client(self, mock_client):
        """Test Network initialization with Client instance."""
        client_instance = Client()
        Network.init(client_instance)

        assert Network._client == client_instance

    @pytest.mark.unit
    def test_info_without_client(self):
        """Test Network.info() raises ValueError when not initialized."""
        with pytest.raises(ValueError, match="Network class not initialized"):
            Network.info()

    @pytest.mark.unit
    def test_chain_id_without_client(self):
        """Test Network.chain_id() raises ValueError when not initialized."""
        with pytest.raises(ValueError, match="Network class not initialized"):
            Network.chain_id()

    @pytest.mark.unit
    def test_client_version_without_client(self):
        """Test Network.client_version() raises ValueError when not initialized."""
        with pytest.raises(ValueError, match="Network class not initialized"):
            Network.client_version()

    @pytest.mark.unit
    @responses.activate
    def test_info_success(self, mock_client, mock_network_info):
        """Test successful network info retrieval."""
        # Mock the API response
        responses.add(
            responses.GET, f"{API_URL}/network/info", json=mock_network_info, status=200
        )

        Network.init(Client())
        result = Network.info()

        assert result == mock_network_info
        assert len(responses.calls) == 1
        assert (
            responses.calls[0].request.headers["x-api-key"] == mock_client.get_api_key()
        )

    @pytest.mark.unit
    @responses.activate
    def test_chain_id_success(self, mock_client):
        """Test successful chain ID retrieval."""
        expected_response = {"success": True, "data": {"chainId": "0x152"}}

        responses.add(
            responses.GET,
            f"{API_URL}/network/chain-id",
            json=expected_response,
            status=200,
        )

        Network.init(Client())
        result = Network.chain_id()

        assert result == expected_response
        assert len(responses.calls) == 1
        assert (
            responses.calls[0].request.headers["x-api-key"] == mock_client.get_api_key()
        )

    @pytest.mark.unit
    @responses.activate
    def test_client_version_success(self, mock_client):
        """Test successful client version retrieval."""
        expected_response = {"success": True, "data": {"version": "v1.2.3"}}

        responses.add(
            responses.GET,
            f"{API_URL}/network/client-version",
            json=expected_response,
            status=200,
        )

        Network.init(Client())
        result = Network.client_version()

        assert result == expected_response
        assert len(responses.calls) == 1
        assert (
            responses.calls[0].request.headers["x-api-key"] == mock_client.get_api_key()
        )

    @pytest.mark.unit
    @responses.activate
    def test_info_api_error(self, mock_client):
        """Test network info with API error response."""
        error_response = {"error": "Unauthorized", "code": "AUTH_ERROR"}

        responses.add(
            responses.GET, f"{API_URL}/network/info", json=error_response, status=401
        )

        Network.init(Client())

        with pytest.raises(Exception, match="Unauthorized"):
            Network.info()

    @pytest.mark.unit
    @responses.activate
    def test_chain_id_api_error(self, mock_client):
        """Test chain ID with API error response."""
        error_response = {"error": "Invalid API key"}

        responses.add(
            responses.GET,
            f"{API_URL}/network/chain-id",
            json=error_response,
            status=403,
        )

        Network.init(Client())

        with pytest.raises(Exception, match="Invalid API key"):
            Network.chain_id()

    @pytest.mark.unit
    @responses.activate
    def test_client_version_api_error(self, mock_client):
        """Test client version with API error response."""
        responses.add(
            responses.GET,
            f"{API_URL}/network/client-version",
            json={"error": "Service unavailable"},
            status=503,
        )

        Network.init(Client())

        with pytest.raises(Exception, match="Service unavailable"):
            Network.client_version()

    @pytest.mark.unit
    @responses.activate
    def test_info_http_error_without_json(self, mock_client):
        """Test network info with HTTP error and no JSON response."""
        responses.add(
            responses.GET,
            f"{API_URL}/network/info",
            body="Internal Server Error",
            status=500,
        )

        Network.init(Client())

        with pytest.raises(Exception, match="HTTP error! status: 500"):
            Network.info()

    @pytest.mark.unit
    @responses.activate
    def test_multiple_calls_same_client(self, mock_client, mock_network_info):
        """Test multiple network calls with the same client instance."""
        responses.add(
            responses.GET, f"{API_URL}/network/info", json=mock_network_info, status=200
        )

        chain_response = {"success": True, "data": {"chainId": "0x152"}}
        responses.add(
            responses.GET,
            f"{API_URL}/network/chain-id",
            json=chain_response,
            status=200,
        )

        Network.init(Client())

        info_result = Network.info()
        chain_result = Network.chain_id()

        assert info_result == mock_network_info
        assert chain_result == chain_response
        assert len(responses.calls) == 2

    @pytest.mark.unit
    def test_network_api_integration_with_integrations_module(self, mock_client):
        """Test that Network class properly uses integrations.network_api functions."""
        Network.init(Client())

        with patch(
            "crypto_com_developer_platform_client.network.get_network_info"
        ) as mock_get_info:
            mock_get_info.return_value = {"mocked": "response"}
            result = Network.info()

            mock_get_info.assert_called_once_with(mock_client.get_api_key())
            assert result == {"mocked": "response"}

        with patch(
            "crypto_com_developer_platform_client.network.get_chain_id"
        ) as mock_get_chain:
            mock_get_chain.return_value = {"chainId": "0x152"}
            result = Network.chain_id()

            mock_get_chain.assert_called_once_with(mock_client.get_api_key())
            assert result == {"chainId": "0x152"}

        with patch(
            "crypto_com_developer_platform_client.network.get_client_version"
        ) as mock_get_version:
            mock_get_version.return_value = {"version": "1.0.0"}
            result = Network.client_version()

            mock_get_version.assert_called_once_with(mock_client.get_api_key())
            assert result == {"version": "1.0.0"}
