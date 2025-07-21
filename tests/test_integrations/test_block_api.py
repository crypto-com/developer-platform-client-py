"""
Tests for the block_api integration module
"""

import pytest
import responses

from crypto_com_developer_platform_client.constants import API_URL
from crypto_com_developer_platform_client.integrations.block_api import (
    get_block_by_tag,
    get_current_block,
)


class TestBlockApi:
    """Test cases for block_api functions."""

    @pytest.mark.unit
    @responses.activate
    def test_get_current_block_success(self):
        """Test successful current block retrieval."""
        expected_response = {
            "success": True,
            "data": {
                "number": "0x12d687",
                "hash": "0x456def000000000000000000000000000000000000000000000000000000",
                "timestamp": "0x123abc",
                "transactions": [],
            },
        }

        responses.add(
            responses.GET,
            f"{API_URL}/block/current-block",
            json=expected_response,
            status=200,
        )

        result = get_current_block("test-api-key")

        assert result == expected_response
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers["x-api-key"] == "test-api-key"
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"

    @pytest.mark.unit
    @responses.activate
    def test_get_block_by_tag_success(self):
        """Test successful block retrieval by tag."""
        block_tag = "latest"
        tx_detail = "full"
        expected_response = {
            "success": True,
            "data": {
                "number": "0x12d687",
                "hash": "0x456def000000000000000000000000000000000000000000000000000000",
                "timestamp": "0x123abc",
                "transactions": [],
            },
        }

        responses.add(
            responses.GET,
            f"{API_URL}/block/block-tag",
            json=expected_response,
            status=200,
        )

        result = get_block_by_tag("test-api-key", block_tag, tx_detail)

        assert result == expected_response
        assert len(responses.calls) == 1
        assert f"blockTag={block_tag}" in responses.calls[0].request.url
        assert f"txDetail={tx_detail}" in responses.calls[0].request.url

    @pytest.mark.unit
    @responses.activate
    def test_get_current_block_api_error(self):
        """Test current block with API error response."""
        error_response = {"error": "Service temporarily unavailable"}

        responses.add(
            responses.GET,
            f"{API_URL}/block/current-block",
            json=error_response,
            status=503,
        )

        with pytest.raises(Exception, match="Service temporarily unavailable"):
            get_current_block("test-api-key")

    @pytest.mark.unit
    @responses.activate
    def test_get_block_by_tag_invalid_tag(self):
        """Test block by tag with invalid tag error."""
        invalid_tag = "invalid"
        tx_detail = "full"
        error_response = {"error": "Invalid block tag"}

        responses.add(
            responses.GET, f"{API_URL}/block/block-tag", json=error_response, status=400
        )

        with pytest.raises(Exception, match="Invalid block tag"):
            get_block_by_tag("test-api-key", invalid_tag, tx_detail)

    @pytest.mark.unit
    @responses.activate
    def test_http_error_status_codes(self):
        """Test various HTTP error status codes."""
        error_cases = [
            (400, "Bad request"),
            (401, "Unauthorized"),
            (404, "Not found"),
            (500, "Internal server error"),
        ]

        for status_code, error_message in error_cases:
            responses.reset()
            responses.add(
                responses.GET,
                f"{API_URL}/block/current-block",
                json={"error": error_message},
                status=status_code,
            )

            with pytest.raises(Exception, match=error_message):
                get_current_block("test-api-key")

    @pytest.mark.unit
    @responses.activate
    def test_success_status_codes(self):
        """Test that both 200 and 201 status codes are accepted as success."""
        success_response = {"data": {"number": "0x123"}}

        for status_code in [200, 201]:
            responses.reset()
            responses.add(
                responses.GET,
                f"{API_URL}/block/current-block",
                json=success_response,
                status=status_code,
            )

            result = get_current_block("test-api-key")
            assert result == success_response

    @pytest.mark.unit
    @responses.activate
    def test_api_key_parameter_validation(self):
        """Test that API key is properly included in headers."""
        test_keys = ["test-key-1", "another-api-key", "key-with-special-chars-123"]

        for api_key in test_keys:
            responses.reset()
            responses.add(
                responses.GET,
                f"{API_URL}/block/current-block",
                json={"data": {}},
                status=200,
            )

            get_current_block(api_key)

            assert responses.calls[0].request.headers["x-api-key"] == api_key
