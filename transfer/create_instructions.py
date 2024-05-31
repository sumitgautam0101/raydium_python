from spl.token.constants import TOKEN_PROGRAM_ID
from solders.system_program import TransferParams, transfer
from spl.token.instructions import create_associated_token_account, get_associated_token_address
from solana.rpc.types import TokenAccountOpts
from solders.pubkey import Pubkey #type: ignore
from solana.rpc.api import Keypair

import spl.token.instructions as spl_token

# File Import
from ..utility.constants import LAMPORTS_PER_SOL


def getTokenAccount_your_own(client, wallet_pk: Pubkey, mint: Pubkey):
        try:
            account_data = client.get_token_accounts_by_owner(wallet_pk, TokenAccountOpts(mint))
            return account_data.value[0].pubkey, None
        except:
            swap_associated_token_address = get_associated_token_address(wallet_pk, mint)
            swap_token_account_Instructions = create_associated_token_account(wallet_pk, wallet_pk, mint)
            return swap_associated_token_address, swap_token_account_Instructions



def getTokenAccount_Reciever(client, sender_pk: Pubkey, wallet_pk: Pubkey, mint: Pubkey):
        try:
            account_data = client.get_token_accounts_by_owner(wallet_pk, TokenAccountOpts(mint))
            return account_data.value[0].pubkey, None
        except:
            swap_associated_token_address = get_associated_token_address(wallet_pk, mint)
            swap_token_account_Instructions = create_associated_token_account(sender_pk, wallet_pk, mint)
            return swap_associated_token_address, swap_token_account_Instructions



"""Other tokens Transfer"""
def spl_token_transfer(solana_client, sender: Keypair, reciver: Pubkey, source_account: Pubkey, dest_account: Pubkey, token_address: Pubkey, amount:float):
    try:
        """ Instruction Creation """
        token_decimals = solana_client.get_account_info_json_parsed(token_address).value.data.parsed['info']['decimals']
        amount_in_lamports = int(amount * (10 ** token_decimals))


        transfer_instruction = spl_token.transfer(
                                        spl_token.TransferParams(
                                            program_id=TOKEN_PROGRAM_ID,
                                            source=source_account,
                                            dest=dest_account,
                                            owner=sender.pubkey(),
                                            amount=amount_in_lamports,
                                            signers=[sender.pubkey()],
                                        )
                                     )

        return transfer_instruction
    
    except:
        return None



"""SOL Transfer"""

def sol_transfer(sender: Keypair, receiver: Pubkey, amount: float):
    try:
        amount_in_lamports = int(amount * LAMPORTS_PER_SOL)
        transfer_instruction = transfer(
            TransferParams(
                from_pubkey=sender.pubkey(),
                to_pubkey=receiver,
                lamports=amount_in_lamports
                )
            )
        return transfer_instruction
    except:
        return None