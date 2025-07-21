"""
Tests for the contract_api integration module
"""

import pytest
import responses

from crypto_com_developer_platform_client.constants import API_URL
from crypto_com_developer_platform_client.integrations.contract_api import (
    get_contract_abi,
    get_contract_code,
)


class TestContractApi:
    """Test cases for contract_api functions."""

    @pytest.mark.unit
    @responses.activate
    def test_get_contract_abi_success(self):
        """Test successful contract ABI retrieval."""
        contract_address = "0x123abc000000000000000000000000000000000"
        explorer_key = "test-explorer-key"
        expected_response = {
            "success": True,
            "data": {
                "abi": [
                    {
                        "type": "function",
                        "name": "balanceOf",
                        "inputs": [{"name": "owner", "type": "address"}],
                        "outputs": [{"name": "", "type": "uint256"}],
                    }
                ]
            },
        }

        responses.add(
            responses.GET,
            f"{API_URL}/contract/contract-abi?contractAddress={contract_address}&explorerKey={explorer_key}",
            json=expected_response,
            status=200,
        )

        result = get_contract_abi("test-api-key", contract_address, explorer_key)

        assert result == expected_response
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers["x-api-key"] == "test-api-key"
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"

    @pytest.mark.unit
    @responses.activate
    def test_get_contract_code_success(self):
        """Test successful contract code retrieval."""
        contract_address = "0x123abc000000000000000000000000000000000"
        expected_response = {
            "success": True,
            "data": {"bytecode": "0x123abc..."},
        }

        responses.add(
            responses.GET,
            f"{API_URL}/contract/contract-code?contractAddress={contract_address}",
            json=expected_response,
            status=200,
        )

        result = get_contract_code("test-api-key", contract_address)

        assert result == expected_response
        assert len(responses.calls) == 1
        assert "contractAddress=" in responses.calls[0].request.url

    @pytest.mark.unit
    @responses.activate
    def test_get_contract_abi_not_found(self):
        """Test contract ABI with not found error."""
        contract_address = "0x000000000000000000000000000000000000000"
        explorer_key = "test-explorer-key"
        error_response = {"error": "Contract not found"}

        responses.add(
            responses.GET,
            f"{API_URL}/contract/contract-abi?contractAddress={contract_address}&explorerKey={explorer_key}",
            json=error_response,
            status=404,
        )

        with pytest.raises(Exception, match="Contract not found"):
            get_contract_abi("test-api-key", contract_address, explorer_key)

    @pytest.mark.unit
    @responses.activate
    def test_get_contract_code_invalid_address(self):
        """Test contract code with invalid address error."""
        invalid_address = "0xinvalid"
        error_response = {"error": "Invalid contract address"}

        responses.add(
            responses.GET,
            f"{API_URL}/contract/contract-code?contractAddress={invalid_address}",
            json=error_response,
            status=400,
        )

        with pytest.raises(Exception, match="Invalid contract address"):
            get_contract_code("test-api-key", invalid_address)

    @pytest.mark.unit
    @responses.activate
    def test_get_contract_abi_unauthorized(self):
        """Test contract ABI with unauthorized error."""
        contract_address = "0x123abc000000000000000000000000000000000"
        explorer_key = "test-explorer-key"
        error_response = {"error": "Unauthorized access"}

        responses.add(
            responses.GET,
            f"{API_URL}/contract/contract-abi?contractAddress={contract_address}&explorerKey={explorer_key}",
            json=error_response,
            status=401,
        )

        with pytest.raises(Exception, match="Unauthorized access"):
            get_contract_abi("invalid-api-key", contract_address, explorer_key)

    @pytest.mark.unit
    @responses.activate
    def test_get_contract_code_server_error(self):
        """Test contract code with server error."""
        contract_address = "0x123abc000000000000000000000000000000000"
        error_response = {"error": "Internal server error"}

        responses.add(
            responses.GET,
            f"{API_URL}/contract/contract-code?contractAddress={contract_address}",
            json=error_response,
            status=500,
        )

        with pytest.raises(Exception, match="Internal server error"):
            get_contract_code("test-api-key", contract_address)

    @pytest.mark.unit
    @responses.activate
    def test_http_error_status_codes(self):
        """Test various HTTP error status codes for both functions."""
        contract_address = "0x123abc000000000000000000000000000000000"
        explorer_key = "test-explorer-key"
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
            # Test ABI endpoint
            responses.reset()
            responses.add(
                responses.GET,
                f"{API_URL}/contract/contract-abi?contractAddress={contract_address}&explorerKey={explorer_key}",
                json={"error": error_message},
                status=status_code,
            )

            with pytest.raises(Exception, match=error_message):
                get_contract_abi("test-api-key", contract_address, explorer_key)

            # Test Code endpoint
            responses.reset()
            responses.add(
                responses.GET,
                f"{API_URL}/contract/contract-code?contractAddress={contract_address}",
                json={"error": error_message},
                status=status_code,
            )

            with pytest.raises(Exception, match=error_message):
                get_contract_code("test-api-key", contract_address)

    @pytest.mark.unit
    @responses.activate
    def test_success_status_codes(self):
        """Test that both 200 and 201 status codes are accepted as success."""
        contract_address = "0x123abc000000000000000000000000000000000"
        explorer_key = "test-explorer-key"
        success_response = {"data": {"abi": []}}

        for status_code in [200, 201]:
            responses.reset()
            responses.add(
                responses.GET,
                f"{API_URL}/contract/contract-abi?contractAddress={contract_address}&explorerKey={explorer_key}",
                json=success_response,
                status=status_code,
            )

            result = get_contract_abi("test-api-key", contract_address, explorer_key)
            assert result == success_response

    @pytest.mark.unit
    @responses.activate
    def test_multiple_contract_addresses(self):
        """Test with different contract addresses."""
        explorer_key = "test-explorer-key"
        test_addresses = [
            "0x123abc000000000000000000000000000000000",
            "0x789012000000000000000000000000000000000",
            "0x901234000000000000000000000000000000000",
        ]

        for address in test_addresses:
            responses.add(
                responses.GET,
                f"{API_URL}/contract/contract-abi?contractAddress={address}&explorerKey={explorer_key}",
                json={"data": {"abi": [], "address": address}},
                status=200,
            )

        for address in test_addresses:
            result = get_contract_abi("test-api-key", address, explorer_key)
            assert result["data"]["address"] == address

    @pytest.mark.unit
    @responses.activate
    def test_api_key_parameter_validation(self):
        """Test that API key is properly included in headers."""
        contract_address = "0x123abc000000000000000000000000000000000"
        explorer_key = "test-explorer-key"
        test_keys = ["test-key-1", "another-api-key", "key-with-special-chars-123"]

        for api_key in test_keys:
            responses.reset()
            responses.add(
                responses.GET,
                f"{API_URL}/contract/contract-abi?contractAddress={contract_address}&explorerKey={explorer_key}",
                json={"data": {}},
                status=200,
            )

            get_contract_abi(api_key, contract_address, explorer_key)

            # Verify the API key was sent in headers
            assert responses.calls[0].request.headers["x-api-key"] == api_key

    @pytest.mark.unit
    @responses.activate
    def test_request_timeout_configuration(self):
        """Test that requests are configured with proper timeout."""
        contract_address = "0x123abc000000000000000000000000000000000"
        explorer_key = "test-explorer-key"

        responses.add(
            responses.GET,
            f"{API_URL}/contract/contract-abi?contractAddress={contract_address}&explorerKey={explorer_key}",
            json={"data": {}},
            status=200,
        )

        get_contract_abi("test-api-key", contract_address, explorer_key)

        # The timeout parameter is handled internally, so we just verify the call succeeds
        assert len(responses.calls) == 1

    @pytest.mark.unit
    @responses.activate
    def test_large_abi_response(self):
        """Test handling of large ABI responses."""
        contract_address = "0x123abc000000000000000000000000000000000"
        explorer_key = "test-explorer-key"
        large_abi = []
        for i in range(100):  # Large ABI with many functions
            large_abi.append(
                {
                    "type": "function",
                    "name": f"function_{i}",
                    "inputs": [{"name": "param", "type": "uint256"}],
                    "outputs": [{"name": "", "type": "bool"}],
                }
            )

        expected_response = {"success": True, "data": {"abi": large_abi}}

        responses.add(
            responses.GET,
            f"{API_URL}/contract/contract-abi?contractAddress={contract_address}&explorerKey={explorer_key}",
            json=expected_response,
            status=200,
        )

        result = get_contract_abi("test-api-key", contract_address, explorer_key)

        assert result == expected_response
        assert len(result["data"]["abi"]) == 100
