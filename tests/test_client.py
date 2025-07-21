"""
Tests for the Client class - authentication and API key handling
"""

from unittest.mock import Mock, patch

import pytest

from crypto_com_developer_platform_client.client import Client


class TestClient:
    """Test cases for Client class authentication and initialization."""

    def setup_method(self):
        """Reset Client state before each test."""
        Client._api_key = None
        Client._provider = None

    @pytest.mark.unit
    def test_init_with_api_key_only(self, mock_api_key):
        """Test Client initialization with only API key."""
        Client.init(api_key=mock_api_key)

        assert Client._api_key == mock_api_key
        assert Client._provider == ""

    @pytest.mark.unit
    def test_init_with_api_key_and_provider(self, mock_api_key, mock_provider):
        """Test Client initialization with API key and provider."""
        Client.init(api_key=mock_api_key, provider=mock_provider)

        assert Client._api_key == mock_api_key
        assert Client._provider == mock_provider

    @pytest.mark.unit
    def test_get_api_key_success(self, mock_api_key):
        """Test successful API key retrieval."""
        Client.init(api_key=mock_api_key)

        retrieved_key = Client.get_api_key()
        assert retrieved_key == mock_api_key

    @pytest.mark.unit
    def test_get_api_key_not_set(self):
        """Test API key retrieval when not set raises ValueError."""
        # Ensure API key is not set
        Client._api_key = None

        with pytest.raises(ValueError, match="API key is not set"):
            Client.get_api_key()

    @pytest.mark.unit
    def test_get_provider_success(self, mock_provider):
        """Test successful provider retrieval."""
        Client.init(api_key="test-key", provider=mock_provider)

        retrieved_provider = Client.get_provider()
        assert retrieved_provider == mock_provider

    @pytest.mark.unit
    def test_get_provider_not_set(self):
        """Test provider retrieval when not set raises ValueError."""
        Client._provider = None

        with pytest.raises(ValueError, match="Provider is not set"):
            Client.get_provider()

    @pytest.mark.unit
    def test_init_with_modules_loading(self, mock_api_key):
        """Test that Client.init properly loads and initializes without errors."""
        # This tests the actual loading and initialization process
        # instead of mocking individual modules which is complex due to
        # the imports being inside the init method

        try:
            Client.init(api_key=mock_api_key)
            # If we get here, initialization succeeded
            assert Client.get_api_key() == mock_api_key
        except ImportError as e:
            pytest.fail(f"Module initialization failed with ImportError: {e}")
        except Exception as e:
            pytest.fail(f"Module initialization failed with error: {e}")

    @pytest.mark.unit
    def test_api_key_persistence_across_calls(self, mock_api_key):
        """Test that API key persists across multiple method calls."""
        Client.init(api_key=mock_api_key)

        # Call get_api_key multiple times
        key1 = Client.get_api_key()
        key2 = Client.get_api_key()
        key3 = Client.get_api_key()

        assert key1 == key2 == key3 == mock_api_key

    @pytest.mark.unit
    def test_provider_persistence_across_calls(self, mock_provider):
        """Test that provider persists across multiple method calls."""
        Client.init(api_key="test-key", provider=mock_provider)

        # Call get_provider multiple times
        provider1 = Client.get_provider()
        provider2 = Client.get_provider()
        provider3 = Client.get_provider()

        assert provider1 == provider2 == provider3 == mock_provider

    @pytest.mark.unit
    def test_reinitialize_client(self, mock_api_key, mock_provider):
        """Test that Client can be reinitialized with new values."""
        # Initial initialization
        Client.init(api_key="old-key", provider="old-provider")

        # Reinitialize with new values
        Client.init(api_key=mock_api_key, provider=mock_provider)

        assert Client.get_api_key() == mock_api_key
        assert Client.get_provider() == mock_provider

    @pytest.mark.unit
    def test_empty_string_provider_handling(self, mock_api_key):
        """Test that empty string provider is handled correctly."""
        Client.init(api_key=mock_api_key, provider="")

        assert Client._api_key == mock_api_key
        assert Client._provider == ""

    @pytest.mark.unit
    def test_api_key_validation_type(self):
        """Test API key type validation (should accept strings)."""
        # Test with string API key
        Client.init(api_key="string-api-key")
        assert Client.get_api_key() == "string-api-key"

        # Test with non-string API key (should still work as Python is dynamically typed)
        Client.init(api_key=12345)
        assert Client.get_api_key() == 12345

    @pytest.mark.unit
    def test_class_level_attributes(self, mock_api_key, mock_provider):
        """Test that Client uses class-level attributes correctly."""
        # Verify attributes are class-level, not instance-level
        assert hasattr(Client, "_api_key")
        assert hasattr(Client, "_provider")

        # Initialize and verify class attributes are set
        Client.init(api_key=mock_api_key, provider=mock_provider)

        assert Client._api_key == mock_api_key
        assert Client._provider == mock_provider

    @pytest.mark.unit
    def test_get_api_key_missing_attribute(self):
        """Test get_api_key when _api_key attribute doesn't exist."""
        # Remove the attribute entirely
        if hasattr(Client, "_api_key"):
            delattr(Client, "_api_key")

        with pytest.raises(ValueError, match="API key is not set"):
            Client.get_api_key()

    @pytest.mark.unit
    def test_get_provider_missing_attribute(self):
        """Test get_provider when _provider attribute doesn't exist."""
        # Remove the attribute entirely
        if hasattr(Client, "_provider"):
            delattr(Client, "_provider")

        with pytest.raises(ValueError, match="Provider is not set"):
            Client.get_provider()

    @pytest.mark.unit
    def test_comprehensive_error_conditions(self):
        """Test various error conditions comprehensively."""
        # Test class methods with None values
        Client._api_key = None
        Client._provider = None

        with pytest.raises(ValueError, match="API key is not set"):
            Client.get_api_key()

        with pytest.raises(ValueError, match="Provider is not set"):
            Client.get_provider()
