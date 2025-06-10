from crypto_com_developer_platform_client import Client
from crypto_com_developer_platform_client import Network

# to test methods. will be removed in final PR
if __name__ == "__main__":
    API_KEY = "APIKEY"

    Client.init(api_key=API_KEY)

    # Get the current block
    test = Network.chain_id()
    print("Current Block:\n", test)
