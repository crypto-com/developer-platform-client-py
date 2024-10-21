# Crypto.com Python Client for Developer Platform

The Crypto.com Python Client for Developer Platform is a Python library designed to facilitate easy and efficient interactions with the Crypto.com [Developer Platform Service](https://github.com/crypto-com/developer-platform-service). This client library provides methods to interact with various blockchain networks, manage wallets, tokens, and contracts seamlessly.

![PyPI](https://img.shields.io/pypi/v/crypto-com-developer-platform-client)

## Features

- Simple and intuitive API for interacting with the Crypto.com Developer Platform Service.
- Configurable client instances tailored to your specific endpoint and security needs.
- **Currently in beta**: Expect frequent updates and potential changes in future releases.

## Installation

To install the package, run the following command:

```bash
pip install crypto-com-developer-platform-client
```

## Usage

Here’s how you can use the Crypto.com Python Client for Developer Platform in your project:

### Configuring the Client

```py
from crypto-com-developer-platform-client import Block, Client
from crypto-com-developer-platform-client.interfaces.chain_interfaces import CronosZkEvm


Client.init(api_key="EXPLORER_API_KEY",
            chain_id=CronosZkEvm.TESTNET,provider="YOUR_PROVIDER")

block = Block.get_by_tag("latest")
```

## API Methods

### Block

- `get_by_tag(tag, tx_detail)`
  - `tag`: Integer of a block number in hex, or the string "earliest", "latest" or "pending", as in https://ethereum.org/en/developers/docs/apis/json-rpc/#default-block
  - `tx_detail`: If true it returns the full transaction objects, if false only the hashes of the transactions.

### Contract

- `get_contract_abi(contract_address)`
  - `contract_address`: The address of the smart contract.

### Token

- `get_native_balance(address)`
  - `address`: The address to get the balance for.
- `get_erc20_balance(address, contract_address, block_height)`
  - `address`: The address to get the balance for.
  - `contract_address`: The contract address to get the balance for.
  - `block_height`: The block height to get the balance for. Optional, default to "latest".
- `transfer_token(to, amount)`
  - `to`: The address to transfer the token to.
  - `amount`: The amount of token to transfer.
- `wrap_token(from_contract_address, to_contract_address, to, amount)`
  - `from_contract_address`: The address to wrap the token from.
  - `to_contract_address`: The address to wrap the token to.
  - `to`: The address to send the wrapped token to
  - `amount`: The amount of token to wrap.
- `swap_token(from_contract_address, to_contract_address, to, amount)`
  - `from_contract_address`: The token to swap from.
  - `to_contract_address`: The token to swap to.
  - `to`: The address to send the swapped token to
  - `amount`: The amount of token to swap.

### Transaction

- `get_transactions_by_address(address, session, limit)`
  - `address`: The address to get the transactions for.
  - `session`: The session to get the transactions for. Optional, default to "".
  - `limit`: The limit of the transactions to get. Optional, default to "20".
- `get_transaction_by_hash(hash)`
  - `hash`: The hash of the transaction.
- `get_transaction_status(hash)`
  - `hash`: The hash of the transaction to get the status for.

### Wallet

- `create_wallet()`
- `get_balance(address)`
  - `address`: The address to get the balance for.

## Licensing

The code in this project is licensed under the MIT license.

## Contact

If you have any questions or comments about the library, please feel free to open an issue or a pull request on our GitHub repository.
