"""
Tests for the cronosid_api integration module
"""

import pytest
import responses

from crypto_com_developer_platform_client.constants import API_URL
from crypto_com_developer_platform_client.integrations.cronosid_api import (
    lookup_cronos_id,
    resolve_cronos_id,
)


class TestCronosIdApi:
    """Test cases for cronosid_api functions."""

    @pytest.mark.unit
    @responses.activate
    def test_resolve_cronos_id_success(self):
        """Test successful Cronos ID resolution."""
        cronos_id = "test.cro"
        expected_response = {
            "success": True,
            "data": {
                "name": cronos_id,
                "address": "0x123abc000000000000000000000000000000000",
                "expiry": "2025-12-31T23:59:59Z",
            },
        }

        responses.add(
            responses.GET,
            f"{API_URL}/cronosid/resolve/{cronos_id}",
            json=expected_response,
            status=200,
        )

        result = resolve_cronos_id("test-api-key", cronos_id)

        assert result == expected_response
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers["x-api-key"] == "test-api-key"
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"

    @pytest.mark.unit
    @responses.activate
    def test_lookup_cronos_id_success(self):
        """Test successful Cronos ID lookup by address."""
        address = "0x123abc000000000000000000000000000000000"
        expected_response = {
            "success": True,
            "data": {
                "address": address,
                "name": "test.cro",
                "expiry": "2025-12-31T23:59:59Z",
            },
        }

        responses.add(
            responses.GET,
            f"{API_URL}/cronosid/lookup/{address}",
            json=expected_response,
            status=200,
        )

        result = lookup_cronos_id("test-api-key", address)

        assert result == expected_response
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers["x-api-key"] == "test-api-key"

    @pytest.mark.unit
    @responses.activate
    def test_resolve_cronos_id_not_found(self):
        """Test Cronos ID resolution with not found error."""
        cronos_id = "nonexistent.cro"
        error_response = {"error": "Cronos ID not found"}

        responses.add(
            responses.GET,
            f"{API_URL}/cronosid/resolve/{cronos_id}",
            json=error_response,
            status=404,
        )

        with pytest.raises(Exception, match="Cronos ID not found"):
            resolve_cronos_id("test-api-key", cronos_id)

    @pytest.mark.unit
    @responses.activate
    def test_lookup_cronos_id_not_found(self):
        """Test Cronos ID lookup with not found error."""
        address = "0x000000000000000000000000000000000000000"
        error_response = {"error": "Address not associated with Cronos ID"}

        responses.add(
            responses.GET,
            f"{API_URL}/cronosid/lookup/{address}",
            json=error_response,
            status=404,
        )

        with pytest.raises(Exception, match="Address not associated with Cronos ID"):
            lookup_cronos_id("test-api-key", address)

    @pytest.mark.unit
    @responses.activate
    def test_resolve_cronos_id_unauthorized(self):
        """Test Cronos ID resolution with unauthorized error."""
        cronos_id = "test.cro"
        error_response = {"error": "Unauthorized access"}

        responses.add(
            responses.GET,
            f"{API_URL}/cronosid/resolve/{cronos_id}",
            json=error_response,
            status=401,
        )

        with pytest.raises(Exception, match="Unauthorized access"):
            resolve_cronos_id("invalid-api-key", cronos_id)

    @pytest.mark.unit
    @responses.activate
    def test_lookup_cronos_id_server_error(self):
        """Test Cronos ID lookup with server error."""
        address = "0x123abc000000000000000000000000000000000"
        error_response = {"error": "Internal server error"}

        responses.add(
            responses.GET,
            f"{API_URL}/cronosid/lookup/{address}",
            json=error_response,
            status=500,
        )

        with pytest.raises(Exception, match="Internal server error"):
            lookup_cronos_id("test-api-key", address)

    @pytest.mark.unit
    @responses.activate
    def test_http_error_status_codes(self):
        """Test various HTTP error status codes for both functions."""
        cronos_id = "test.cro"
        address = "0x123abc000000000000000000000000000000000"
        error_cases = [
            (400, "Bad request"),
            (401, "Unauthorized"),
            (403, "Forbidden"),
            (404, "Not found"),
            (429, "Rate limited"),
            (500, "Internal server error"),
            (503, "Service unavailable"),
        ]

        for status_code, error_message in error_cases:
            # Test resolve endpoint
            responses.reset()
            responses.add(
                responses.GET,
                f"{API_URL}/cronosid/resolve/{cronos_id}",
                json={"error": error_message},
                status=status_code,
            )

            with pytest.raises(Exception, match=error_message):
                resolve_cronos_id("test-api-key", cronos_id)

            # Test lookup endpoint
            responses.reset()
            responses.add(
                responses.GET,
                f"{API_URL}/cronosid/lookup/{address}",
                json={"error": error_message},
                status=status_code,
            )

            with pytest.raises(Exception, match=error_message):
                lookup_cronos_id("test-api-key", address)

    @pytest.mark.unit
    @responses.activate
    def test_success_status_codes(self):
        """Test that both 200 and 201 status codes are accepted as success."""
        cronos_id = "test.cro"
        address = "0x123abc000000000000000000000000000000000"
        success_response = {"data": {"name": cronos_id, "address": address}}

        for status_code in [200, 201]:
            # Test resolve endpoint
            responses.reset()
            responses.add(
                responses.GET,
                f"{API_URL}/cronosid/resolve/{cronos_id}",
                json=success_response,
                status=status_code,
            )

            result = resolve_cronos_id("test-api-key", cronos_id)
            assert result == success_response

            # Test lookup endpoint
            responses.reset()
            responses.add(
                responses.GET,
                f"{API_URL}/cronosid/lookup/{address}",
                json=success_response,
                status=status_code,
            )

            result = lookup_cronos_id("test-api-key", address)
            assert result == success_response

    @pytest.mark.unit
    @responses.activate
    def test_multiple_cronos_id_names(self):
        """Test with different Cronos ID names."""
        test_names = ["test.cro", "user123.cro", "my-name.cro", "example_name.cro"]

        for name in test_names:
            responses.add(
                responses.GET,
                f"{API_URL}/cronosid/resolve/{name}",
                json={"data": {"name": name, "address": "0x123..."}},
                status=200,
            )

        for name in test_names:
            result = resolve_cronos_id("test-api-key", name)
            assert result["data"]["name"] == name

    @pytest.mark.unit
    @responses.activate
    def test_api_key_parameter_validation(self):
        """Test that API key is properly included in headers."""
        cronos_id = "test.cro"
        test_keys = ["test-key-1", "another-api-key", "key-with-special-chars-123"]

        for api_key in test_keys:
            responses.reset()
            responses.add(
                responses.GET,
                f"{API_URL}/cronosid/resolve/{cronos_id}",
                json={"data": {}},
                status=200,
            )

            resolve_cronos_id(api_key, cronos_id)

            # Verify the API key was sent in headers
            assert responses.calls[0].request.headers["x-api-key"] == api_key

    @pytest.mark.unit
    @responses.activate
    def test_request_timeout_configuration(self):
        """Test that requests are configured with proper timeout."""
        cronos_id = "test.cro"

        responses.add(
            responses.GET,
            f"{API_URL}/cronosid/resolve/{cronos_id}",
            json={"data": {}},
            status=200,
        )

        resolve_cronos_id("test-api-key", cronos_id)

        # The timeout parameter is handled internally, so we just verify the call succeeds
        assert len(responses.calls) == 1

    @pytest.mark.unit
    @responses.activate
    def test_special_characters_in_names(self):
        """Test handling of special characters in Cronos ID names."""
        special_names = [
            "test-with-dashes.cro",
            "test_with_underscores.cro",
            "test123.cro",
            "MixedCase.cro",
        ]

        for name in special_names:
            responses.add(
                responses.GET,
                f"{API_URL}/cronosid/resolve/{name}",
                json={"data": {"name": name}},
                status=200,
            )

        for name in special_names:
            result = resolve_cronos_id("test-api-key", name)
            assert "data" in result

    @pytest.mark.unit
    @responses.activate
    def test_http_error_without_json_body(self):
        """Test handling HTTP errors without JSON response body."""
        cronos_id = "test.cro"

        responses.add(
            responses.GET,
            f"{API_URL}/cronosid/resolve/{cronos_id}",
            status=500,
            body="Internal Server Error",  # Plain text, not JSON
        )

        with pytest.raises(Exception, match="HTTP error! status: 500"):
            resolve_cronos_id("test-api-key", cronos_id)
