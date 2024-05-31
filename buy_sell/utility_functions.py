from spl.token.instructions import create_associated_token_account
from spl.token.instructions import get_associated_token_address
from solders.pubkey import Pubkey #type: ignore
from solders.instruction import Instruction #type: ignore
from solana.rpc.types import TokenAccountOpts
from solana.transaction import AccountMeta

from ..utility.constants import RAY_V4_AMM_ID as AMM_PROGRAM_ID
from ..utility.constants import OPEN_BOOK_PROGRAM as SERUM_PROGRAM_ID
from ..utility.layouts import SWAP_LAYOUT 


def make_swap_instruction(client, amount_in: int, token_account_in: Pubkey, token_account_out: Pubkey, accounts: dict, mint: Pubkey, owner : Pubkey ) -> Instruction:

    accountProgramId = client.get_account_info_json_parsed(mint)
    TOKEN_PROGRAM_ID = accountProgramId.value.owner

    keys = [
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["amm_id"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["authority"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["open_orders"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["target_orders"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["base_vault"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["quote_vault"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=SERUM_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["market_id"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["bids"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["asks"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["event_queue"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["market_base_vault"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["market_quote_vault"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["market_authority"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=token_account_in, is_signer=False, is_writable=True),  # UserSourceTokenAccount
        AccountMeta(pubkey=token_account_out, is_signer=False, is_writable=True),  # UserDestTokenAccount
        AccountMeta(pubkey=owner.pubkey(), is_signer=True, is_writable=False)  # UserOwner
    ]

    data = SWAP_LAYOUT.build(
        dict(
            instruction=9,
            amount_in=int(amount_in),
            min_amount_out=0
        )
    )
    return Instruction(AMM_PROGRAM_ID, data, keys)


def get_token_account(client, owner: Pubkey, mint: Pubkey) -> tuple:
    try:
        account_data = client.get_token_accounts_by_owner(owner, TokenAccountOpts(mint))
        return account_data.value[0].pubkey, None
    except:
        swap_associated_token_address = get_associated_token_address(owner, mint)
        swap_token_account_Instructions = create_associated_token_account(owner, owner, mint)

        return swap_associated_token_address, swap_token_account_Instructions
    
    
def sell_get_token_account(client, owner: Pubkey, mint: Pubkey) -> Pubkey:
    try:
        account_data = client.get_token_accounts_by_owner(owner, TokenAccountOpts(mint))
        return account_data.value[0].pubkey
    except:
        print("Mint Token Not found")
        return None
