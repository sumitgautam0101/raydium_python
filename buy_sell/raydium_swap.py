from spl.token.client import Token
from spl.token.core import _TokenCore
from solana.rpc.commitment import Commitment
from spl.token.instructions import close_account, CloseAccountParams
from solders.pubkey import Pubkey #type: ignore
from solders.compute_budget import set_compute_unit_limit, set_compute_unit_price #type: ignore
from solana.rpc.api import Keypair
from solana.transaction import Transaction
import time

# File Imports
from ..utility.constants import LAMPORTS_PER_SOL, WSOL
from .utility_functions import get_token_account, sell_get_token_account
from .utility_functions import make_swap_instruction


def buy(solana_client, mint: Pubkey, payer: Keypair, amount: float, pool_keys: dict = None, GAS_LIMIT: int = 200_337, GAS_PRICE: int = 25_232, slippage: int = 100):

    for _ in range(3):
        
        try:
                    
            """ Calculate amount """
            # lamports_amm = amount * LAMPORTS_PER_SOL
            amount_in =  int(amount * LAMPORTS_PER_SOL)

            """ Get swap token program id """
            accountProgramId = solana_client.get_account_info_json_parsed(mint)
            TOKEN_PROGRAM_ID = accountProgramId.value.owner

            """ Set Mint Token accounts addresses """
            swap_associated_token_address, swap_token_account_Instructions  = get_token_account(solana_client, payer.pubkey(), mint)

            """ Create Wrap Sol Instructions """
            balance_needed = Token.get_min_balance_rent_for_exempt_for_account(solana_client)
            WSOL_token_account, swap_tx, payer, Wsol_account_keyPair, opts, = _TokenCore._create_wrapped_native_account_args(
                TOKEN_PROGRAM_ID, payer.pubkey(), payer,amount_in,False, balance_needed, Commitment("confirmed"))
            

            """ Create Swap Instructions """
            instructions_swap = make_swap_instruction(solana_client, amount_in, WSOL_token_account, swap_associated_token_address, pool_keys, mint, payer)

            """Create Close Account Instructions..."""
            params = CloseAccountParams(account=WSOL_token_account, dest=payer.pubkey(), owner=payer.pubkey(), program_id=TOKEN_PROGRAM_ID)
            closeAcc =(close_account(params))

            """6. Add instructions to transaction..."""

            swap_tx.add(set_compute_unit_limit(GAS_LIMIT)) #my default limit
            swap_tx.add(set_compute_unit_price(GAS_PRICE))

            if swap_token_account_Instructions != None:
                swap_tx.add(swap_token_account_Instructions)

            swap_tx.add(instructions_swap)
            swap_tx.add(closeAcc)

            """ Execute TXN """
            txn = solana_client.send_transaction(swap_tx, payer,Wsol_account_keyPair)
            txid_string_sig = txn.value
            
            if txid_string_sig:

                print(f"Transaction Signature: https://solscan.io/tx/{txid_string_sig}")
                return txid_string_sig

        except Exception as Er:
            print(f"Error while Swaping(BUY) : {Er}")
            time.sleep(10) 

    return

def sell(solana_client, mint: Pubkey, payer: Keypair, amount: float, pool_keys: dict = None, GAS_LIMIT: int = 200_337, GAS_PRICE: int = 25_232, slippage: int = 100):

    for _ in range(3):

        try:

            """ Calculate amount """
            amount_in = int(amount  * (10 ** pool_keys["base_decimals"]) )

            """ Get swap token program id """
            accountProgramId = solana_client.get_account_info_json_parsed(mint)
            TOKEN_PROGRAM_ID = accountProgramId.value.owner

            """Get token accounts"""
            swap_token_account = sell_get_token_account(solana_client, payer.pubkey(), mint)
            WSOL_token_account, WSOL_token_account_Instructions = get_token_account(solana_client,payer.pubkey(), WSOL)

            if swap_token_account == None:
                print("swap_token_account not found...")
                return None
            
            """Make swap instructions"""
            instructions_swap = make_swap_instruction(solana_client, amount_in, swap_token_account, WSOL_token_account, pool_keys, mint, payer)

            """Close wsol account"""
            params = CloseAccountParams(account=WSOL_token_account, dest=payer.pubkey(), owner=payer.pubkey(), program_id=TOKEN_PROGRAM_ID)
            closeAcc =(close_account(params))

            """Create transaction and add instructions"""
            swap_tx = Transaction(fee_payer=payer.pubkey())

            swap_tx.add(set_compute_unit_limit(GAS_LIMIT)) #my default limit
            swap_tx.add(set_compute_unit_price(GAS_PRICE))

            if WSOL_token_account_Instructions != None:
                swap_tx.add(WSOL_token_account_Instructions)

            swap_tx.add(instructions_swap)
            swap_tx.add(closeAcc)

            """ Execute TXN """
            txn = solana_client.send_transaction(swap_tx, payer)
            txid_string_sig = txn.value

            if txid_string_sig:
                print(f"Transaction Signature: https://solscan.io/tx/{txid_string_sig}")

                return txid_string_sig

        except Exception as Er:
            print(f"Error while Swaping(SELL) : {Er}")
            time.sleep(10)

    return
