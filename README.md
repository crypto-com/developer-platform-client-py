# Crypto.com Developer Platform Client.py

The **Crypto.com Developer Platform Client.py** is a Python SDK for integrating with the Crypto.com Developer Platform Service API. It simplifies access to blockchain features across the Cronos ecosystem (Cronos EVM & Cronos ZK EVM), covering native & ERC20 tokens, smart contracts, DeFi, wallets, transactions, and more.

![PyPI](https://img.shields.io/pypi/v/crypto-com-developer-platform-client)

## Features

- Blockchain interaction for Cronos EVM & ZK EVM chains
- Native and ERC20/ERC721 token operations
- Smart contract ABI & bytecode querying
- Cronos ID forward/reverse resolution
- Transactions, blocks, and fee utilities
- DeFi protocols: farms, tokens
- Exchange ticker data

## Installation

```bash
pip install crypto-com-developer-platform-client
```

### Initialize the Client

First, initialize the client with your API key. To get an API Key, please create an account and a project at https://developer.crypto.com.

```py
from crypto_com_developer_platform_client import Client
from crypto_com_developer_platform_client.interfaces.chain_interfaces import CronosZkEvm

Client.init(
    api_key="YOUR_EXPLORER_API_KEY",
    provider="https://your-provider.com"  # Optional
)
```

## Wallet

```py
from crypto_com_developer_platform_client import Wallet

wallet = Wallet.create()
print(wallet)
```

```py
balance = Wallet.get_balance("0xYourWalletAddress")
print(balance)
```

## Token

```py
from crypto_com_developer_platform_client import Token

native_balance = Token.get_native_balance("0xYourWalletAddress")
print(native_balance)
```

```py
erc20_balance = Token.get_erc20_balance("0xYourWallet", "0xTokenContract")
print(erc20_balance)
```

```py
result = Token.transfer_token("0xRecipient", 10)
print(result)
```

```py
wrap = Token.wrap_token("0xFromContract", "0xToContract", "0xReceiver", 5)
print(wrap)
```

```py
swap = Token.swap_token("0xFrom", "0xTo", "0xReceiver", 3)
print(swap)
```

## Transaction

```py
from crypto_com_developer_platform_client import Transaction

transactions = Transaction.get_transactions_by_address("0xAddress", session="", limit="10")
print(transactions)
```

```py
tx = Transaction.get_transaction_by_hash("0xTxHash")
print(tx)
```

```py
status = Transaction.get_transaction_status("0xTxHash")
print(status)
```

```py
count = Transaction.get_transaction_count("0xWallet")
print(count)
```

```py
gas_price = Transaction.get_gas_price()
print(gas_price)
```

```py
fee = Transaction.get_fee_data()
print(fee)
```

```py
estimate = Transaction.estimate_gas({
    "from": "0xFromAddress",
    "to": "0xToAddress",
    "value": "0xAmountInHex"
})
print(estimate)
```

## Contract

```py
from crypto_com_developer_platform_client import Contract

abi = Contract.get_contract_abi("0xContractAddress", "ExplorerAPIKey")
print(abi)
```

```py
bytecode = Contract.get_contract_code("0xContractAddress")
print(bytecode)
```

## Block

```py
from crypto_com_developer_platform_client import Block

current = Block.get_current_block()
print(current)
```

```py
block = Block.get_by_tag("latest", tx_detail="true")
print(block)
```

## Cronos ID

```py
from crypto_com_developer_platform_client import CronosId

resolved = CronosId.forward_resolve("alice.cro")
print(resolved)
```

```py
reverse = CronosId.reverse_resolve("0xAddress")
print(reverse)
```

## DeFi

```py
from crypto_com_developer_platform_client import Defi
from crypto_com_developer_platform_client.interfaces.defi_interfaces import DefiProtocol

tokens = Defi.get_whitelisted_tokens(DefiProtocol.H2)
print(tokens)
```

```py
farms = Defi.get_all_farms(DefiProtocol.VVS)
print(farms)
```

```py
farm = Defi.get_farm_by_symbol(DefiProtocol.H2, "zkCRO-MOON")
print(farm)
```

## Exchange

```py
from crypto_com_developer_platform_client import Exchange

tickers = Exchange.get_all_tickers()
print(tickers)
```

```py
ticker = Exchange.get_ticker_by_instrument("BTC_USDT")
print(ticker)
```

## API

### Client

- `Client.init(api_key, chain_id, provider=None)`: Initialize the SDK with API key, chain, and optional provider.

### Wallet

- `Wallet.create()`: Creates a new wallet.
- `Wallet.get_balance(address)`: Returns the native token balance for a given wallet address.

### Token

- `Token.get_native_balance(address)`: Fetches native token balance.
- `Token.get_erc20_balance(address, contract_address, block_height='latest')`: Fetches ERC20 token balance.
- `Token.transfer_token(to, amount)`: Transfers tokens.
- `Token.wrap_token(from_contract_address, to_contract_address, to, amount)`: Wraps tokens.
- `Token.swap_token(from_contract_address, to_contract_address, to, amount)`: Swaps tokens.

### Transaction

- `Transaction.get_transactions_by_address(address, session='', limit='20')`: Returns transaction list for address.
- `Transaction.get_transaction_by_hash(tx_hash)`: Returns a transaction by hash.
- `Transaction.get_transaction_status(tx_hash)`: Returns the status of a transaction.
- `Transaction.get_transaction_count(address)`: Returns nonce for a wallet.
- `Transaction.get_gas_price()`: Returns current gas price.
- `Transaction.get_fee_data()`: Returns fee-related data.
- `Transaction.estimate_gas(payload)`: Estimates gas for a given transaction payload.

### Contract

- `Contract.get_contract_abi(contract_address, explorer_key)`: Fetches contract ABI.
- `Contract.get_contract_code(contract_address)`: Fetches contract bytecode.

### Block

- `Block.get_current_block()`: Returns the latest block.
- `Block.get_by_tag(tag, tx_detail=False)`: Returns a block by tag or number.

### CronosId

- `CronosId.forward_resolve(cronos_id)`: Resolves CronosId to address.
- `CronosId.reverse_resolve(address)`: Resolves address to CronosId.

### DeFi

- `Defi.get_whitelisted_tokens(protocol)`: Returns list of whitelisted tokens.
- `Defi.get_all_farms(protocol)`: Returns all farms.
- `Defi.get_farm_by_symbol(protocol, symbol)`: Returns specific farm by symbol.

### Exchange

- `Exchange.get_all_tickers()`: Returns all tickers.
- `Exchange.get_ticker_by_instrument(instrument_name)`: Returns specific ticker info.

## Supported Chains

The SDK supports both **Cronos EVM** and **Cronos ZK EVM** networks.

```py
from crypto_com_developer_platform_client.interfaces.chain_interfaces import CronosEvm, CronosZkEvm

CronosEvm.MAINNET     # Chain ID: 25
CronosEvm.TESTNET     # Chain ID: 338
CronosZkEvm.MAINNET   # Chain ID: 388
CronosZkEvm.TESTNET   # Chain ID: 240
```

## License

This project is licensed under the MIT License.

## Contact

If you have any questions or comments about the library, please feel free to open an issue or a pull request on our GitHub repository.
