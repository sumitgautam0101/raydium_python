from solana.rpc.api import Client
from solana.rpc.commitment import Confirmed
from solders.pubkey import Pubkey #type: ignore
from solders.keypair import Keypair #type: ignore
from solders.signature import Signature #type: ignore

# File Imports
from .pool_keys_and_id.get_pool_keys import get_pool_keys
from .buy_sell.raydium_swap import buy, sell
from .token_balance.balance import get_token_balance
from .transfer.transact import transfer_token
from .utility.verify_txn import verify_transaction
from .utility.constants import WSOL
from .config import *


class Raydium:

    GAS_LIMIT = 200000
    GAS_PRICE = 25000

    def __init__(self, wallet_key: str, rpc_url: str = HTTP_ENDPOINT) -> None:
        
        self.client = Client(rpc_url)
        self.payer = Keypair.from_base58_string(wallet_key)
        self.my_wallet = self.payer.pubkey()

    # To fetch Wallet balance
    def token_balance(self, token: str = str(WSOL)) -> tuple:

        token = Pubkey.from_string(token)

        balance = get_token_balance(self.client, token, self.payer)

        return balance
    
    # To verify a transaction
    def verify_txn(self, signature: str) -> bool:

        #TODO: This method if slow, could be enhanced
        verification = verify_transaction(self.client, signature)

        return verification

    # To Transfer Token to another wallet
    def transfer_tokens(self, token: str, reciver_wallet: str, amount: float) -> Signature:

        token = Pubkey.from_string(token)
        reciver_wallet = Pubkey.from_string(reciver_wallet)

        txn = transfer_token(self.client, token, reciver_wallet, amount, self.payer, self.GAS_LIMIT, self.GAS_PRICE)

        return txn
    
    # Pool keys
    def get_pool_data(self, amm_id: str) -> dict:

        amm_id = Pubkey.from_string(amm_id)

        pool_keys = get_pool_keys(self.client, amm_id)

        return pool_keys

    # Buy SWAP TXN 
    def buy_swap(self, amm_id: str, amount: float, pool_keys=None) -> Signature:

        pool_keys = self.get_pool_data(amm_id) if not pool_keys else pool_keys

        if pool_keys:    

            txn = buy(self.client, pool_keys['base_mint'], self.payer, amount, pool_keys, self.GAS_LIMIT, self.GAS_PRICE)

            return txn
    
    # Sell SWAP TXN
    def sell_swap(self, amm_id: str, amount: float, pool_keys=None) -> Signature:

        pool_keys = self.get_pool_data(amm_id) if not pool_keys else pool_keys

        if pool_keys:    

            txn = sell(self.client, pool_keys['base_mint'], self.payer, amount, pool_keys, self.GAS_LIMIT, self.GAS_PRICE)

            return txn
    
    # Sell SWAP TXN using total balance's percent
    def sell_swap_percent(self, amm_id: str, percent: float, pool_keys=None) -> Signature:

        pool_keys = self.get_pool_data(amm_id) if not pool_keys else pool_keys

        if pool_keys:    

            wallet_balance = self.token_balance(str(pool_keys['base_mint']))

            if wallet_balance:
                    
                amount = wallet_balance[1] * (percent / 100)

                txn = sell(self.client, pool_keys['base_mint'], self.payer, amount, pool_keys, self.GAS_LIMIT, self.GAS_PRICE)

                return txn


