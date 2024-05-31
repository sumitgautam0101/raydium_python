from solders.compute_budget import set_compute_unit_limit, set_compute_unit_price #type: ignore
from solders.keypair import Keypair #type: ignore
from solders.pubkey import Pubkey #type: ignore
from solana.transaction import Transaction

# File Imports
from .create_instructions import getTokenAccount_your_own, getTokenAccount_Reciever
from .create_instructions import sol_transfer, spl_token_transfer
from ..utility.constants import WSOL


def transfer_token(solana_client, token : Pubkey, receiver : Pubkey, token_amount : float, payer: Keypair, GAS_LIMIT: int = 200_000, GAS_PRICE: int = 50_000):

    """ Transaction Creation """
    transaction = Transaction(fee_payer=payer.pubkey())
    transaction.add(set_compute_unit_limit(GAS_LIMIT))
    transaction.add(set_compute_unit_price(GAS_PRICE))

    transfer_instructions = None

    if token == WSOL or token == Pubkey.from_string("So11111111111111111111111111111111111111111"):

        transfer_instructions = sol_transfer(payer, receiver, token_amount)

    else:
        """ Any Other Token """    

        sender_token_account, ATA_Inst = getTokenAccount_your_own(solana_client, payer.pubkey(), token)
        if ATA_Inst != None:
            transaction.add(ATA_Inst)
        if sender_token_account != None:
            reciever_token_account, ATA_Inst = getTokenAccount_Reciever(solana_client, payer.pubkey(), receiver, token)
            if ATA_Inst != None:
                transaction.add(ATA_Inst)
        if sender_token_account != None and reciever_token_account != None:

                transfer_instructions = spl_token_transfer(solana_client, payer, receiver, sender_token_account, reciever_token_account, token, token_amount)


    if transfer_instructions != None:
        transaction.add(transfer_instructions)

        """ Txn execution and confirmation """

        try:
            # print("Execute Transaction...")
            txn = solana_client.send_transaction(transaction, payer)
            txid_string_sig = txn.value

            print(f"https://solscan.io/tx/{txid_string_sig}")

            return txid_string_sig

        except Exception as Er:
            
            print("Error while transferring tokens -> ", Er)
            
