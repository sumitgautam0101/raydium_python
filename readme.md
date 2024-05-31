# Raydium Trading API ```raydium-python```

This project provides a set of functions for interacting with Raydium, a decentralized exchange on the Solana blockchain. It includes functionalities to retrieve pool keys, execute buy and sell swaps, and check token balances.

# Donations
If you find this project helpful and would like to support its development, you can make a donation. Donations help keep the project running and motivate the contributors to add new features.

```
BSC Address: 0x60f99B659f34a2e9f4a085bB9a2aDB62Dbf0064E
Solana Address: 4ugq7zXaJZHL47HD8gZ65pGcwbzLZhvzcRQKnA5Nikwc
Ethereum Address: 0x31e02bFB7a76a6BE128B6191335cDE818174c08a
```


## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/sumitgautam0101/raydium-python.git
    cd raydium-python
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Setting up client `foo.py` file:
    ```python
    from raydium_python import Raydium

    WALLET_KEY = "YOUR_WALLET_SECRET_KEY"
    client = Raydium(WALLET_KEY) #if you have your private RPC you can pass it's endpoint as 2nd parameter 
    ```

## Methods Available

```token_balance``` : Fetches the token balance of the wallet for the specified token.
Parameters:

* token (str, optional): The public key of the token to check the balance for. Default is WSOL.


```verify_txn``` : Verifies the status of a transaction on the Solana blockchain.
Parameters:

* signature (str): The signature of the transaction to verify.




```transfer_tokens``` : Transfers a specified amount of tokens to another wallet.
Parameters:

* token (str): The public key of the token to transfer.
* receiver_wallet (str): The public key of the receiver's wallet.
* amount (float): The amount of tokens to transfer.


```get_pool_data``` : Retrieves the pool keys and data for a specific AMM.
Parameters:

* amm_id (str): The public key of the Automated Market Maker (AMM) to get pool data from.


```buy_swap``` : Executes a buy swap transaction on the specified AMM.
Parameters:

* amm_id (str): The public key of the AMM to interact with.
* amount (float): The amount of tokens to swap.
* pool_keys (optional): Pre-fetched pool keys. If not provided, they will be fetched automatically.


```sell_swap``` : Executes a sell swap transaction on the specified AMM.
Parameters:

* amm_id (str): The public key of the AMM to interact with.
* amount (float): The amount of tokens to swap.
* pool_keys (optional): Pre-fetched pool keys. If not provided, they will be fetched automatically.


```sell_swap_percent``` : Executes a sell swap transaction using a specified percentage of the wallet's total token balance.
Parameters:

* amm_id (str): The public key of the AMM to interact with.
* percent (float): The percentage of the wallet's total balance to swap.
* pool_keys (optional): Pre-fetched pool keys. If not provided, they will be fetched automatically.


## Raydium Class Constants
```GAS_LIMIT``` : Description: The maximum amount of gas to use for transactions.
* Default: 200000

```GAS_PRICE```
Description: The price of gas per unit.
* Default: 25000




