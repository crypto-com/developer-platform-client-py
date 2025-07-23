"""
Tests for the token_api integration module
"""

import pytest
import responses

from crypto_com_developer_platform_client.constants import API_URL
from crypto_com_developer_platform_client.integrations.token_api import (
    get_erc20_metadata,
    get_erc20_token_balance,
    get_erc721_metadata,
    get_erc721_token_balance,
    get_native_token_balance,
    get_token_owner,
    get_token_uri,
    swap_token,
    transfer_token,
    wrap_token,
)


class TestTokenApi:
    """Test cases for token_api functions."""

    @pytest.mark.unit
    @responses.activate
    def test_get_native_token_balance_success(self):
        """Test successful native token balance retrieval."""
        wallet_address = "0x123abc000000000000000000000000000000000"
        expected_response = {
            "success": True,
            "data": {
                "balance": "1500000000000000000",
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

        result = get_native_token_balance("test-api-key", wallet_address)

        assert result == expected_response
        assert len(responses.calls) == 1
        assert f"walletAddress={wallet_address}" in responses.calls[0].request.url

    @pytest.mark.unit
    @responses.activate
    def test_get_erc20_token_balance_success(self):
        """Test successful ERC20 token balance retrieval."""
        wallet_address = "0x123abc000000000000000000000000000000000"
        contract_address = "0x789012000000000000000000000000000000000"
        block_height = "latest"
        expected_response = {
            "success": True,
            "data": {
                "balance": "1000000000",
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

        result = get_erc20_token_balance(
            "test-api-key", wallet_address, contract_address, block_height
        )

        assert result == expected_response
        assert f"walletAddress={wallet_address}" in responses.calls[0].request.url
        assert f"contractAddress={contract_address}" in responses.calls[0].request.url
        assert f"blockHeight={block_height}" in responses.calls[0].request.url

    @pytest.mark.unit
    @responses.activate
    def test_get_erc721_token_balance_success(self):
        """Test successful ERC721 token balance retrieval."""
        wallet_address = "0x123abc000000000000000000000000000000000"
        contract_address = "0x789012000000000000000000000000000000000"
        expected_response = {
            "success": True,
            "data": {"balance": 5, "tokens": ["1", "2", "3", "4", "5"]},
        }

        responses.add(
            responses.GET,
            f"{API_URL}/token/erc721-token-balance",
            json=expected_response,
            status=200,
        )

        result = get_erc721_token_balance(
            "test-api-key", wallet_address, contract_address
        )

        assert result == expected_response
        assert f"walletAddress={wallet_address}" in responses.calls[0].request.url
        assert f"contractAddress={contract_address}" in responses.calls[0].request.url

    @pytest.mark.unit
    @responses.activate
    def test_get_erc20_metadata_success(self):
        """Test successful ERC20 metadata retrieval."""
        contract_address = "0x789012000000000000000000000000000000000"
        expected_response = {
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
            json=expected_response,
            status=200,
        )

        result = get_erc20_metadata("test-api-key", contract_address)

        assert result == expected_response
        assert f"contractAddress={contract_address}" in responses.calls[0].request.url

    @pytest.mark.unit
    @responses.activate
    def test_transfer_token_success(self):
        """Test successful token transfer."""
        payload = {
            "to": "0x789012000000000000000000000000000000000",
            "amount": "1000000000000000000",
        }
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

        result = transfer_token("test-api-key", payload)

        assert result == expected_response
        assert len(responses.calls) == 1

    @pytest.mark.unit
    @responses.activate
    def test_wrap_token_success(self):
        """Test successful token wrapping."""
        payload = {"amount": "500000000000000000"}
        expected_response = {
            "success": True,
            "data": {"transactionHash": "0xwrap1234...", "status": "pending"},
        }

        responses.add(
            responses.POST, f"{API_URL}/token/wrap", json=expected_response, status=200
        )

        result = wrap_token("test-api-key", payload)

        assert result == expected_response
        assert len(responses.calls) == 1

    @pytest.mark.unit
    @responses.activate
    def test_swap_token_success(self):
        """Test successful token swap."""
        payload = {
            "fromToken": "0x789012000000000000000000000000000000000",
            "toToken": "0x901234000000000000000000000000000000000",
            "amount": "1000000",
        }
        expected_response = {
            "success": True,
            "data": {
                "transactionHash": "0xswap1234...",
                "status": "pending",
                "estimatedOutput": "950000",
            },
        }

        responses.add(
            responses.POST, f"{API_URL}/token/swap", json=expected_response, status=200
        )

        result = swap_token("test-api-key", payload)

        assert result == expected_response
        assert len(responses.calls) == 1

    @pytest.mark.unit
    @responses.activate
    def test_get_native_token_balance_api_error(self):
        """Test native token balance with API error."""
        wallet_address = "0x123abc000000000000000000000000000000000"
        error_response = {"error": "Invalid wallet address"}

        responses.add(
            responses.GET,
            f"{API_URL}/token/native-token-balance",
            json=error_response,
            status=400,
        )

        with pytest.raises(Exception, match="Invalid wallet address"):
            get_native_token_balance("test-api-key", wallet_address)

    @pytest.mark.unit
    @responses.activate
    def test_transfer_token_insufficient_balance(self):
        """Test token transfer with insufficient balance."""
        payload = {
            "to": "0x789012000000000000000000000000000000000",
            "amount": "1000000000000000000000",
        }
        error_response = {"error": "Insufficient balance"}

        responses.add(
            responses.POST, f"{API_URL}/token/transfer", json=error_response, status=422
        )

        with pytest.raises(Exception, match="Insufficient balance"):
            transfer_token("test-api-key", payload)

    @pytest.mark.unit
    @responses.activate
    def test_http_error_status_codes(self):
        """Test various HTTP error status codes."""
        wallet_address = "0x123abc000000000000000000000000000000000"
        error_cases = [
            (400, "Bad request"),
            (401, "Unauthorized"),
            (404, "Not found"),
            (429, "Rate limited"),
            (500, "Internal server error"),
        ]

        for status_code, error_message in error_cases:
            responses.reset()
            responses.add(
                responses.GET,
                f"{API_URL}/token/native-token-balance",
                json={"error": error_message},
                status=status_code,
            )

            with pytest.raises(Exception, match=error_message):
                get_native_token_balance("test-api-key", wallet_address)

    @pytest.mark.unit
    @responses.activate
    def test_success_status_codes(self):
        """Test that both 200 and 201 status codes are accepted as success."""
        wallet_address = "0x123abc000000000000000000000000000000000"
        success_response = {"data": {"balance": "1000000000000000000"}}

        for status_code in [200, 201]:
            responses.reset()
            responses.add(
                responses.GET,
                f"{API_URL}/token/native-token-balance",
                json=success_response,
                status=status_code,
            )

            result = get_native_token_balance("test-api-key", wallet_address)
            assert result == success_response

    @pytest.mark.unit
    @responses.activate
    def test_api_key_header_validation(self):
        """Test that API key is properly included in headers."""
        wallet_address = "0x123abc000000000000000000000000000000000"
        test_keys = ["test-key-1", "another-api-key", "key-with-special-chars-123"]

        for api_key in test_keys:
            responses.reset()
            responses.add(
                responses.GET,
                f"{API_URL}/token/native-token-balance",
                json={"data": {}},
                status=200,
            )

            get_native_token_balance(api_key, wallet_address)

            assert responses.calls[0].request.headers["x-api-key"] == api_key

    @pytest.mark.unit
    @responses.activate
    def test_get_token_owner_success(self):
        """Test successful token owner retrieval."""
        contract_address = "0x456def000000000000000000000000000000000"
        token_id = "12345"
        expected_response = {
            "success": True,
            "data": {
                "owner": "0x123abc000000000000000000000000000000000",
                "contractAddress": contract_address,
                "tokenId": token_id,
            },
        }

        responses.add(
            responses.GET,
            f"{API_URL}/token/erc721-token-owner?contractAddress={contract_address}&tokenId={token_id}",
            json=expected_response,
            status=200,
        )

        result = get_token_owner("test-api-key", contract_address, token_id)

        assert result == expected_response
        assert len(responses.calls) == 1
        assert f"contractAddress={contract_address}" in responses.calls[0].request.url
        assert f"tokenId={token_id}" in responses.calls[0].request.url

    @pytest.mark.unit
    @responses.activate
    def test_get_token_uri_success(self):
        """Test successful token URI retrieval."""
        contract_address = "0x456def000000000000000000000000000000000"
        token_id = "12345"
        expected_response = {
            "success": True,
            "data": {
                "tokenURI": "https://example.com/token/12345.json",
                "contractAddress": contract_address,
                "tokenId": token_id,
            },
        }

        responses.add(
            responses.GET,
            f"{API_URL}/token/erc721-token-uri?contractAddress={contract_address}&tokenId={token_id}",
            json=expected_response,
            status=200,
        )

        result = get_token_uri("test-api-key", contract_address, token_id)

        assert result == expected_response
        assert len(responses.calls) == 1
        assert f"contractAddress={contract_address}" in responses.calls[0].request.url
        assert f"tokenId={token_id}" in responses.calls[0].request.url

    @pytest.mark.unit
    @responses.activate
    def test_get_erc721_metadata_success(self):
        """Test successful ERC721 metadata retrieval."""
        contract_address = "0x456def000000000000000000000000000000000"
        expected_response = {
            "success": True,
            "data": {
                "name": "CryptoKitties",
                "symbol": "CK",
                "totalSupply": "2000000",
                "contractAddress": contract_address,
            },
        }

        responses.add(
            responses.GET,
            f"{API_URL}/token/erc721-token-metadata?contractAddress={contract_address}",
            json=expected_response,
            status=200,
        )

        result = get_erc721_metadata("test-api-key", contract_address)

        assert result == expected_response
        assert len(responses.calls) == 1
        assert f"contractAddress={contract_address}" in responses.calls[0].request.url

    @pytest.mark.unit
    @responses.activate
    def test_get_token_owner_not_found(self):
        """Test token owner with not found error."""
        contract_address = "0x000000000000000000000000000000000000000"
        token_id = "999999"
        error_response = {"error": "Token not found"}

        responses.add(
            responses.GET,
            f"{API_URL}/token/erc721-token-owner?contractAddress={contract_address}&tokenId={token_id}",
            json=error_response,
            status=404,
        )

        with pytest.raises(Exception, match="Token not found"):
            get_token_owner("test-api-key", contract_address, token_id)

    @pytest.mark.unit
    @responses.activate
    def test_get_token_uri_invalid_token(self):
        """Test token URI with invalid token error."""
        contract_address = "0x456def000000000000000000000000000000000"
        token_id = "invalid"
        error_response = {"error": "Invalid token ID"}

        responses.add(
            responses.GET,
            f"{API_URL}/token/erc721-token-uri?contractAddress={contract_address}&tokenId={token_id}",
            json=error_response,
            status=400,
        )

        with pytest.raises(Exception, match="Invalid token ID"):
            get_token_uri("test-api-key", contract_address, token_id)

    @pytest.mark.unit
    @responses.activate
    def test_get_erc721_metadata_unauthorized(self):
        """Test ERC721 metadata with unauthorized error."""
        contract_address = "0x456def000000000000000000000000000000000"
        error_response = {"error": "Unauthorized access"}

        responses.add(
            responses.GET,
            f"{API_URL}/token/erc721-token-metadata?contractAddress={contract_address}",
            json=error_response,
            status=401,
        )

        with pytest.raises(Exception, match="Unauthorized access"):
            get_erc721_metadata("invalid-api-key", contract_address)

    @pytest.mark.unit
    @responses.activate
    def test_missing_functions_http_error_status_codes(self):
        """Test various HTTP error status codes for missing functions."""
        contract_address = "0x456def000000000000000000000000000000000"
        token_id = "12345"
        error_cases = [
            (400, "Bad request"),
            (401, "Unauthorized"),
            (403, "Forbidden"),
            (404, "Not found"),
            (500, "Internal server error"),
            (503, "Service unavailable"),
        ]

        for status_code, error_message in error_cases:
            # Test get_token_owner endpoint
            responses.reset()
            responses.add(
                responses.GET,
                f"{API_URL}/token/erc721-token-owner?contractAddress={contract_address}&tokenId={token_id}",
                json={"error": error_message},
                status=status_code,
            )

            with pytest.raises(Exception, match=error_message):
                get_token_owner("test-api-key", contract_address, token_id)

            # Test get_token_uri endpoint
            responses.reset()
            responses.add(
                responses.GET,
                f"{API_URL}/token/erc721-token-uri?contractAddress={contract_address}&tokenId={token_id}",
                json={"error": error_message},
                status=status_code,
            )

            with pytest.raises(Exception, match=error_message):
                get_token_uri("test-api-key", contract_address, token_id)

            # Test get_erc721_metadata endpoint
            responses.reset()
            responses.add(
                responses.GET,
                f"{API_URL}/token/erc721-token-metadata?contractAddress={contract_address}",
                json={"error": error_message},
                status=status_code,
            )

            with pytest.raises(Exception, match=error_message):
                get_erc721_metadata("test-api-key", contract_address)

    @pytest.mark.unit
    @responses.activate
    def test_non_json_error_responses(self):
        """Test error responses that are not JSON."""
        wallet_address = "0x123abc000000000000000000000000000000000"
        contract_address = "0x789012000000000000000000000000000000000"

        # Test for all functions that can have non-JSON errors
        test_cases = [
            (
                "native_balance",
                f"{API_URL}/token/native-token-balance",
                lambda: get_native_token_balance("test-api-key", wallet_address),
                responses.GET,
            ),
            (
                "erc20_balance",
                f"{API_URL}/token/erc20-token-balance",
                lambda: get_erc20_token_balance(
                    "test-api-key", wallet_address, contract_address, "latest"
                ),
                responses.GET,
            ),
            (
                "erc721_balance",
                f"{API_URL}/token/erc721-token-balance",
                lambda: get_erc721_token_balance(
                    "test-api-key", wallet_address, contract_address
                ),
                responses.GET,
            ),
            (
                "erc20_metadata",
                f"{API_URL}/token/erc20-token-metadata",
                lambda: get_erc20_metadata("test-api-key", contract_address),
                responses.GET,
            ),
            (
                "erc721_metadata",
                f"{API_URL}/token/erc721-token-metadata",
                lambda: get_erc721_metadata("test-api-key", contract_address),
                responses.GET,
            ),
            (
                "token_owner",
                f"{API_URL}/token/erc721-token-owner",
                lambda: get_token_owner("test-api-key", contract_address, "123"),
                responses.GET,
            ),
            (
                "token_uri",
                f"{API_URL}/token/erc721-token-uri",
                lambda: get_token_uri("test-api-key", contract_address, "123"),
                responses.GET,
            ),
            (
                "transfer",
                f"{API_URL}/token/transfer",
                lambda: transfer_token(
                    "test-api-key", {"to": "0x123", "amount": "100"}
                ),
                responses.POST,
            ),
            (
                "wrap",
                f"{API_URL}/token/wrap",
                lambda: wrap_token("test-api-key", {"amount": "100"}),
                responses.POST,
            ),
            (
                "swap",
                f"{API_URL}/token/swap",
                lambda: swap_token(
                    "test-api-key",
                    {"fromToken": "0x123", "toToken": "0x456", "amount": "100"},
                ),
                responses.POST,
            ),
        ]

        for test_name, url, test_func, method in test_cases:
            responses.reset()
            # Add a non-JSON response
            responses.add(
                method,
                url,
                body="Internal Server Error",
                status=500,
                content_type="text/plain",
            )

            with pytest.raises(Exception, match="HTTP error! status: 500"):
                test_func()

    @pytest.mark.unit
    @responses.activate
    def test_comprehensive_post_method_error_handling(self):
        """Test comprehensive error handling for POST methods (transfer, wrap, swap)."""
        payload = {"test": "data"}
        error_cases = [
            (400, "Bad request"),
            (401, "Unauthorized"),
            (403, "Forbidden"),
            (404, "Endpoint not found"),
            (422, "Validation error"),
            (429, "Rate limited"),
            (500, "Internal server error"),
            (502, "Bad gateway"),
            (503, "Service unavailable"),
        ]

        post_functions = [
            ("transfer", transfer_token, f"{API_URL}/token/transfer"),
            ("wrap", wrap_token, f"{API_URL}/token/wrap"),
            ("swap", swap_token, f"{API_URL}/token/swap"),
        ]

        for func_name, func, url in post_functions:
            for status_code, error_message in error_cases:
                responses.reset()
                responses.add(
                    responses.POST,
                    url,
                    json={"error": error_message},
                    status=status_code,
                )

                with pytest.raises(Exception, match=error_message):
                    func("test-api-key", payload)

    @pytest.mark.unit
    @responses.activate
    def test_comprehensive_get_method_error_handling(self):
        """Test comprehensive error handling for GET methods."""
        wallet_address = "0x123abc000000000000000000000000000000000"
        contract_address = "0x789012000000000000000000000000000000000"
        token_id = "12345"

        error_cases = [
            (400, "Bad request"),
            (401, "Unauthorized"),
            (403, "Forbidden"),
            (404, "Not found"),
            (429, "Rate limited"),
            (500, "Internal server error"),
            (502, "Bad gateway"),
            (503, "Service unavailable"),
        ]

        get_functions = [
            (
                "native_balance",
                lambda: get_native_token_balance("test-api-key", wallet_address),
            ),
            (
                "erc20_balance",
                lambda: get_erc20_token_balance(
                    "test-api-key", wallet_address, contract_address, "latest"
                ),
            ),
            (
                "erc721_balance",
                lambda: get_erc721_token_balance(
                    "test-api-key", wallet_address, contract_address
                ),
            ),
            (
                "erc20_metadata",
                lambda: get_erc20_metadata("test-api-key", contract_address),
            ),
            (
                "erc721_metadata",
                lambda: get_erc721_metadata("test-api-key", contract_address),
            ),
            (
                "token_owner",
                lambda: get_token_owner("test-api-key", contract_address, token_id),
            ),
            (
                "token_uri",
                lambda: get_token_uri("test-api-key", contract_address, token_id),
            ),
        ]

        for func_name, func in get_functions:
            for status_code, error_message in error_cases:
                responses.reset()
                # Mock the appropriate URL pattern to catch the request
                responses.add(
                    responses.GET,
                    f"{API_URL}/token",
                    json={"error": error_message},
                    status=status_code,
                )
                responses.add(
                    responses.GET,
                    f"{API_URL}/token/native-token-balance",
                    json={"error": error_message},
                    status=status_code,
                )
                responses.add(
                    responses.GET,
                    f"{API_URL}/token/erc20-token-balance",
                    json={"error": error_message},
                    status=status_code,
                )
                responses.add(
                    responses.GET,
                    f"{API_URL}/token/erc721-token-balance",
                    json={"error": error_message},
                    status=status_code,
                )
                responses.add(
                    responses.GET,
                    f"{API_URL}/token/erc20-token-metadata",
                    json={"error": error_message},
                    status=status_code,
                )
                responses.add(
                    responses.GET,
                    f"{API_URL}/token/erc721-token-metadata",
                    json={"error": error_message},
                    status=status_code,
                )
                responses.add(
                    responses.GET,
                    f"{API_URL}/token/erc721-token-owner",
                    json={"error": error_message},
                    status=status_code,
                )
                responses.add(
                    responses.GET,
                    f"{API_URL}/token/erc721-token-uri",
                    json={"error": error_message},
                    status=status_code,
                )

                with pytest.raises(Exception, match=error_message):
                    func()

    @pytest.mark.unit
    @responses.activate
    def test_cronos_id_support(self):
        """Test that CronosId addresses with .cro suffix are supported."""
        cronos_id = "test.cro"
        expected_response = {
            "success": True,
            "data": {
                "balance": "2000000000000000000",
                "balanceInEth": "2.0",
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

        result = get_native_token_balance("test-api-key", cronos_id)

        assert result == expected_response
        assert f"walletAddress={cronos_id}" in responses.calls[0].request.url

    @pytest.mark.unit
    @responses.activate
    def test_content_type_headers(self):
        """Test that Content-Type headers are properly set for all requests."""
        wallet_address = "0x123abc000000000000000000000000000000000"
        contract_address = "0x789012000000000000000000000000000000000"
        token_id = "12345"
        payload = {"test": "data"}

        # Test GET requests
        responses.add(
            responses.GET,
            f"{API_URL}/token/native-token-balance",
            json={"data": {}},
            status=200,
        )
        get_native_token_balance("test-api-key", wallet_address)
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"

        responses.reset()
        responses.add(
            responses.GET,
            f"{API_URL}/token/erc20-token-balance",
            json={"data": {}},
            status=200,
        )
        get_erc20_token_balance(
            "test-api-key", wallet_address, contract_address, "latest"
        )
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"

        responses.reset()
        responses.add(
            responses.GET,
            f"{API_URL}/token/erc721-token-balance",
            json={"data": {}},
            status=200,
        )
        get_erc721_token_balance("test-api-key", wallet_address, contract_address)
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"

        responses.reset()
        responses.add(
            responses.GET,
            f"{API_URL}/token/erc20-token-metadata",
            json={"data": {}},
            status=200,
        )
        get_erc20_metadata("test-api-key", contract_address)
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"

        responses.reset()
        responses.add(
            responses.GET,
            f"{API_URL}/token/erc721-token-metadata",
            json={"data": {}},
            status=200,
        )
        get_erc721_metadata("test-api-key", contract_address)
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"

        responses.reset()
        responses.add(
            responses.GET,
            f"{API_URL}/token/erc721-token-owner",
            json={"data": {}},
            status=200,
        )
        get_token_owner("test-api-key", contract_address, token_id)
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"

        responses.reset()
        responses.add(
            responses.GET,
            f"{API_URL}/token/erc721-token-uri",
            json={"data": {}},
            status=200,
        )
        get_token_uri("test-api-key", contract_address, token_id)
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"

        # Test POST requests
        responses.reset()
        responses.add(
            responses.POST, f"{API_URL}/token/transfer", json={"data": {}}, status=200
        )
        transfer_token("test-api-key", payload)
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"

        responses.reset()
        responses.add(
            responses.POST, f"{API_URL}/token/wrap", json={"data": {}}, status=200
        )
        wrap_token("test-api-key", payload)
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"

        responses.reset()
        responses.add(
            responses.POST, f"{API_URL}/token/swap", json={"data": {}}, status=200
        )
        swap_token("test-api-key", payload)
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"
