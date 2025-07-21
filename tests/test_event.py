from unittest.mock import patch

import pytest
import responses

from crypto_com_developer_platform_client.client import Client
from crypto_com_developer_platform_client.constants import API_URL
from crypto_com_developer_platform_client.event import Event


class TestEvent:
    """Test cases for the Event class."""

    def setup_method(self):
        """Reset state before each test."""
        Event._client = None

    @pytest.mark.unit
    def test_init_with_client(self, mock_client):
        """Test Event initialization with a Client instance."""
        Event.init(mock_client)
        assert Event._client == mock_client

    @pytest.mark.unit
    def test_get_logs_without_client(self):
        """Test get_logs without client initialization."""
        Event._client = None

        with pytest.raises(
            ValueError, match="Event class not initialized with a Client instance"
        ):
            Event.get_logs("0x123...")

    @pytest.mark.unit
    @responses.activate
    def test_get_logs_success(self, mock_client):
        """Test successful event logs retrieval."""
        contract_address = "0x123abc000000000000000000000000000000000"
        expected_response = {
            "success": True,
            "data": {
                "events": [
                    {
                        "event": "Transfer",
                        "address": contract_address,
                        "blockNumber": 1234567,
                        "transactionHash": "0xabc123...",
                    }
                ]
            },
        }

        responses.add(
            responses.GET, f"{API_URL}/events", json=expected_response, status=200
        )

        Event.init(Client())
        result = Event.get_logs(contract_address)

        assert result == expected_response
        assert len(responses.calls) == 1
        assert f"address={contract_address}" in responses.calls[0].request.url

    @pytest.mark.unit
    @responses.activate
    def test_get_logs_api_error(self, mock_client):
        """Test get_logs with API error response."""
        contract_address = "0x123abc000000000000000000000000000000000"
        error_response = {"error": "Contract not found"}

        responses.add(
            responses.GET, f"{API_URL}/events", json=error_response, status=404
        )

        Event.init(Client())

        with pytest.raises(Exception, match="Contract not found"):
            Event.get_logs(contract_address)

    @pytest.mark.unit
    def test_event_api_integration_with_integrations_module(self, mock_client):
        """Test that Event class properly uses integrations.event_api functions."""
        Event.init(mock_client)

        with patch(
            "crypto_com_developer_platform_client.event.get_logs"
        ) as mock_get_logs:
            mock_get_logs.return_value = {"events": []}
            result = Event.get_logs("0x123...")

            mock_get_logs.assert_called_once_with(mock_client.get_api_key(), "0x123...")
            assert result == {"events": []}

    @pytest.mark.unit
    def test_multiple_operations_same_client(self, mock_client):
        """Test multiple Event operations with the same client."""
        Event.init(mock_client)

        with patch(
            "crypto_com_developer_platform_client.event.get_logs"
        ) as mock_get_logs:
            mock_get_logs.return_value = {"events": []}

            # Multiple operations
            Event.get_logs("0x123...")
            Event.get_logs("0x456...")

            # Verify all use the same client
            assert mock_get_logs.call_count == 2

            # Check API key consistency
            for call in mock_get_logs.call_args_list:
                assert call[0][0] == mock_client.get_api_key()

    @pytest.mark.unit
    @responses.activate
    def test_get_logs_with_different_addresses(self, mock_client):
        """Test get_logs with different contract addresses."""
        addresses = [
            "0x123abc000000000000000000000000000000000",
            "0x789012000000000000000000000000000000000",
        ]

        for i, address in enumerate(addresses):
            responses.add(
                responses.GET,
                f"{API_URL}/events",
                json={"events": [{"contractAddress": address}]},
                status=200,
            )

        Event.init(Client())

        for address in addresses:
            result = Event.get_logs(address)
            assert result["events"][0]["contractAddress"] == address
