from unittest.mock import patch

import pytest
import responses

from crypto_com_developer_platform_client.client import Client
from crypto_com_developer_platform_client.constants import API_URL
from crypto_com_developer_platform_client.exchange import Exchange


class TestExchange:
    """Test cases for the Exchange class."""

    def setup_method(self):
        """Reset state before each test."""
        Exchange._client = None

    @pytest.mark.unit
    def test_init_with_client(self, mock_client):
        """Test Exchange initialization with a Client instance."""
        Exchange.init(mock_client)
        assert Exchange._client == mock_client

    @pytest.mark.unit
    def test_get_all_tickers_without_client(self):
        """Test get_all_tickers without client initialization."""
        Exchange._client = None

        with pytest.raises(
            ValueError, match="Exchange class not initialized with a Client instance"
        ):
            Exchange.get_all_tickers()

    @pytest.mark.unit
    def test_get_ticker_by_instrument_without_client(self):
        """Test get_ticker_by_instrument without client initialization."""
        Exchange._client = None

        with pytest.raises(
            ValueError, match="Exchange class not initialized with a Client instance"
        ):
            Exchange.get_ticker_by_instrument("BTC_USDT")

    @pytest.mark.unit
    @responses.activate
    def test_get_all_tickers_success(self, mock_client):
        """Test successful retrieval of all tickers."""
        expected_response = {
            "success": True,
            "data": [
                {"instrument_name": "BTC_USDT", "last": "50000.00", "change": "2.5"},
                {"instrument_name": "ETH_USDT", "last": "3000.00", "change": "1.8"},
            ],
        }

        responses.add(
            responses.GET,
            f"{API_URL}/exchange/tickers",
            json=expected_response,
            status=200,
        )

        Exchange.init(Client())
        result = Exchange.get_all_tickers()

        assert result == expected_response
        assert len(responses.calls) == 1

    @pytest.mark.unit
    @responses.activate
    def test_get_ticker_by_instrument_success(self, mock_client):
        """Test successful retrieval of ticker by instrument."""
        instrument = "BTC_USDT"
        expected_response = {
            "success": True,
            "data": {
                "instrument_name": instrument,
                "last": "50000.00",
                "bid": "49950.00",
                "ask": "50050.00",
                "change": "2.5",
            },
        }

        responses.add(
            responses.GET,
            f"{API_URL}/exchange/tickers/{instrument}",
            json=expected_response,
            status=200,
        )

        Exchange.init(Client())
        result = Exchange.get_ticker_by_instrument(instrument)

        assert result == expected_response
        assert len(responses.calls) == 1

    @pytest.mark.unit
    def test_get_ticker_by_instrument_invalid_input(self, mock_client):
        """Test get_ticker_by_instrument with invalid input."""
        Exchange.init(mock_client)

        with pytest.raises(ValueError, match="Instrument name is required"):
            Exchange.get_ticker_by_instrument("")

        with pytest.raises(ValueError, match="Instrument name is required"):
            Exchange.get_ticker_by_instrument(None)

    @pytest.mark.unit
    @responses.activate
    def test_get_all_tickers_api_error(self, mock_client):
        """Test get_all_tickers with API error response."""
        error_response = {"error": "Service temporarily unavailable"}

        responses.add(
            responses.GET,
            f"{API_URL}/exchange/tickers",
            json=error_response,
            status=503,
        )

        Exchange.init(Client())

        with pytest.raises(Exception, match="Service temporarily unavailable"):
            Exchange.get_all_tickers()

    @pytest.mark.unit
    @responses.activate
    def test_get_ticker_by_instrument_api_error(self, mock_client):
        """Test get_ticker_by_instrument with API error response."""
        instrument = "INVALID_PAIR"
        error_response = {"error": "Instrument not found"}

        responses.add(
            responses.GET,
            f"{API_URL}/exchange/tickers/{instrument}",
            json=error_response,
            status=404,
        )

        Exchange.init(Client())

        with pytest.raises(Exception, match="Instrument not found"):
            Exchange.get_ticker_by_instrument(instrument)

    @pytest.mark.unit
    def test_exchange_api_integration_with_integrations_module(self, mock_client):
        """Test that Exchange class properly uses integrations.exchange_api functions."""
        Exchange.init(mock_client)

        with patch(
            "crypto_com_developer_platform_client.exchange.get_all_tickers"
        ) as mock_all_tickers:
            mock_all_tickers.return_value = {"tickers": []}
            result = Exchange.get_all_tickers()

            mock_all_tickers.assert_called_once_with(mock_client.get_api_key())
            assert result == {"tickers": []}

        with patch(
            "crypto_com_developer_platform_client.exchange.get_ticker_by_instrument"
        ) as mock_ticker:
            mock_ticker.return_value = {"ticker": {}}
            result = Exchange.get_ticker_by_instrument("BTC_USDT")

            mock_ticker.assert_called_once_with(mock_client.get_api_key(), "BTC_USDT")
            assert result == {"ticker": {}}

    @pytest.mark.unit
    def test_multiple_operations_same_client(self, mock_client):
        """Test multiple Exchange operations with the same client."""
        Exchange.init(mock_client)

        with (
            patch(
                "crypto_com_developer_platform_client.exchange.get_all_tickers"
            ) as mock_all_tickers,
            patch(
                "crypto_com_developer_platform_client.exchange.get_ticker_by_instrument"
            ) as mock_ticker,
        ):

            mock_all_tickers.return_value = {"tickers": []}
            mock_ticker.return_value = {"ticker": {}}

            # Multiple operations
            Exchange.get_all_tickers()
            Exchange.get_ticker_by_instrument("BTC_USDT")
            Exchange.get_ticker_by_instrument("ETH_USDT")

            # Verify call counts
            assert mock_all_tickers.call_count == 1
            assert mock_ticker.call_count == 2
