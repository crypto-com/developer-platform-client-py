"""
Pytest configuration and fixtures for crypto_com_developer_platform_client tests
"""

import json
from unittest.mock import Mock, patch

import pytest
import responses

from crypto_com_developer_platform_client import Client
from crypto_com_developer_platform_client.constants import API_URL


@pytest.fixture
def mock_api_key():
    """Fixture providing a test API key."""
    return "test-api-key-12345"


@pytest.fixture
def mock_provider():
    """Fixture providing a test provider URL."""
    return "https://test-provider.example.com"


@pytest.fixture
def mock_client(mock_api_key, mock_provider):
    """Fixture providing a mocked Client instance."""
    # Reset client state before each test
    Client._api_key = None
    Client._provider = None
    Client.init(api_key=mock_api_key, provider=mock_provider)
    # Return an instance, not the class
    return Client()


@pytest.fixture
def mock_wallet_address():
    """Fixture providing a test wallet address."""
    return "0x123abc000000000000000000000000000000000"


@pytest.fixture
def mock_contract_address():
    """Fixture providing a test contract address."""
    return "0x456def000000000000000000000000000000000"


@pytest.fixture
def mock_transaction_hash():
    """Fixture providing a test transaction hash."""
    return "0x123abc0000000000000000000000000000000000000000000000000000"


@pytest.fixture
def mock_block_number():
    """Fixture providing a test block number."""
    return 12345678


@pytest.fixture
def responses_mock():
    """Fixture providing the responses mock for HTTP requests."""
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def mock_api_response():
    """Fixture providing a sample API response."""
    return {"success": True, "data": {"result": "test-result"}}


@pytest.fixture
def mock_error_response():
    """Fixture providing a sample error response."""
    return {"error": "Test error message", "code": "TEST_ERROR"}


@pytest.fixture
def mock_network_info():
    """Fixture providing mock network info response."""
    return {
        "success": True,
        "data": {
            "chainId": "0x152",
            "networkName": "Cronos Testnet",
            "blockTime": 6,
            "nativeCurrency": {"name": "Cronos", "symbol": "CRO", "decimals": 18},
        },
    }


@pytest.fixture
def mock_wallet_balance():
    """Fixture providing mock wallet balance response."""
    return {
        "success": True,
        "data": {
            "balance": "1000000000000000000",  # 1 CRO in wei
            "balanceInEth": "1.0",
            "address": "0x123abc000000000000000000000000000000000",
        },
    }


@pytest.fixture
def mock_token_balance():
    """Fixture providing mock token balance response."""
    return {
        "success": True,
        "data": {
            "balance": "500000000000000000000",  # 500 tokens
            "decimals": 18,
            "symbol": "USDC",
            "name": "USD Coin",
        },
    }


@pytest.fixture
def mock_contract_abi():
    """Fixture providing mock contract ABI response."""
    return {
        "success": True,
        "data": {
            "abi": [
                {
                    "inputs": [],
                    "name": "totalSupply",
                    "outputs": [{"type": "uint256", "name": ""}],
                    "type": "function",
                }
            ]
        },
    }


@pytest.fixture
def mock_block_data():
    """Fixture providing mock block data response."""
    return {
        "success": True,
        "data": {
            "number": "0xBC614E",
            "hash": "0x123abc0000000000000000000000000000000000000000000000000000",
            "timestamp": "0x123abc",
            "transactions": [],
            "gasUsed": "0x5208",
            "gasLimit": "0x1C9C380",
        },
    }


class MockRequestsResponse:
    """Mock response class for testing HTTP requests."""

    def __init__(self, status_code=200, json_data=None, text="", headers=None):
        self.status_code = status_code
        self._json_data = json_data or {}
        self.text = text
        self.headers = headers or {}

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code} Error")


@pytest.fixture
def mock_requests_get(monkeypatch):
    """Fixture to mock requests.get calls."""

    def _mock_get(url, **kwargs):
        return MockRequestsResponse(200, {"success": True, "data": "mocked"})

    monkeypatch.setattr("requests.get", _mock_get)
    return _mock_get


@pytest.fixture
def mock_requests_post(monkeypatch):
    """Fixture to mock requests.post calls."""

    def _mock_post(url, **kwargs):
        return MockRequestsResponse(200, {"success": True, "data": "mocked"})

    monkeypatch.setattr("requests.post", _mock_post)
    return _mock_post


def create_mock_response(status_code=200, json_data=None, text=""):
    """Helper function to create mock HTTP responses."""
    return MockRequestsResponse(status_code=status_code, json_data=json_data, text=text)


def assert_api_call_made(responses_mock, method, endpoint, expected_headers=None):
    """Helper function to assert that an API call was made with correct parameters."""
    assert len(responses_mock.calls) == 1
    call = responses_mock.calls[0]
    assert call.request.method == method
    assert endpoint in call.request.url

    if expected_headers:
        for header, value in expected_headers.items():
            assert call.request.headers.get(header) == value


def mock_api_endpoint(responses_mock, method, endpoint, response_data, status_code=200):
    """Helper function to mock API endpoints."""
    url = f"{API_URL}{endpoint}"
    responses_mock.add(
        method=getattr(responses, method.upper()),
        url=url,
        json=response_data,
        status=status_code,
    )
