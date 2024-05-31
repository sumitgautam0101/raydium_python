from solana.rpc.types import TokenAccountOpts
from solders.pubkey import Pubkey #type: ignore
from solana.rpc.api import Keypair
import time

# File Imports
from ..utility.constants import WSOL, LAMPORTS_PER_SOL


def get_token_balance(solana_client, mint: Pubkey, payer: Keypair) -> tuple:

    for _ in range(3):

        try:

            if mint == WSOL:

                account = solana_client.get_account_info(payer.pubkey())

                sol_lamports = account.value.lamports

                return sol_lamports, sol_lamports / LAMPORTS_PER_SOL
            
            else:

                accountProgramId = solana_client.get_account_info_json_parsed(mint)
                programid_of_token = accountProgramId.value.owner
                accounts = solana_client.get_token_accounts_by_owner_json_parsed(payer.pubkey(), TokenAccountOpts(program_id=programid_of_token))


                for account in accounts.value:
                    mint_in_acc = account.account.data.parsed['info']['mint']
                    if mint_in_acc == str(mint):
                        balance = int(account.account.data.parsed['info']['tokenAmount']['amount'])
                        ui_balance = float(account.account.data.parsed['info']['tokenAmount']['uiAmount'])

                        return balance, ui_balance
                    
        except Exception as Er:
            print("Error while fetching Balance --> ", Er)
            time.sleep(5)

    return None, None


