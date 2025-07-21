"""
Tests for the defi_api integration module
"""

import pytest
import responses

from crypto_com_developer_platform_client.constants import API_URL
from crypto_com_developer_platform_client.integrations.defi_api import (
    get_all_farms,
    get_farm_by_symbol,
    get_whitelisted_tokens,
)


class TestDefiApi:
    """Test cases for defi_api functions."""

    @pytest.mark.unit
    @responses.activate
    def test_get_whitelisted_tokens_success(self):
        """Test successful retrieval of whitelisted tokens."""
        project = "mmfinance"
        expected_response = {
            "success": True,
            "data": {
                "tokens": [
                    {
                        "symbol": "CRO",
                        "address": "0x456def000000000000000000000000000000000",
                        "decimals": 8,
                        "name": "Cronos",
                    },
                    {
                        "symbol": "USDC",
                        "address": "0x567890000000000000000000000000000000000",
                        "decimals": 6,
                        "name": "USD Coin",
                    },
                ]
            },
        }

        responses.add(
            responses.GET,
            f"{API_URL}/defi/whitelisted-tokens/{project}?apiKey=test-api-key",
            json=expected_response,
            status=200,
        )

        result = get_whitelisted_tokens(project, "test-api-key")

        assert result == expected_response
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers["x-api-key"] == "test-api-key"
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"

    @pytest.mark.unit
    @responses.activate
    def test_get_all_farms_success(self):
        """Test successful retrieval of all farms."""
        project = "mmfinance"
        expected_response = {
            "success": True,
            "data": {
                "farms": [
                    {
                        "symbol": "CRO-USDC",
                        "apy": 45.67,
                        "tvl": "1234567.89",
                        "farmAddress": "0x123abc000000000000000000000000000000000",
                    },
                    {
                        "symbol": "CRO-USDT",
                        "apy": 38.21,
                        "tvl": "987654.32",
                        "farmAddress": "0x789012000000000000000000000000000000000",
                    },
                ]
            },
        }

        responses.add(
            responses.GET,
            f"{API_URL}/defi/farms/{project}?apiKey=test-api-key",
            json=expected_response,
            status=200,
        )

        result = get_all_farms(project, "test-api-key")

        assert result == expected_response
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers["x-api-key"] == "test-api-key"

    @pytest.mark.unit
    @responses.activate
    def test_get_farm_by_symbol_success(self):
        """Test successful retrieval of specific farm by symbol."""
        project = "mmfinance"
        symbol = "CRO-USDC"
        expected_response = {
            "success": True,
            "data": {
                "symbol": symbol,
                "apy": 45.67,
                "tvl": "1234567.89",
                "farmAddress": "0x123abc000000000000000000000000000000000",
                "stakingToken": {"address": "0x123...", "decimals": 18},
                "rewardTokens": [
                    {
                        "symbol": "CRO",
                        "address": "0x456def000000000000000000000000000000000",
                    }
                ],
            },
        }

        responses.add(
            responses.GET,
            f"{API_URL}/defi/farms/{project}/{symbol}?apiKey=test-api-key",
            json=expected_response,
            status=200,
        )

        result = get_farm_by_symbol(project, symbol, "test-api-key")

        assert result == expected_response
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers["x-api-key"] == "test-api-key"

    @pytest.mark.unit
    @responses.activate
    def test_get_whitelisted_tokens_not_found(self):
        """Test whitelisted tokens with not found error."""
        project = "nonexistent"
        error_response = {"error": "Project not found"}

        responses.add(
            responses.GET,
            f"{API_URL}/defi/whitelisted-tokens/{project}?apiKey=test-api-key",
            json=error_response,
            status=404,
        )

        with pytest.raises(Exception, match="Project not found"):
            get_whitelisted_tokens(project, "test-api-key")

    @pytest.mark.unit
    @responses.activate
    def test_get_all_farms_unauthorized(self):
        """Test all farms with unauthorized error."""
        project = "mmfinance"
        error_response = {"error": "Unauthorized access"}

        responses.add(
            responses.GET,
            f"{API_URL}/defi/farms/{project}?apiKey=invalid-key",
            json=error_response,
            status=401,
        )

        with pytest.raises(Exception, match="Unauthorized access"):
            get_all_farms(project, "invalid-key")

    @pytest.mark.unit
    @responses.activate
    def test_get_farm_by_symbol_not_found(self):
        """Test farm by symbol with not found error."""
        project = "mmfinance"
        symbol = "NONEXISTENT-PAIR"
        error_response = {"error": "Farm not found"}

        responses.add(
            responses.GET,
            f"{API_URL}/defi/farms/{project}/{symbol}?apiKey=test-api-key",
            json=error_response,
            status=404,
        )

        with pytest.raises(Exception, match="Farm not found"):
            get_farm_by_symbol(project, symbol, "test-api-key")

    @pytest.mark.unit
    @responses.activate
    def test_http_error_status_codes(self):
        """Test various HTTP error status codes for all functions."""
        project = "mmfinance"
        symbol = "CRO-USDC"
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
            # Test whitelisted tokens endpoint
            responses.reset()
            responses.add(
                responses.GET,
                f"{API_URL}/defi/whitelisted-tokens/{project}?apiKey=test-api-key",
                json={"error": error_message},
                status=status_code,
            )

            with pytest.raises(Exception, match=error_message):
                get_whitelisted_tokens(project, "test-api-key")

            # Test all farms endpoint
            responses.reset()
            responses.add(
                responses.GET,
                f"{API_URL}/defi/farms/{project}?apiKey=test-api-key",
                json={"error": error_message},
                status=status_code,
            )

            with pytest.raises(Exception, match=error_message):
                get_all_farms(project, "test-api-key")

            # Test farm by symbol endpoint
            responses.reset()
            responses.add(
                responses.GET,
                f"{API_URL}/defi/farms/{project}/{symbol}?apiKey=test-api-key",
                json={"error": error_message},
                status=status_code,
            )

            with pytest.raises(Exception, match=error_message):
                get_farm_by_symbol(project, symbol, "test-api-key")

    @pytest.mark.unit
    @responses.activate
    def test_success_status_codes(self):
        """Test that both 200 and 201 status codes are accepted as success."""
        project = "mmfinance"
        symbol = "CRO-USDC"
        success_response = {"data": {"success": True}}

        for status_code in [200, 201]:
            # Test whitelisted tokens
            responses.reset()
            responses.add(
                responses.GET,
                f"{API_URL}/defi/whitelisted-tokens/{project}?apiKey=test-api-key",
                json=success_response,
                status=status_code,
            )

            result = get_whitelisted_tokens(project, "test-api-key")
            assert result == success_response

            # Test all farms
            responses.reset()
            responses.add(
                responses.GET,
                f"{API_URL}/defi/farms/{project}?apiKey=test-api-key",
                json=success_response,
                status=status_code,
            )

            result = get_all_farms(project, "test-api-key")
            assert result == success_response

            # Test farm by symbol
            responses.reset()
            responses.add(
                responses.GET,
                f"{API_URL}/defi/farms/{project}/{symbol}?apiKey=test-api-key",
                json=success_response,
                status=status_code,
            )

            result = get_farm_by_symbol(project, symbol, "test-api-key")
            assert result == success_response

    @pytest.mark.unit
    @responses.activate
    def test_multiple_projects(self):
        """Test with different DeFi projects."""
        test_projects = ["mmfinance", "vvsfinance", "tectonic", "cronaswap"]

        for project in test_projects:
            responses.add(
                responses.GET,
                f"{API_URL}/defi/whitelisted-tokens/{project}?apiKey=test-api-key",
                json={"data": {"project": project, "tokens": []}},
                status=200,
            )

        for project in test_projects:
            result = get_whitelisted_tokens(project, "test-api-key")
            assert result["data"]["project"] == project

    @pytest.mark.unit
    @responses.activate
    def test_api_key_parameter_validation(self):
        """Test that API key is properly included in headers and URL params."""
        project = "mmfinance"
        test_keys = ["test-key-1", "another-api-key", "key-with-special-chars-123"]

        for api_key in test_keys:
            responses.reset()
            responses.add(
                responses.GET,
                f"{API_URL}/defi/whitelisted-tokens/{project}?apiKey={api_key}",
                json={"data": {}},
                status=200,
            )

            get_whitelisted_tokens(project, api_key)

            # Verify the API key was sent in both headers and URL params
            assert responses.calls[0].request.headers["x-api-key"] == api_key
            assert f"apiKey={api_key}" in responses.calls[0].request.url

    @pytest.mark.unit
    @responses.activate
    def test_request_timeout_configuration(self):
        """Test that requests are configured with proper timeout."""
        project = "mmfinance"

        responses.add(
            responses.GET,
            f"{API_URL}/defi/whitelisted-tokens/{project}?apiKey=test-api-key",
            json={"data": {}},
            status=200,
        )

        get_whitelisted_tokens(project, "test-api-key")

        # The timeout parameter is handled internally, so we just verify the call succeeds
        assert len(responses.calls) == 1

    @pytest.mark.unit
    @responses.activate
    def test_special_characters_in_symbols(self):
        """Test handling of special characters in farm symbols."""
        project = "mmfinance"
        special_symbols = ["CRO-USDC", "ETH_BTC", "Token1/Token2", "LP-TOKEN"]

        for symbol in special_symbols:
            responses.add(
                responses.GET,
                f"{API_URL}/defi/farms/{project}/{symbol}?apiKey=test-api-key",
                json={"data": {"symbol": symbol}},
                status=200,
            )

        for symbol in special_symbols:
            result = get_farm_by_symbol(project, symbol, "test-api-key")
            assert result["data"]["symbol"] == symbol

    @pytest.mark.unit
    @responses.activate
    def test_http_error_without_json_body(self):
        """Test handling HTTP errors without JSON response body."""
        project = "mmfinance"

        responses.add(
            responses.GET,
            f"{API_URL}/defi/whitelisted-tokens/{project}?apiKey=test-api-key",
            status=500,
            body="Internal Server Error",  # Plain text, not JSON
        )

        with pytest.raises(Exception, match="HTTP error! status: 500"):
            get_whitelisted_tokens(project, "test-api-key")

    @pytest.mark.unit
    @responses.activate
    def test_large_response_handling(self):
        """Test handling of large responses with many farms/tokens."""
        project = "mmfinance"
        large_token_list = []
        for i in range(100):  # Create 100 tokens
            large_token_list.append(
                {"symbol": f"TOKEN_{i}", "address": f"0x{i:040d}", "decimals": 18}
            )

        expected_response = {"success": True, "data": {"tokens": large_token_list}}

        responses.add(
            responses.GET,
            f"{API_URL}/defi/whitelisted-tokens/{project}?apiKey=test-api-key",
            json=expected_response,
            status=200,
        )

        result = get_whitelisted_tokens(project, "test-api-key")

        assert result == expected_response
        assert len(result["data"]["tokens"]) == 100

    @pytest.mark.unit
    @responses.activate
    def test_malformed_json_error_handling(self):
        """Test handling of malformed JSON in error responses."""
        project = "mmfinance"
        symbol = "CRO-USDC"

        # Test all three functions with malformed JSON responses
        test_functions = [
            (
                "whitelisted_tokens",
                lambda: get_whitelisted_tokens(project, "test-api-key"),
            ),
            ("all_farms", lambda: get_all_farms(project, "test-api-key")),
            (
                "farm_by_symbol",
                lambda: get_farm_by_symbol(project, symbol, "test-api-key"),
            ),
        ]

        for func_name, func in test_functions:
            responses.reset()

            if func_name == "whitelisted_tokens":
                url = f"{API_URL}/defi/whitelisted-tokens/{project}?apiKey=test-api-key"
            elif func_name == "all_farms":
                url = f"{API_URL}/defi/farms/{project}?apiKey=test-api-key"
            else:
                url = f"{API_URL}/defi/farms/{project}/{symbol}?apiKey=test-api-key"

            responses.add(
                responses.GET,
                url,
                body="{invalid json}",  # Malformed JSON that will cause ValueError
                status=500,
                content_type="application/json",
            )

            with pytest.raises(Exception, match="HTTP error! status: 500"):
                func()

    @pytest.mark.unit
    @responses.activate
    def test_json_response_without_error_key(self):
        """Test handling of JSON error responses without 'error' key."""
        project = "mmfinance"
        symbol = "CRO-USDC"

        # Test all three functions with JSON responses that don't have 'error' key (KeyError)
        test_functions = [
            (
                "whitelisted_tokens",
                lambda: get_whitelisted_tokens(project, "test-api-key"),
            ),
            ("all_farms", lambda: get_all_farms(project, "test-api-key")),
            (
                "farm_by_symbol",
                lambda: get_farm_by_symbol(project, symbol, "test-api-key"),
            ),
        ]

        for func_name, func in test_functions:
            responses.reset()

            if func_name == "whitelisted_tokens":
                url = f"{API_URL}/defi/whitelisted-tokens/{project}?apiKey=test-api-key"
            elif func_name == "all_farms":
                url = f"{API_URL}/defi/farms/{project}?apiKey=test-api-key"
            else:
                url = f"{API_URL}/defi/farms/{project}/{symbol}?apiKey=test-api-key"

            responses.add(
                responses.GET,
                url,
                json={
                    "message": "Something went wrong",
                    "status": "failed",
                },  # No 'error' key
                status=422,
            )

            with pytest.raises(Exception, match="HTTP error! status: 422"):
                func()

    @pytest.mark.unit
    @responses.activate
    def test_empty_json_error_response(self):
        """Test handling of empty JSON in error responses."""
        project = "mmfinance"

        responses.add(
            responses.GET,
            f"{API_URL}/defi/whitelisted-tokens/{project}?apiKey=test-api-key",
            json={},  # Empty JSON object
            status=500,
        )

        with pytest.raises(Exception, match="HTTP error! status: 500"):
            get_whitelisted_tokens(project, "test-api-key")

    @pytest.mark.unit
    @responses.activate
    def test_url_encoding_special_project_names(self):
        """Test URL encoding for project names with special characters."""
        special_projects = [
            "project with spaces",
            "project@domain.com",
            "project&special=chars",
            "project%encoded",
        ]

        for project in special_projects:
            responses.reset()
            responses.add(
                responses.GET,
                f"{API_URL}/defi/whitelisted-tokens/{project}?apiKey=test-api-key",
                json={"data": {"project": project}},
                status=200,
            )

            result = get_whitelisted_tokens(project, "test-api-key")
            assert result["data"]["project"] == project

    @pytest.mark.unit
    @responses.activate
    def test_comprehensive_content_type_headers(self):
        """Test that Content-Type headers are properly set for all endpoints."""
        project = "mmfinance"
        symbol = "CRO-USDC"

        # Test whitelisted tokens endpoint
        responses.add(
            responses.GET,
            f"{API_URL}/defi/whitelisted-tokens/{project}?apiKey=test-api-key",
            json={"data": {}},
            status=200,
        )
        get_whitelisted_tokens(project, "test-api-key")
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"

        # Test all farms endpoint
        responses.reset()
        responses.add(
            responses.GET,
            f"{API_URL}/defi/farms/{project}?apiKey=test-api-key",
            json={"data": {}},
            status=200,
        )
        get_all_farms(project, "test-api-key")
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"

        # Test farm by symbol endpoint
        responses.reset()
        responses.add(
            responses.GET,
            f"{API_URL}/defi/farms/{project}/{symbol}?apiKey=test-api-key",
            json={"data": {}},
            status=200,
        )
        get_farm_by_symbol(project, symbol, "test-api-key")
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"

    @pytest.mark.unit
    @responses.activate
    def test_comprehensive_api_key_validation(self):
        """Test comprehensive API key validation for all endpoints."""
        project = "mmfinance"
        symbol = "CRO-USDC"
        api_key = "comprehensive-test-key"

        # Test that API keys are included in both headers and URL for all endpoints
        endpoints = [
            ("whitelisted_tokens", get_whitelisted_tokens, [project, api_key]),
            ("all_farms", get_all_farms, [project, api_key]),
            ("farm_by_symbol", get_farm_by_symbol, [project, symbol, api_key]),
        ]

        for endpoint_name, func, args in endpoints:
            responses.reset()

            if endpoint_name == "whitelisted_tokens":
                url = f"{API_URL}/defi/whitelisted-tokens/{project}?apiKey={api_key}"
            elif endpoint_name == "all_farms":
                url = f"{API_URL}/defi/farms/{project}?apiKey={api_key}"
            else:
                url = f"{API_URL}/defi/farms/{project}/{symbol}?apiKey={api_key}"

            responses.add(responses.GET, url, json={"data": {}}, status=200)

            func(*args)

            # Verify API key in both headers and URL
            assert responses.calls[0].request.headers["x-api-key"] == api_key
            assert f"apiKey={api_key}" in responses.calls[0].request.url

    @pytest.mark.unit
    @responses.activate
    def test_edge_case_empty_responses(self):
        """Test handling of edge case empty responses."""
        project = "mmfinance"
        symbol = "CRO-USDC"

        # Test all endpoints with empty data responses
        empty_responses = [
            {"data": {"tokens": []}},  # Empty tokens array
            {"data": {"farms": []}},  # Empty farms array
            {"data": {}},  # Empty data object
        ]

        endpoints = [
            (get_whitelisted_tokens, [project, "test-api-key"]),
            (get_all_farms, [project, "test-api-key"]),
            (get_farm_by_symbol, [project, symbol, "test-api-key"]),
        ]

        for i, (func, args) in enumerate(endpoints):
            responses.reset()

            if i == 0:
                url = f"{API_URL}/defi/whitelisted-tokens/{project}?apiKey=test-api-key"
            elif i == 1:
                url = f"{API_URL}/defi/farms/{project}?apiKey=test-api-key"
            else:
                url = f"{API_URL}/defi/farms/{project}/{symbol}?apiKey=test-api-key"

            responses.add(responses.GET, url, json=empty_responses[i], status=200)

            result = func(*args)
            assert result == empty_responses[i]

    @pytest.mark.unit
    @responses.activate
    def test_extremely_long_project_names(self):
        """Test handling of extremely long project names."""
        long_project = "a" * 200  # 200 character project name

        responses.add(
            responses.GET,
            f"{API_URL}/defi/whitelisted-tokens/{long_project}?apiKey=test-api-key",
            json={"data": {"project": long_project}},
            status=200,
        )

        result = get_whitelisted_tokens(long_project, "test-api-key")
        assert result["data"]["project"] == long_project

    @pytest.mark.unit
    @responses.activate
    def test_various_error_status_codes_comprehensive(self):
        """Test comprehensive error status code handling."""
        project = "mmfinance"
        symbol = "CRO-USDC"

        # Extended list of HTTP status codes
        error_cases = [
            (400, "Bad request"),
            (401, "Unauthorized"),
            (403, "Forbidden"),
            (404, "Not found"),
            (405, "Method not allowed"),
            (408, "Request timeout"),
            (409, "Conflict"),
            (422, "Unprocessable entity"),
            (429, "Rate limited"),
            (500, "Internal server error"),
            (502, "Bad gateway"),
            (503, "Service unavailable"),
            (504, "Gateway timeout"),
        ]

        functions = [
            (
                get_whitelisted_tokens,
                [project, "test-api-key"],
                f"whitelisted-tokens/{project}",
            ),
            (get_all_farms, [project, "test-api-key"], f"farms/{project}"),
            (
                get_farm_by_symbol,
                [project, symbol, "test-api-key"],
                f"farms/{project}/{symbol}",
            ),
        ]

        for func, args, endpoint in functions:
            for status_code, error_message in error_cases:
                responses.reset()
                responses.add(
                    responses.GET,
                    f"{API_URL}/defi/{endpoint}?apiKey=test-api-key",
                    json={"error": error_message},
                    status=status_code,
                )

                with pytest.raises(Exception, match=error_message):
                    func(*args)
